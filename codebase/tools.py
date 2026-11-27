"""Công cụ của bài toán D1 — Xử lý khiếu nại đơn giao đồ ăn thiếu món.

Mỗi công cụ là một hàm Python có @tool. Docstring ghi đúng 4 ý như sơ đồ ở spec.md §4:
    tên · input · output · có tác động ra ngoài không (gửi tin, sửa dữ liệu, chấm điểm…)
Khung tự ghi mỗi lần gọi công cụ vào trace (tên, input, output rút gọn, thời gian, lỗi).

Tuân thủ quy định AGENTS.md:
    Các công cụ có tác động ra ngoài chỉ tạo bản nháp mô phỏng (draft) chờ người duyệt.
"""
import json
import os
import re
from tracing import tool, TOOLS  # noqa: F401

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(ROOT, "data", "orders_db.json")
POLICIES_PATH = os.path.join(ROOT, "data", "policies.json")


def _load_db() -> dict:
    db = {}
    if os.path.exists(DATA_PATH):
        try:
            with open(DATA_PATH, "r", encoding="utf-8") as f:
                db = json.load(f)
        except Exception:
            pass
    if os.path.exists(POLICIES_PATH):
        try:
            with open(POLICIES_PATH, "r", encoding="utf-8") as f:
                pdata = json.load(f)
                if "policies" in pdata:
                    db.setdefault("policies", {}).update(pdata["policies"])
                if "global_constraints" in pdata:
                    db["global_constraints"] = pdata["global_constraints"]
        except Exception:
            pass
    if db:
        return db
    # Fallback dữ liệu nội tại nếu không đọc được file
    return {
        "orders": {
            "ORD-101": {
                "order_id": "ORD-101",
                "user_id": "U1",
                "restaurant": "Cơm Tấm Ba Ghiền",
                "items": [
                    {"id": "item_1", "name": "Cơm sườn nướng", "price": 65000, "quantity": 1},
                    {"id": "item_2", "name": "Canh rong biển", "price": 15000, "quantity": 1},
                    {"id": "item_3", "name": "Trà đá đường", "price": 10000, "quantity": 1}
                ],
                "shipping_fee": 16000,
                "total_paid": 96000,
                "status": "delivered",
                "claimed_items": []
            },
            "ORD-102": {
                "order_id": "ORD-102",
                "user_id": "U2",
                "restaurant": "Trà Sữa ToCoToCo",
                "items": [
                    {"id": "item_1", "name": "Trà sữa trân châu sợi", "price": 42000, "quantity": 1},
                    {"id": "item_2", "name": "Trà đào hạt chia", "price": 38000, "quantity": 1}
                ],
                "shipping_fee": 15000,
                "total_paid": 95000,
                "status": "delivered",
                "claimed_items": []
            },
            "ORD-103": {
                "order_id": "ORD-103",
                "user_id": "U3_ABUSE",
                "restaurant": "Gà Rán KFC",
                "items": [
                    {"id": "item_1", "name": "Combo gà rán 3 miếng", "price": 105000, "quantity": 1},
                    {"id": "item_2", "name": "Khoai tây chiên vừa", "price": 25000, "quantity": 1}
                ],
                "shipping_fee": 20000,
                "total_paid": 150000,
                "status": "delivered",
                "claimed_items": []
            }
        },
        "policies": {
            "missing_item": {
                "issue_type": "missing_item",
                "max_auto_refund_amount": 50000,
                "max_claims_monthly": 3,
                "action": "refund_item_price_or_voucher"
            }
        },
        "user_complaint_history": {
            "U1": {"user_id": "U1", "complaints_this_month": 0, "trust_score": "high"},
            "U2": {"user_id": "U2", "complaints_this_month": 1, "trust_score": "medium"},
            "U3_ABUSE": {"user_id": "U3_ABUSE", "complaints_this_month": 4, "trust_score": "low"}
        }
    }


@tool
def get_order(order_id: str) -> dict:
    """Tra cứu chi tiết đơn hàng theo mã đơn (order_id).
    Input: order_id (str) — mã đơn hàng (ví dụ 'ORD-101').
    Output: dict chứa danh sách món, đơn giá, tổng tiền, giờ giao và trạng thái.
    Có tác động ra ngoài không: Không (chỉ đọc dữ liệu)."""
    db = _load_db()
    order_id_clean = (order_id or "").strip().upper()
    order = db.get("orders", {}).get(order_id_clean)
    if order:
        return {"found": True, "order": order}
    return {"found": False, "message": f"Không tìm thấy đơn hàng với mã '{order_id}'"}


@tool
def get_policy(issue_type: str = "missing_item") -> dict:
    """Tra cứu chính sách bồi thường theo loại sự cố khiếu nại.
    Input: issue_type (str) — loại sự cố, mặc định là 'missing_item'.
    Output: dict chứa hạn mức hoàn tiền tối đa và điều kiện bồi thường.
    Có tác động ra ngoài không: Không (chỉ đọc chính sách)."""
    db = _load_db()
    policy = db.get("policies", {}).get(issue_type, db.get("policies", {}).get("missing_item"))
    return policy or {
        "issue_type": "missing_item",
        "max_auto_refund_amount": 50000,
        "max_claims_monthly": 3
    }


