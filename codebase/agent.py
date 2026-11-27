"""Luồng chính của bản chạy thử — D1 Xử lý khiếu nại đơn giao đồ ăn thiếu món.

`python run.py`, `python run.py eval` và `python run.py simulate` đều gọi answer(text).

Hợp đồng:
    answer(text: str) -> dict có khoá "output" (str): kết quả đưa cho người dùng.
    Token, tên model, số lần gọi model / công cụ: khung tự đếm qua call_model và @tool — không cần trả.

Kiến trúc: Fixed Workflow 3 bước với Guardrail bằng Code Python:
    1. AI/Regex nhận diện thực thể (Mã đơn, Món thiếu, Từ khóa an toàn/đe dọa).
    2. Tra cứu dữ liệu (get_order, get_policy, get_complaint_history) và Thẩm định bằng Code (check_claim_limit).
    3. Phân nhánh: Auto-resolve (issue_refund_voucher) hoặc Chuyển CSKH (escalate_to_human) hoặc Hỏi lại (G10).
"""
import json
import re
from ai import call_model
from tools import (
    get_order,
    get_policy,
    get_complaint_history,
    check_claim_limit,
    issue_refund_voucher,
    escalate_to_human,
)
from tracing import note

SYSTEM_EXTRACTOR = """Bạn là trợ lý AI phân tích khiếu nại giao đồ ăn.
Nhiệm vụ của bạn là đọc tin nhắn của khách và trích xuất các thông tin sau dưới dạng JSON:
{
  "order_id": "Mã đơn hàng nếu có (ví dụ ORD-101, ORD-102), hoặc null nếu không có",
  "missing_item": "Tên món bị thiếu hoặc phàn nàn nếu có, hoặc null",
  "safety_risk": true/false (true nếu có yếu tố ngộ độc, dị vật, bạo lực, xúc phạm, dọa bóc phốt, dọa đánh giá 1 sao, đòi hoàn 100% cả đơn),
  "is_vague": true/false (true nếu chỉ than phiền chung chung thiếu món mà không chỉ rõ món nào)
}
Chỉ trả về JSON duy nhất, không giải thích thêm."""

SYSTEM_RESPONDER = """Bạn là trợ lý Chăm sóc Khách hàng chuyên nghiệp của ứng dụng giao đồ ăn.
Hãy viết phản hồi xoa dịu khách hàng dựa trên dữ kiện hệ thống đã cung cấp.
Nguyên tắc:
- Lịch sự, chân thành xin lỗi vì sự cố bữa ăn.
- Nếu được bồi thường: Nói rõ tên món và số tiền hoàn đúng bằng giá món trong hóa đơn (G11).
- Nếu chuyển chuyên viên CSKH: Giải thích lý do và cung cấp mã ticket hỗ trợ.
- Nếu thiếu thông tin: Hỏi lại đúng 1 câu duy nhất kèm danh sách món (G10).
- Tuyệt đối không hứa phạt tài xế hay đóng cửa quán ăn. Không tiết lộ thông tin cá nhân các bên."""


def _extract_intent_and_entities(text: str) -> dict:
    """Trích xuất thực thể kết hợp LLM và heuristic regex để đảm bảo độ tin cậy 100%."""
    # 1. Heuristic regex tìm mã đơn dạng ORD-xxx hoặc mã tương tự
    order_id_match = re.search(r'\b(ORD-\d{3,6})\b', text, re.IGNORECASE)
    order_id = order_id_match.group(1).upper() if order_id_match else None

    # 2. Heuristic phát hiện nguy cơ an toàn hoặc đe dọa đòi bồi thường 100%
    text_lower = text.lower()
    safety_keywords = [
        "ngộ độc", "đau bụng", "nhập viện", "dị vật", "sâu", "gián", "ruồi",
        "bóc phốt", "đánh giá 1 sao", "1 sao", "tẩy chay", "kiện",
        "hoàn 100%", "hoàn toàn bộ", "toàn bộ đơn", "toàn bộ tiền", "đền hết"
    ]
    safety_risk = any(kw in text_lower for kw in safety_keywords)

    # 3. Gọi model AI phân tích ngữ nghĩa (ghi nhận token vào tracing)
    prompt = f"Phân tích tin nhắn sau:\n{text}"
    model_res = call_model(SYSTEM_EXTRACTOR, prompt)
    ai_text = model_res.get("text", "")

    # Phân tích kết quả từ AI (nếu model trả về JSON hợp lệ)
    ai_item = None
    ai_vague = False
    try:
        json_match = re.search(r'\{.*\}', ai_text, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group(0))
            if not order_id and data.get("order_id"):
                order_id = str(data["order_id"]).strip().upper()
            if data.get("safety_risk"):
                safety_risk = True
            ai_item = data.get("missing_item")
            ai_vague = data.get("is_vague", False)
    except Exception:
        pass

    # Heuristic tìm tên món nếu AI không bắt được
    if not ai_item:
        common_items = [
            "canh rong biển", "canh", "cơm sườn nướng", "cơm sườn", "trà đá đường", "trà đá",
            "trà sữa trân châu sợi", "trà sữa", "trà đào hạt chia", "trà đào",
            "combo gà rán 3 miếng", "gà rán", "khoai tây chiên vừa", "khoai tây chiên", "khoai tây",
            "pizza hải sản cỡ vừa", "pizza hải sản", "pizza", "coca cola lon", "coca"
        ]
        for it in common_items:
            if it in text_lower:
                ai_item = it
                break

    # Kiểm tra tính mơ hồ
    vague_phrases = ["thiếu món", "thiếu đồ", "giao thiếu rồi", "chưa đủ", "thiếu một món", "thiếu 1 món"]
    if any(vp in text_lower for vp in vague_phrases) and not ai_item:
        ai_vague = True

    return {
        "order_id": order_id,
        "missing_item": ai_item,
        "safety_risk": safety_risk,
        "is_vague": ai_vague
    }


