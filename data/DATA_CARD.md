# Data card — Dữ liệu bản chạy thử D1 (Khiếu nại đơn thiếu món)

> Điền ở guide bước 2.4 (bản đầu ở CP2, đủ ở CP3). Ôn lại: ngày 6 · lab ngày 6. Chấm ở rubric R4.

## Dataset 1 · orders_db.json (Dữ liệu đơn hàng, chính sách & lịch sử tài khoản)

| Trường | Chi tiết |
|---|---|
| **Dùng để làm gì** | Cung cấp dữ liệu nền cho các công cụ trong `codebase/tools.py`: `get_order`, `get_policy`, `get_complaint_history`, `check_claim_limit` phục vụ bản chạy thử và bộ câu thử eval. |
| **Từ đâu** | Nhóm tự dựng có cấu trúc (dựa trên format hóa đơn thực tế của ShopeeFood / GrabFood) kết hợp chính sách bồi thường công khai của sàn TMĐT. |
| **Xử lý những bước gì** | Ẩn danh hoàn toàn thông tin cá nhân (chỉ dùng User ID mã hóa U1, U2, U3_ABUSE); tạo các trường hợp đơn hàng có món $\le 50k$ và $>50k$ để phục vụ kiểm thử boundary. |
| **Số dòng / số đoạn** | 4 đơn hàng mẫu đa dạng danh mục (cơm tấm, trà sữa, gà rán, pizza); 1 chính sách chuẩn bồi thường thiếu món; 3 hồ sơ lịch sử tài khoản. |
| **Phiên bản / ngày lấy** | v1.0 · Ngày 27/11/2026 |
| **Nhãn** | `synthetic` (dữ liệu giả lập phục vụ chạy thử) |
| **Giới hạn** | Số lượng đơn hàng giới hạn trong các kịch bản demo điển hình; không kết nối API ngân hàng hoặc ví điện tử thật. |

**Cách sinh & Kiểm soát:**
- Nhóm tự thiết kế tay (người kiểm: Đỗ Duy Tùng, Nguyễn Lâm Tùng).
- Dữ liệu này chỉ dùng làm môi trường chạy thử (environment runtime) cho agent, **không phải bằng chứng pain**. Bằng chứng pain được lưu riêng trong `evidence/data-mining.md`.
