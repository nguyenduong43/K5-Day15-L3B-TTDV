# Tóm tắt mô phỏng simulate-2@20261128-122441

Do `python run.py simulate` sinh ra — không sửa tay. Chép bảng sang `cost/cost-estimate.md`.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| khach_thinh_thoang | 33 | 1 | 243 | 46 | 1.0 | 2.6 |
| khach_van_phong | 16 | 2 | 492 | 93 | 2.0 | 5.4 |
| khach_lam_dung | 1 | 3 | 712 | 130 | 3.0 | 5.0 |

Tỉ lệ đạt dùng để tính: 26/26 (100%) — lượt run-3@20261128-115217

- Tỉ lệ đạt lấy từ lượt nhóm chọn: eval/run-3.csv (--rate-from). ⚠️ Lượt này chạy bằng google/gemini-3.5-flash, mô phỏng đo trên gemini-3.1-flash-lite — khác model.

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (1.000 người) | Chi phí / tháng — cơ sở (3.000 người) | Chi phí / tháng — cao (6.000 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| gemini-3.1-flash-lite (vào 0.25 · ra 1.5 $/1M) | $0.00018 (≈ 4 ₫) | $0.00018 (≈ 4 ₫) | $0.00013 (≈ 3 ₫) | $0.3365 (≈ 8.547 ₫) | $1.01 (≈ 25.641 ₫) | $2.02 (≈ 51.282 ₫) | $0.00034 (≈ 9 ₫) |
| openai/gpt-4o-mini (vào 0.15 · ra 0.6 $/1M) | $0.000087 (≈ 2 ₫) | $0.000087 (≈ 2 ₫) | $0.000064 (≈ 2 ₫) | $0.1662 (≈ 4.222 ₫) | $0.4987 (≈ 12.667 ₫) | $0.9974 (≈ 25.334 ₫) | $0.00017 (≈ 4 ₫) |

- Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt. Chi phí / câu hỏi đạt = chi phí / phiên ÷ số lượt hỏi trung bình mỗi phiên (1.4) ÷ tỉ lệ đạt — tỉ lệ đạt đo theo từng câu thử.
- Token đo trên model: gemini-3.1-flash-lite. Giá tính theo từng model trong bảng — model khác bộ tách token thì số token thật có thể lệch; ghi rõ "đo trên model X, tính giá model Y" trong cost/cost-estimate.md.
- Phiên lỗi (không tính vào trung bình): 0/50.
- Tỷ giá: 1 USD = 25.400 ₫ (Tỷ giá Vietcombank ngày 27/11/2026).