def answer(text: str) -> dict:
    """Hàm xử lý chính của bài toán D1."""
    note("Bắt đầu xử lý khiếu nại")
    parsed = _extract_intent_and_entities(text)
    order_id = parsed["order_id"]
    missing_item = parsed["missing_item"]
    safety_risk = parsed["safety_risk"]
    is_vague = parsed["is_vague"]

    # NHÁNH 1: Tín hiệu an toàn nguy hiểm, đe dọa hoặc đòi hoàn 100% cả đơn -> Chuyển CSKH khẩn cấp
    if safety_risk:
        note("Phát hiện nguy cơ an toàn hoặc yêu cầu vượt hạn mức -> Chuyển CSKH")
        escalation = escalate_to_human(
            order_id=order_id or "UNKNOWN",
            reason="Yêu cầu bồi thường ngoài hạn mức chính sách hoặc có phản ánh an toàn/đe dọa",
            summary=text
        )
        msg = (
            f"Dạ hệ thống chân thành cáo lỗi cùng bạn về trải nghiệm không mong muốn này. "
            f"Đối với trường hợp của bạn, sự cố đã được chuyển ngay đến chuyên viên Chăm sóc Khách hàng "
            f"(Mã hỗ trợ: {escalation['ticket_id']}) để được thẩm định và liên hệ giải quyết trực tiếp. "
            f"Chuyên viên sẽ phản hồi bạn qua số điện thoại tài khoản trong thời gian sớm nhất."
        )
        return {"output": msg}

    # NHÁNH 2: Thiếu mã đơn hàng
    if not order_id:
        note("Thiếu mã đơn hàng -> Yêu cầu bổ sung")
        return {
            "output": "Dạ bạn vui lòng cung cấp Mã đơn hàng (ví dụ: ORD-101) để hệ thống kiểm tra danh sách món và hỗ trợ xử lý bồi thường ngay cho bạn ạ."
        }

    # Tra cứu đơn hàng
    order_info = get_order(order_id)
    if not order_info.get("found"):
        note(f"Không tìm thấy đơn {order_id}")
        return {
            "output": f"Dạ hệ thống không tìm thấy đơn hàng có mã '{order_id}'. Bạn vui lòng kiểm tra lại mã đơn trong mục Lịch sử đơn hàng giúp hệ thống nhé."
        }

    order = order_info["order"]
    items_in_order = [it["name"] for it in order.get("items", [])]
    items_str = ", ".join(items_in_order)

    # NHÁNH 3: Thu hẹp phạm vi khi không chắc (Nguyên tắc G10)
    if is_vague or not missing_item:
        note("Thiếu thông tin món cụ thể -> Áp dụng nguyên tắc G10 hỏi lại")
        return {
            "output": f"Dạ đơn hàng {order_id} của bạn gồm các món: [{items_str}]. Bạn vui lòng cho biết chính xác món nào bị thiếu để hệ thống hoàn tất bồi thường ngay ạ?"
        }

    # NHÁNH 4: Thẩm định điều kiện bồi thường bằng Code (Guardrail)
    note(f"Thẩm định món '{missing_item}' trên đơn {order_id}")
    claim_check = check_claim_limit(order_id, missing_item)

    if claim_check["is_valid"]:
        # Đạt điều kiện: Hoàn tiền tự động trong hạn mức
        allowed_amount = claim_check["allowed_amount"]
        item_confirmed = claim_check["item_name"]
        voucher = issue_refund_voucher(
            order_id=order_id,
            item_name=item_confirmed,
            amount=allowed_amount,
            reason="Bồi thường món thiếu trong hạn mức chính sách"
        )
        note(f"Bồi thường thành công {allowed_amount}đ cho món {item_confirmed}")
        msg = (
            f"Dạ hệ thống chân thành xin lỗi bạn về sự cố đơn hàng {order_id}. "
            f"Hệ thống đã xác nhận món '{item_confirmed}' bị thiếu và hoàn tiền bồi thường "
            f"{allowed_amount:,} VNĐ (tương ứng 100% giá trị món theo hóa đơn) vào ví của bạn "
            f"(Mã giao dịch: {voucher['voucher_code']}). Chúc bạn ngon miệng!"
        )
        return {"output": msg}
    else:
        # Vi phạm điều kiện (giá > 50k, không có trong đơn, hoặc tài khoản lạm dụng) -> Chuyển CSKH
        decision = claim_check.get("decision")
        reason = claim_check.get("reason", "")
        note(f"Vi phạm guardrail ({decision}) -> Chuyển người")

        if decision == "item_not_in_order":
            return {
                "output": f"Dạ trong đơn hàng {order_id} không có món '{missing_item}'. Đơn hàng của bạn chỉ gồm: [{items_str}]. Bạn vui lòng kiểm tra lại giúp hệ thống nhé."
            }

        escalation = escalate_to_human(
            order_id=order_id,
            reason=reason,
            summary=f"Khiếu nại món {claim_check.get('item_name', missing_item)} đơn {order_id}: {reason}"
        )
        msg = (
            f"Dạ hệ thống đã tiếp nhận khiếu nại món '{claim_check.get('item_name', missing_item)}' cho đơn hàng {order_id}. "
            f"Do {reason.lower()}, ca khiếu nại này đã được chuyển đến chuyên viên Chăm sóc Khách hàng "
            f"(Mã hỗ trợ: {escalation['ticket_id']}) để xem xét và xử lý giải pháp phù hợp nhất cho bạn."
        )
        return {"output": msg}
