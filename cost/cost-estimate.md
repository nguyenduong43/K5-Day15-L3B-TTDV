# Chi phí khi dùng thật

> Điền ở guide bước 4.2, nộp ở CP4 14:30 Thứ Bảy 28/11. Ôn lại: ngày 13, ngày 1, ngày 14 · lab ngày 13, lab ngày 14. Chấm ở rubric R6.
> Số **không điền tay**: điền `cost/personas.yaml` → `python run.py simulate` → chép bảng trong `cost/simulate-N-summary.md` vào đây.
> Lúc build dùng gói miễn phí vẫn tính theo **giá gói trả phí** — đây là chi phí cho lúc đưa vào dùng thật.

## 1. Đầu vào

- **Persona** (`cost/personas.yaml`): 3 nhóm người dùng dựa trên nghiên cứu thực tế tại `spec.md` §1 và §2:
  - `khach_thinh_thoang` (share 60%): 1 phiên/người/tháng, 1 lượt hỏi/phiên. Nguồn: `spec.md` §2 — Khách thỉnh thoảng đặt 2–4 đơn/tháng, khiếu nại 1 lần / vài tháng (làm tròn 1 lần/tháng vào hệ thống khi gặp sự cố).
  - `khach_van_phong` (share 35%): 2 phiên/người/tháng, 2 lượt hỏi/phiên. Nguồn: `spec.md` §2 — Khách văn phòng đặt thường xuyên 15–20 đơn/tháng, khiếu nại 1–2 lần/tháng.
  - `khach_lam_dung` (share 5%): 4 phiên/người/tháng, 3 lượt hỏi/phiên. Nguồn: `spec.md` §2 — Nhóm tài khoản có dấu hiệu khiếu nại bất thường/nhiều lần (4–5 lần/tháng).