@tool
def get_complaint_history(user_id: str) -> dict:
    """Tra cứu lịch sử khiếu nại trong 30 ngày của người dùng.
    Input: user_id (str) — mã người dùng (ví dụ 'U1').
    Output: dict số lần khiếu nại và điểm tin cậy tài khoản.
    Có tác động ra ngoài không: Không (chỉ đọc lịch sử)."""
    db = _load_db()
    history = db.get("user_complaint_history", {}).get(user_id)
    if history:
        return history
    return {"user_id": user_id, "complaints_this_month": 0, "trust_score": "medium"}


@tool
def check_claim_limit(order_id: str, item_name: str) -> dict:
    """Bộ chặn rủi ro bằng Code Python thuần: đối soát đơn hàng và hạn mức bồi thường.
    Input: order_id (str) — mã đơn hàng, item_name (str) — tên món khách báo thiếu.
    Output: dict kết quả kiểm tra (is_valid: bool, decision: str, allowed_amount: int, reason: str).
    Có tác động ra ngoài không: Không (chỉ thẩm định logic cứng trong bộ nhớ)."""
    db = _load_db()
    order_id_clean = (order_id or "").strip().upper()
    order = db.get("orders", {}).get(order_id_clean)

    if not order:
        return {
            "is_valid": False,
            "decision": "order_not_found",
            "allowed_amount": 0,
            "reason": f"Không tìm thấy mã đơn hàng '{order_id}' trong hệ thống."
        }

    # Tìm kiếm món trong đơn hàng (so khớp tương đối không phân biệt hoa thường)
    target = (item_name or "").strip().lower()
    matched_item = None
    for it in order.get("items", []):
        name_lower = it["name"].lower()
        if target in name_lower or name_lower in target:
            matched_item = it
            break

    if not matched_item:
        items_list = [it["name"] for it in order.get("items", [])]
        return {
            "is_valid": False,
            "decision": "item_not_in_order",
            "allowed_amount": 0,
            "available_items": items_list,
            "reason": f"Món '{item_name}' không có trong danh sách món của đơn {order_id}."
        }

    # Kiểm tra món đã được bồi thường trước đó chưa
    if matched_item["name"] in order.get("claimed_items", []):
        return {
            "is_valid": False,
            "decision": "already_claimed",
            "allowed_amount": 0,
            "reason": f"Món '{matched_item['name']}' của đơn {order_id} đã được xử lý bồi thường trước đó."
        }

    item_price = matched_item.get("price", 0)
    policy = get_policy("missing_item")
    max_limit = policy.get("max_auto_refund_amount", 50000)

    # Kiểm tra lịch sử khiếu nại của người dùng
    user_id = order.get("user_id", "")
    history = get_complaint_history(user_id)
    if history.get("complaints_this_month", 0) >= policy.get("max_claims_monthly", 3):
        return {
            "is_valid": False,
            "decision": "escalate_abuse",
            "item_name": matched_item["name"],
            "item_price": item_price,
            "allowed_amount": 0,
            "reason": "Tài khoản có tần suất khiếu nại vượt ngưỡng an toàn trong tháng, cần chuyển CSKH thẩm định."
        }

    # Kiểm tra giá trị món có vượt trần không
    if item_price > max_limit:
        return {
            "is_valid": False,
            "decision": "escalate_over_limit",
            "item_name": matched_item["name"],
            "item_price": item_price,
            "allowed_amount": 0,
            "reason": f"Giá trị món ({item_price:,}đ) vượt quá hạn mức bồi thường tự động ({max_limit:,}đ)."
        }

    return {
        "is_valid": True,
        "decision": "auto_refund",
        "item_name": matched_item["name"],
        "item_price": item_price,
        "allowed_amount": item_price,
        "reason": f"Món '{matched_item['name']}' hợp lệ và trong hạn mức {max_limit:,}đ."
    }


@tool
def issue_refund_voucher(order_id: str, item_name: str, amount: int, reason: str = "") -> dict:
    """Tạo bản nháp bồi thường / voucher hoàn tiền mô phỏng (tuân thủ luật AGENTS.md).
    Input: order_id, item_name, amount (số tiền VNĐ), reason.
    Output: dict thông tin mã giao dịch bồi thường mô phỏng.
    Có tác động ra ngoài không: Có (tạo bản nháp giao dịch bồi thường mô phỏng)."""
    order_id_clean = (order_id or "").strip().upper()
    return {
        "status": "draft_voucher_created",
        "order_id": order_id_clean,
        "item_name": item_name,
        "refund_amount": amount,
        "voucher_code": f"REFUND-{order_id_clean[-4:]}-{amount // 1000}K",
        "action": "wallet_refund_simulation",
        "note": "Bản nháp mô phỏng bồi thường hoàn tất thành công trong hạn mức."
    }


@tool
def escalate_to_human(order_id: str, reason: str, summary: str = "") -> dict:
    """Tạo phiếu hỗ trợ khẩn cấp chuyển chuyên viên CSKH thẩm định trực tiếp (HITL).
    Input: order_id, reason (lý do chuyển), summary (tóm tắt bối cảnh ca khiếu nại).
    Output: dict mã ticket hỗ trợ và mức độ ưu tiên.
    Có tác động ra ngoài không: Có (tạo ticket hỗ trợ trong hệ thống CSKH)."""
    order_id_clean = (order_id or "").strip().upper()
    return {
        "status": "ticket_escalated",
        "order_id": order_id_clean,
        "ticket_id": f"TICK-{order_id_clean[-4:] if order_id_clean else 'GEN'}-CSKH",
        "priority": "HIGH" if "ngộ độc" in reason.lower() or "dị vật" in reason.lower() else "MEDIUM",
        "reason": reason,
        "summary": summary
    }
