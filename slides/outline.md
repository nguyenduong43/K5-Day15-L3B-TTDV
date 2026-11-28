# Dàn slide → lấy số từ file nào

> Làm ở guide bước 5.1. Luật: **không có bằng chứng thì không có slide** — mỗi trang ≥1 con số / trích dẫn có nguồn / kết quả đo.
> Xuất PDF thành `demo-slides.pdf` ở thư mục gốc repo, nộp tại CP4 14:30 Thứ Bảy 28/11. Nộp PDF, không nộp link.

| # | Trang | Có gì | Số lấy từ | Xong |
|---|---|---|---|---|
| 1 | Người dùng & pain | Ai · việc gì · chỗ đau + số và trích dẫn | `evidence/summary.md` | ☐ |
| 2 | Vì sao chọn bài này | Bảng impact rút gọn + hướng bị loại | `spec.md` §2 | ☐ |
| 3 | Giải pháp | Lát cắt một câu · sơ đồ · AI tự làm đến đâu, vì sao | `spec.md` §4 | ☐ |
| 4 | Demo live | 1 trường hợp thường + 1 trường hợp khó (lấy từ bộ câu thử); mạng hỏng → video dự phòng | `eval/benchmark.csv` | ☐ |
| 5 | **Đánh giá thế nào** | Dataset · bộ câu thử · metric · lượt 1 → lượt 2 so với chuẩn "đạt" (kèm run ID) · lỗi chính | `eval/README.md`, `eval/report.md` | ☐ |
| 6 | **Chi phí khi dùng thật** | Chi phí / task thành công · 3 kịch bản · so với impact | `cost/cost-estimate.md` | ☐ |
| 7 | Kết luận | Go / iterate / stop — dẫn số ở trang 1, 5, 6 | — | ☐ |
| 8 | Nếu có thêm 1 tuần | 2–3 việc, trỏ về lỗi còn lại / phản hồi người dùng | `eval/report.md` mục 4 · `validation/log.md` | ☐ |

## Nội dung trang 1, 2 và 8

### Trang 1 · Người dùng và vấn đề

**Khi đơn giao thiếu món, khách cần biết cách báo và bước xử lý tiếp theo.**

- **5/800 review ShopeeFood** và **2/1.200 review ứng dụng Grab** nêu rõ việc thiếu món. Nếu tính cả giao sai và hỗ trợ chậm, nhóm xác nhận được **24/800** và **7/1.200** trong hai mẫu review 1–3 sao. [Tổng hợp bằng chứng](../evidence/summary.md)
- **“shop làm thiếu món”** — ShopeeFood R323. Người viết kể đã báo hỗ trợ và phải chờ phản hồi. [Review đã ẩn danh](../evidence/data-mining.md)

### Trang 2 · Vì sao chọn D1

**D1 có thể xử lý trọn một ca bằng dữ liệu đơn và chính sách bồi thường.**

| Hướng | Chi phí hoặc thời gian | Quyết định |
|---|---|---|
| D1 · Xử lý thiếu món | P2 kể mất **5–15 phút để gửi yêu cầu**. P1 ước tính chờ **khoảng 30 phút để có phản hồi đầu tiên**. | Chọn. Đối chiếu được đơn, giá món và điều kiện xử lý. |
| D2 · Đặt đơn nhóm | Ước tính **20–30 phút** để gom món, tính tiền và kiểm ràng buộc. | Giỏ hàng có nhiều ràng buộc về ngân sách và ăn uống. |
| D3 · Trả hàng trên sàn | Ước tính **2–5 ngày** chờ xử lý. | Quy trình cần bằng chứng và duyệt qua nhiều bên. |

**Impact minh họa:** 3.000 ca/tháng × 70% đủ điều kiện × 10 phút CSKH/ca ≈ **350 giờ CSKH/tháng**, theo kịch bản tự ước tính. Các thời gian P1 và P2 kể là hai bước khác nhau. [Bảng impact](../spec.md) · [Tổng hợp phỏng vấn](../evidence/summary.md)

### Trang 8 · Nếu có thêm một tuần

**Ưu tiên giúp khách hiểu mình cần làm gì sau khi gửi báo thiếu món.**

1. **Làm rõ phản hồi.** Hiển thị phương án xử lý, bên phụ trách và việc khách cần làm tiếp. Kiểm lại bằng cách hỏi người thử tự giải thích kết quả trên cùng phiên bản demo. [Tổng hợp các điểm cần xem lại](../validation/log.md)
2. **Kiểm lại ca ngoài phạm vi.** Lượt 1 đạt **4/6 câu từ chối**. Thử lại các ca giao trễ, giao sai và đơn đã hủy với cách diễn đạt mới để kiểm việc hướng dẫn đúng kênh hoặc chuyển CSKH. [Báo cáo đánh giá](../eval/report.md)
3. **Kiểm lại impact.** Thu số ca thiếu món, tỷ lệ đủ điều kiện và thời gian xử lý thực tế để cập nhật kịch bản 350 giờ/tháng. [Bảng impact](../spec.md)

> **Ghi chú khi ráp slide:** đối chiếu phiên bản dùng thử trước khi dùng tên nút, thông báo và thời gian thao tác trong log. Bản web hiện tại có nút “Kiểm tra yêu cầu”, còn ca `ORD-101` trong kết quả lượt 1 ghi hoàn 15.000 đồng. [Giao diện](../codebase/web/index.html) · [Kết quả lượt 1](../eval/run-1.csv)

**Trước khi lên:** tải repo về một máy khác (hoặc thư mục mới), chạy theo mục "Chạy trong 3 phút" của `README.md` · `.env` có trên máy demo, đã gọi thử 1 câu trong vòng 1 giờ trước giờ demo · video dự phòng mở được bằng cửa sổ ẩn danh · biết bản chạy thử sẽ làm gì với **1 câu thử lạ** của giám khảo.

Ai nói trang nào (mỗi người ≥1 phần):

| Trang | Người nói |
|---|---|
| | |