- **Số người dùng thật** 3 kịch bản: thấp **1.000** · cơ sở **3.000** · cao **6.000** người gặp sự cố khiếu nại/tháng. Nguồn: `spec.md` §1 & §2 — Quy mô 100.000 đơn hàng/tháng với tỷ lệ sự cố thiếu/sai món 3% (từ 2.000 review Google Play: ShopeeFood 3,00%, GrabFood 0,58%), tương đương 3.000 ca khiếu nại/tháng ở kịch bản cơ sở. Thấp (1.000) và cao (6.000) ước tính theo biến động volume đơn.
- **Giá** ≥2 mức model (có link + ngày xem):
  - `gemini-3.1-flash-lite`: vào **$0.25** / ra **$1.50** trên 1 triệu token (Nguồn: https://ai.google.dev/pricing · xem 28/11/2026).
  - `openai/gpt-4o-mini`: vào **$0.15** / ra **$0.60** trên 1 triệu token (Nguồn: https://openai.com/api/pricing · xem 28/11/2026).
- **Tỉ lệ đạt** dùng để tính: **26/26 (100%)** — lấy từ lượt cải tiến `eval/run-3.csv` (`run-3@20261128-115217`).
- Đo token trên model `gemini-3.1-flash-lite`, tính giá model `gemini-3.1-flash-lite` và `openai/gpt-4o-mini`. Tỷ giá: 1 USD = 25.400 ₫ (Vietcombank 27/11/2026).

## 2. Kết quả mô phỏng

Lượt mô phỏng: `cost/simulate-2.csv` · run ID `simulate-2@20261128-122441` · **50 phiên** (seed 42) · **Phiên lỗi: 0/50**.

*(Chép chính xác từ bảng tự động sinh `cost/simulate-2-summary.md`)*

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| khach_thinh_thoang | 33 | 1 | 243 | 46 | 1.0 | 2.6 |
| khach_van_phong | 16 | 2 | 492 | 93 | 2.0 | 5.4 |
| khach_lam_dung | 1 | 3 | 712 | 130 | 3.0 | 5.0 |

Tỉ lệ đạt dùng để tính: **26/26 (100%)** — lượt `run-3@20261128-115217` (`eval/run-3.csv`).

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (1.000 người) | Chi phí / tháng — cơ sở (3.000 người) | Chi phí / tháng — cao (6.000 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| gemini-3.1-flash-lite (vào 0.25 · ra 1.5 $/1M) | $0.00018 (≈ 4 ₫) | $0.00018 (≈ 4 ₫) | $0.00013 (≈ 3 ₫) | $0.3365 (≈ 8.547 ₫) | $1.01 (≈ 25.641 ₫) | $2.02 (≈ 51.282 ₫) | $0.00034 (≈ 9 ₫) |
| openai/gpt-4o-mini (vào 0.15 · ra 0.6 $/1M) | $0.000087 (≈ 2 ₫) | $0.000087 (≈ 2 ₫) | $0.000064 (≈ 2 ₫) | $0.1662 (≈ 4.222 ₫) | $0.4987 (≈ 12.667 ₫) | $0.9974 (≈ 25.334 ₫) | $0.00017 (≈ 4 ₫) |

- *Chi phí / task thành công* = chi phí / phiên ÷ tỉ lệ đạt (100%) = **$0.00018** (≈ **4 ₫**).
- *Chi phí / tháng ở quy mô cơ sở (3.000 ca khiếu nại)* = **$1.01** (≈ **25.641 ₫/tháng** với Gemini) và **$0.50** (≈ **12.667 ₫/tháng** với GPT-4o-mini).

## 3. So với impact

- **Impact / tháng** (`spec.md` §2): Tiết kiệm **~350 giờ CSKH/tháng** (tương đương 21.000 phút lao động nhân sự CSKH cho 3.000 ca khiếu nại, giảm thời gian xử lý khiếu nại từ 24h–48h xuống **dưới 5 giây**). Nếu tính lương CSKH trung bình 30.000 ₫/giờ, giá trị tiết kiệm tương đương **~10.500.000 ₫ – 21.000.000 ₫/tháng**.
- **Chi phí AI / tháng** (cơ sở, model `gemini-3.1-flash-lite`): **25.641 ₫/tháng** (~$1.01 USD/tháng). Chi phí / người / tháng: **~9 ₫/người**.
- **Kết luận một dòng — đáng làm không:** **CỰC KỲ ĐÁNG LÀM** — Chi phí vận hành AI hoàn toàn không đáng kể (~25.000 ₫/tháng cho 3.000 ca) so với giá trị tiết kiệm được hơn 350 giờ nhân sự CSKH (~10–20 triệu đồng/tháng), mang lại ROI hàng trăm lần và giải quyết ngay lập tức cho khách hàng.

## 4. Phân tích độ nhạy & Mở rộng

- **So sánh 2 model:** `gpt-4o-mini` có chi phí rẻ hơn gần một nửa so với `gemini-3.1-flash-lite` (12.667 ₫/tháng so với 25.641 ₫/tháng) do giá output rẻ hơn ($0.60 vs $1.50/1M token). Cả hai model đều có chi phí dưới 30.000 ₫/tháng, hoàn toàn khả thi trong thực tế.
- **Tối ưu hóa token:** Do sử dụng kiến trúc Fixed Workflow với trích xuất thực thể gọn và bộ chặn Guardrail bằng code Python thuần (`check_claim_limit`), hệ thống chỉ gọi LLM trung bình 1.0–2.0 lần mỗi phiên, token vào chỉ ~243–492 token/phiên, giúp chi phí giữ ở mức tối thiểu.
- **Quy mô nào thì bài toán còn đáng làm:** Ngay từ quy mô thấp (1.000 ca/tháng, chi phí AI ~8.500 ₫/tháng) cho đến quy mô lớn (hơn 100.000 ca/tháng, chi phí AI ~850.000 ₫/tháng), giải pháp đều đem lại lợi ích kinh tế vượt trội so với tuyển dụng thêm nhân sự CSKH thủ công.
