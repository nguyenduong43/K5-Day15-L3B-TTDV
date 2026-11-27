# Tổng hợp bằng chứng pain

> Điền ở guide bước 1.2, xong trước **CP3 10:00 Thứ Bảy 28/11**. Chấm ở rubric R1.
> Ba nguồn ngang nhau — tối thiểu **≥1 nguồn đạt ngưỡng**. Mạnh nhất: đào data ra insight → hỏi người dùng để kiểm lại (hoặc ngược lại).

## 1. Nguồn đã dùng

| Nguồn | Đạt ngưỡng? | File |
|---|---|---|
| Đào data (x/N, %, cách đếm chạy lại được, ≥5 ví dụ) | ☑ | [Dữ liệu review](data-mining.md) |
| Phỏng vấn (≥3 người ngoài nhóm, đúng người dùng) | ☐ Có 2 ca thuộc D1, chờ xác nhận thời điểm. Ca P3 là mua hàng qua sàn. | [P1](interviews/P1.md), [P2](interviews/P2.md), [P3](interviews/P3.md) |
| Khảo sát (≥20 người ngoài nhóm, đúng người dùng) | ☐ | `evidence/survey/` |

## 2. Số chính

- **Đào data:** số dưới đây là mức tối thiểu tìm thấy sau sàng lọc và đọc xác nhận. [Cách đếm và 25 ví dụ](data-mining.md)
  - ShopeeFood (review 1–3 sao, 01/07–26/11/2026). **24/800 (3,00%)** có ít nhất một vấn đề. Trong đó **5/800 (0,63%)** thiếu món, **4/800 (0,50%)** giao sai món hoặc sai đơn và **18/800 (2,25%)** hỗ trợ hoặc hoàn tiền chậm.
  - GrabFood (review 1–3 sao của ứng dụng Grab, 12/09–26/11/2026, mẫu số gồm các dịch vụ khác của Grab). **7/1.200 (0,58%)** có ít nhất một vấn đề. Trong đó **2/1.200 (0,17%)** thiếu món, **1/1.200 (0,08%)** giao sai món hoặc sai đơn và **5/1.200 (0,42%)** hỗ trợ hoặc hoàn tiền chậm.
- **Phỏng vấn:** 2 người kể về thiếu món khi đặt qua app giao đồ ăn. Cả hai kể nhận voucher. Thời điểm xảy ra của hai ca còn cần xác nhận để biết có thuộc tháng vừa qua hay không.
- **Khảo sát:** chưa dùng nguồn này.

Phỏng vấn nhiều vai thì đếm theo từng vai, không cộng chung.

| | Vai | Gặp pain? | Số lần / 1 tháng qua | Lần gần nhất mất | Đang xoay xở bằng |
|---|---|---|---|---|---|
| P1 | Khách ShopeeFood | Thiếu bún ăn kèm nem nướng | Chưa rõ | Báo ngay. Phản hồi khoảng 30 phút. Phương án được đưa ra trong vài phút theo lời kể, mốc bắt đầu chưa rõ. | Chụp ảnh và đánh giá 1 sao. Nhận voucher 10.000 đồng lần sau. |
| P2 | Khách GrabFood | Thiếu rau ăn kèm | Nói chưa gặp lại trong tháng qua. Chưa rõ ngày xảy ra ca được kể. | Khoảng 5–15 phút để gửi yêu cầu trên app ở những lần có báo. Chờ phản hồi và xử lý được mô tả là ngắn, chưa có số cụ thể. | Gọi tài xế, báo trên app kèm ảnh hoặc bỏ qua tùy lần. Nhận voucher ở ca có xử lý. |
| P3 | Khách mua bánh qua Shopee | Nhận 5 cái, tổng ước tính dưới 100 g so với 200 g đã đặt. Ca tham khảo ngoài D1. | Chưa rõ | Chưa rõ thời gian chờ. Theo lời kể, người bán chưa phản hồi. | Nhắn người bán kèm ảnh rồi đánh giá 1 sao. |

## 3. ≥5 trích dẫn hoặc ví dụ nguyên văn (có nguồn, bỏ tên)

Mã và ngày của các review đối chiếu được ở mục 4. [Dữ liệu review](data-mining.md)

1. “Quán giao món thiếu” — ShopeeFood R064, 07/11/2026.
2. “nó phản hồi lâu kinh khủng” — ShopeeFood R139, 22/10/2026.
3. “shop làm thiếu món” — ShopeeFood R323, 23/09/2026.
4. “đợi hơn 7 ngày” — ShopeeFood R320, 24/09/2026.
5. “thiếu 2 miếng gà” — GrabFood R049, 21/11/2026.
6. “Chắc nửa tiếng là có phản hồi” — khách ShopeeFood. [P1](interviews/P1.md)
7. “Các thao tác trên ứng dụng nhìn chung khá suôn sẻ, không gặp lỗi hay phải làm lại bước nào.” — khách GrabFood. [P2](interviews/P2.md)

## 4. Các nguồn có khớp nhau không

Review và hai lời kể đều ghi nhận thiếu món trên ShopeeFood và GrabFood. R064, R049, P1 và P2 đều mô tả phương án voucher. Tốc độ xử lý khác nhau giữa các ca. Một số review mô tả chờ lâu. P1 ước tính phản hồi sau khoảng nửa tiếng, còn P2 mô tả xử lý tự động trong thời gian ngắn và thao tác trên app suôn sẻ. P2 cũng có lúc bỏ qua vì phần thiếu nhỏ và ngại làm phiền tài xế. P3 phản ánh một ca thiếu hàng qua sàn Shopee và được giữ làm tham khảo ngoài D1.

## 5. Kết luận

Giả thuyết ở `evidence/hypothesis.md`: **phải đổi theo bằng chứng hiện có**. Các ca đã xác nhận qua sàng lọc review chưa ủng hộ ngưỡng 25%. Tỷ lệ 3,00% và 0,58% là mức tối thiểu tìm thấy trong hai mẫu review 1–3 sao, gồm nhiều loại phản ánh. Điều kiện phỏng vấn **ít nhất 2/3 người chờ quá 12 giờ** chưa đủ dữ liệu để kiểm tra. Cần xác nhận ngày xảy ra và thời gian xử lý của P1, P2, rồi bổ sung người đúng phạm vi D1 có ca xảy ra trong tháng qua cho đủ ba. [Giả thuyết ban đầu](hypothesis.md)

## Lịch hẹn (dùng cho CP2 — chỉ ghi vai và giờ, không tên)

| Vai | Giờ hẹn | Đã xong? |
|---|---|---|
| Khách đặt đồ ăn qua ShopeeFood (P1) | Dự kiến 20:00 ngày 27/11/2026 | Đã có lời kể, chưa ghi giờ thực tế |
| Khách đặt đồ ăn qua GrabFood (P2) | Dự kiến 20:30 ngày 27/11/2026 | Đã có lời kể, chưa ghi giờ thực tế |
| Khách mua bánh qua Shopee (P3) | Dự kiến 08:30 ngày 28/11/2026 | Đã có lời kể, dùng làm tham khảo ngoài D1 |
