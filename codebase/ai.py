"""Nối model — chỗ DUY NHẤT trong bản chạy thử gọi model AI.

Hợp đồng (giữ nguyên để khung đo được token):
    call_model(system: str, user: str) -> dict với 4 khoá
        "text":       str   chữ model trả về
        "model":      str   tên model đã gọi (để tra giá ở bảng giá model)
        "tokens_in":  int   số token vào, lấy từ trường usage trong phản hồi API — KHÔNG ước lượng
        "tokens_out": int   số token ra, gồm cả token suy luận / suy nghĩ nếu API tính riêng
    @model_call (từ tracing.py) tự ghi mỗi lần gọi vào trace; agent.py gọi call_model bao nhiêu lần
    cũng được, khung tự cộng token.

Chế độ giả (mặc định khi .env chưa có MODEL_PROVIDER, hoặc MODEL_PROVIDER=fake):
    trả một câu giả cố định, model "fake", token 0 — để luồng chạy hết từ trước CP2 (guide bước 3.2).

Hỗ trợ sẵn các nhà cung cấp:
    - fake: Chạy thử kiểm tra khung không tốn token
    - gemini: Gọi Google Gemini API bằng urllib chuẩn
    - openai: Gọi OpenAI / DeepSeek / Groq (OpenAI compatible)
    - anthropic: Gọi Claude API
    - ollama: Gọi model local
"""
import json
import os
import urllib.error
import urllib.request

from tracing import model_call

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_env(path=os.path.join(ROOT, ".env")):
    """Đọc file .env (KEY=VALUE mỗi dòng) vào biến môi trường, không ghi đè biến đã có. Khung — không cần sửa."""
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env()
MODEL_PROVIDER = (os.environ.get("MODEL_PROVIDER") or "fake").strip().lower()
MODEL_NAME = (os.environ.get("MODEL_NAME") or "gemini-2.5-flash").strip()
API_KEY = (os.environ.get("API_KEY") or "").strip()

SHOW_RAW = False


def post_json(url, headers, body, timeout=60):
    """Gửi POST JSON, trả về JSON phản hồi. Chỉ dùng thư viện chuẩn (urllib)."""
    req = urllib.request.Request(
        url, data=json.dumps(body).encode("utf-8"), method="POST",
        headers=dict({"Content-Type": "application/json"}, **headers))
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", "replace")[:400]
        raise RuntimeError("HTTP %d: %s" % (e.code, error_body))
    if SHOW_RAW:
        print(json.dumps(data, ensure_ascii=False, indent=2)[:3000])
    return data


def call_openai(system, user, base_url=None):
    """Gọi OpenAI / OpenRouter / OpenAI-compatible endpoint."""
    url = base_url or os.environ.get("OPENAI_BASE_URL") or "https://api.openai.com/v1/chat/completions"
    messages = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": user}]
    headers = {
        "Authorization": "Bearer " + API_KEY,
        "HTTP-Referer": "https://github.com/nguyenduong43/K5-Day15-L3B-TTDV",
        "X-Title": "Food Delivery Dispute AI"
    }
    data = post_json(url, headers,
                     {"model": MODEL_NAME or "gpt-4o-mini", "messages": messages, "max_tokens": 2048})
    u = data.get("usage", {})
    return {
        "text": data["choices"][0]["message"]["content"],
        "tokens_in": u.get("prompt_tokens", 0),
        "tokens_out": u.get("completion_tokens", 0)
    }


def call_gemini(system, user):
    """Gọi Google Gemini REST API qua urllib chuẩn."""
    model = MODEL_NAME or "gemini-2.5-flash"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={API_KEY}"
    body = {
        "contents": [{"parts": [{"text": user}]}]
    }
    if system:
        body["system_instruction"] = {"parts": [{"text": system}]}

    data = post_json(url, {}, body)
    text = ""
    try:
        parts = data["candidates"][0]["content"]["parts"]
        text = "".join(p.get("text", "") for p in parts)
    except Exception:
        text = str(data)

    usage = data.get("usageMetadata", {})
    tokens_in = usage.get("promptTokenCount", 0)
    tokens_out = usage.get("candidatesTokenCount", 0)

    return {
        "text": text,
        "tokens_in": tokens_in,
        "tokens_out": tokens_out
    }


def call_claude(system, user):
    """Gọi Anthropic Claude API."""
    url = "https://api.anthropic.com/v1/messages"
    data = post_json(url,
                     {"x-api-key": API_KEY, "anthropic-version": "2023-06-01"},
                     {"model": MODEL_NAME or "claude-3-5-haiku-20241022", "max_tokens": 1024, "system": system or "",
                      "messages": [{"role": "user", "content": user}]})
    text = "".join(b.get("text", "") for b in data.get("content", []) if b.get("type") == "text")
    u = data.get("usage", {})
    return {"text": text, "tokens_in": u.get("input_tokens", 0), "tokens_out": u.get("output_tokens", 0)}


def call_ollama(system, user):
    """Gọi local Ollama."""
    url = os.environ.get("OLLAMA_URL") or "http://localhost:11434/api/chat"
    messages = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": user}]
    data = post_json(url, {}, {"model": MODEL_NAME, "messages": messages, "stream": False}, timeout=300)
    return {
        "text": data["message"]["content"],
        "tokens_in": data.get("prompt_eval_count", 0),
        "tokens_out": data.get("eval_count", 0)
    }


@model_call
def call_model(system: str, user: str) -> dict:
    provider = MODEL_PROVIDER
    if not provider or provider == "fake":
        last = (user.strip().splitlines() or [""])[-1]
        return {
            "text": "[câu trả lời giả — chưa nối model] " + last[:60],
            "model": "fake",
            "tokens_in": 0,
            "tokens_out": 0
        }

    if provider in ("gemini", "google"):
        r = call_gemini(system, user)
    elif provider in ("openai", "openrouter", "deepseek", "groq"):
        url = None
        if provider == "openrouter":
            url = "https://openrouter.ai/api/v1/chat/completions"
        elif provider == "deepseek":
            url = "https://api.deepseek.com/chat/completions"
        elif provider == "groq":
            url = "https://api.groq.com/openai/v1/chat/completions"
        r = call_openai(system, user, base_url=url)
    elif provider in ("anthropic", "claude"):
        r = call_claude(system, user)
    elif provider == "ollama":
        r = call_ollama(system, user)
    else:
        raise NotImplementedError(f"Chưa hỗ trợ MODEL_PROVIDER={provider} trong codebase/ai.py")

    return {
        "text": r["text"],
        "model": MODEL_NAME or provider,
        "tokens_in": int(r["tokens_in"]),
        "tokens_out": int(r["tokens_out"])
    }
