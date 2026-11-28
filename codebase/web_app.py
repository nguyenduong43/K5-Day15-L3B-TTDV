"""Serve the D1 prototype on loopback with the existing Python workflow."""

import json
import os
import sys
import webbrowser
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Lock

import ai
import tracing
from agent import answer
from tools import _load_db


HOST = "127.0.0.1"
DEFAULT_PORT = 8765
MAX_BODY_BYTES = 8192
MAX_TEXT_LENGTH = 1600
WEB_ROOT = Path(__file__).with_name("web")
ASSETS = {
    "/": ("index.html", "text/html; charset=utf-8"),
    "/app.css": ("app.css", "text/css; charset=utf-8"),
    "/app.js": ("app.js", "text/javascript; charset=utf-8"),
}
RESULT_TYPES = {
    "issue_refund_voucher": "refund",
    "escalate_to_human": "escalated",
}
PROVIDER_ERRORS = {
    "401": "AI từ chối API key. Kiểm tra cấu hình .env trên máy chạy.",
    "402": "Tài khoản của nhà cung cấp AI chưa đủ số dư.",
    "429": "Nhà cung cấp AI đang giới hạn lượt gọi. Hãy chờ rồi thử lại.",
}
# Tracing shares one active case within a process.
ANSWER_LOCK = Lock()


def demo_info():
    provider = ai.MODEL_PROVIDER
    if not provider or provider == "fake":
        mode = "fake"
    elif provider != "ollama" and not ai.API_KEY:
        mode = "missing"
    else:
        mode = "configured"

    orders = [
        {
            "id": order_id,
            "restaurant": order["restaurant"],
            "items": [{"name": item["name"], "price": item["price"]} for item in order["items"]],
        }
        for order_id, order in _load_db().get("orders", {}).items()
    ]
    return {"mode": mode, "orders": orders}


def process_claim(text):
    tracing.begin("web")
    try:
        response = answer(text)
    finally:
        summary, events = tracing.end()

    status = next(
        (RESULT_TYPES[event["name"]] for event in reversed(events)
         if event["kind"] == "tool" and event["name"] in RESULT_TYPES),
        "review",
    )
    return {
        "status": status,
        "output": response["output"],
        "models": summary["models"],
        "tool_calls": summary["tool_calls"],
        "tokens_in": summary["tokens_in"],
        "tokens_out": summary["tokens_out"],
    }


class WebHandler(BaseHTTPRequestHandler):
    def setup(self):
        super().setup()
        self.connection.settimeout(12)

    def log_message(self, format, *args):
        # Keep demo inputs and browser request details out of the terminal.
        return

    def send_response_body(self, status, content_type, body):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'self'; frame-ancestors 'none'; base-uri 'none'")
        self.end_headers()
        self.wfile.write(body)

    def send_json(self, status, data):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response_body(status, "application/json; charset=utf-8", body)

    def valid_host(self):
        port = self.server.server_port
        return self.headers.get("Host") in {f"{HOST}:{port}", f"localhost:{port}"}

    def do_GET(self):
        if not self.valid_host():
            self.send_json(HTTPStatus.FORBIDDEN, {"error": "Hãy mở địa chỉ cục bộ hiện trong terminal."})
            return
        if self.path == "/api/demo":
            self.send_json(HTTPStatus.OK, self.server.demo_info)
            return
        asset = ASSETS.get(self.path)
        if asset is None:
            self.send_json(HTTPStatus.NOT_FOUND, {"error": "Không tìm thấy trang."})
            return
        filename, content_type = asset
        self.send_response_body(HTTPStatus.OK, content_type, (WEB_ROOT / filename).read_bytes())

    def do_POST(self):
        origin = self.headers.get("Origin")
        if not self.valid_host() or (origin and origin != f"http://{self.headers['Host']}"):
            self.send_json(HTTPStatus.FORBIDDEN, {"error": "Yêu cầu phải được gửi từ trang bản thử."})
            return
        if self.path != "/api/claim":
            self.send_json(HTTPStatus.NOT_FOUND, {"error": "Không tìm thấy trang."})
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= MAX_BODY_BYTES or self.headers.get_content_type() != "application/json":
                raise ValueError
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            text = payload.get("text") if isinstance(payload, dict) else None
            if not isinstance(text, str) or not 0 < len(text.strip()) <= MAX_TEXT_LENGTH:
                raise ValueError
        except (ValueError, TimeoutError):
            self.send_json(HTTPStatus.BAD_REQUEST, {"error": "Nhập thông tin khiếu nại tối đa 1.600 ký tự."})
            return

        if self.server.demo_info["mode"] == "missing":
            self.send_json(HTTPStatus.SERVICE_UNAVAILABLE, {"error": "Chưa có API key trong cấu hình .env."})
            return
        if not ANSWER_LOCK.acquire(blocking=False):
            self.send_json(HTTPStatus.TOO_MANY_REQUESTS, {"error": "Đang xử lý một yêu cầu khác. Hãy thử lại sau."})
            return

        try:
            result = process_claim(text.strip())
        except Exception as exc:
            code = str(exc).split(":", 1)[0].removeprefix("HTTP ")
            message = PROVIDER_ERRORS.get(code, "Chưa nhận được phản hồi. Kiểm tra kết nối hoặc cấu hình AI rồi thử lại.")
            self.send_json(HTTPStatus.BAD_GATEWAY, {"error": message})
        else:
            self.send_json(HTTPStatus.OK, result)
        finally:
            ANSWER_LOCK.release()


def run_web(open_browser=False):
    try:
        port = int(os.environ.get("TTDV_PORT", DEFAULT_PORT))
        if not 0 <= port <= 65535:
            raise ValueError
    except ValueError:
        print("TTDV_PORT phải là số nguyên từ 0 đến 65535.", file=sys.stderr)
        return 1

    try:
        with ThreadingHTTPServer((HOST, port), WebHandler) as server:
            server.demo_info = demo_info()
            url = f"http://{HOST}:{server.server_port}"
            print(f"Giao diện TTDV: {url}  (Ctrl+C để dừng)", flush=True)
            if open_browser:
                try:
                    webbrowser.open(url)
                except (OSError, webbrowser.Error):
                    pass  # Người dùng có thể mở địa chỉ đã in ở trên.
            server.serve_forever()
    except KeyboardInterrupt:
        return 0
    except OSError as exc:
        print(f"Không mở được giao diện trên cổng {port}: {exc}", file=sys.stderr)
        return 1
    return 0
