# Tóm tắt mô phỏng simulate-1@20261128-121231

Do `python run.py simulate` sinh ra — không sửa tay. Chép bảng sang `cost/cost-estimate.md`.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| khach_thinh_thoang | 15 | 1 | 245 | 571 | 1.0 | 3.3 |
| khach_van_phong | 6 | 2 | 491 | 1130 | 2.0 | 4.2 |
| khach_lam_dung | 0 | 3 | — | — | — | — |

Tỉ lệ đạt dùng để tính: 26/26 (100%) — lượt run-3@20261128-115217

- Tỉ lệ đạt lấy từ lượt nhóm chọn: eval/run-3.csv (--rate-from).

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (1.000 người) | Chi phí / tháng — cơ sở (3.000 người) | Chi phí / tháng — cao (6.000 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| google/gemini-3.5-flash (vào 0.15 · ra 0.6 $/1M) | $0.00049 (≈ 12 ₫) | $0.00049 (≈ 12 ₫) | $0.00038 (≈ 10 ₫) | $0.8511 (≈ 21.617 ₫) | $2.55 (≈ 64.850 ₫) | $5.11 (≈ 129.701 ₫) | $0.00085 (≈ 22 ₫) |
| openai/gpt-4o-mini (vào 0.15 · ra 0.6 $/1M) | $0.00049 (≈ 12 ₫) | $0.00049 (≈ 12 ₫) | $0.00038 (≈ 10 ₫) | $0.8511 (≈ 21.617 ₫) | $2.55 (≈ 64.850 ₫) | $5.11 (≈ 129.701 ₫) | $0.00085 (≈ 22 ₫) |

- Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt. Chi phí / câu hỏi đạt = chi phí / phiên ÷ số lượt hỏi trung bình mỗi phiên (1.3) ÷ tỉ lệ đạt — tỉ lệ đạt đo theo từng câu thử.
- Token đo trên model: google/gemini-3.5-flash. Giá tính theo từng model trong bảng — model khác bộ tách token thì số token thật có thể lệch; ghi rõ "đo trên model X, tính giá model Y" trong cost/cost-estimate.md.
- Phiên lỗi (không tính vào trung bình): 29/50.
- Tỷ giá: 1 USD = 25.400 ₫ (Tỷ giá Vietcombank ngày 27/11/2026).
