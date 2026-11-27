# Đào data — cách đếm và kết quả

> Điền ở guide bước 1.2. Ôn lại: ngày 2, ngày 6 · lab ngày 2, lab ngày 6.
> Không đào data thì xoá file này. Script / công thức đếm để trong repo (vd `evidence/count.py` hoặc ghi công thức Sheets ngay dưới), người khác chạy lại phải ra cùng số.
> Repo chỉ chứa số đã tổng hợp và vài dòng ví dụ — không chép lại nguyên file data.

## 1. Cách đếm — viết TRƯỚC khi chạy

- Data dùng: `raw-reviews-shopeefood-800.csv`, gồm review đăng từ 01/07 đến 26/11/2026, thu lúc 17:24 ngày 27/11/2026. `raw-reviews-grab-1200.csv`, gồm review đăng từ 12/09 đến 26/11/2026, thu lúc 17:41 cùng ngày. Giờ thu là giờ Việt Nam. [ShopeeFood trên Google Play](https://play.google.com/store/apps/details?id=com.deliverynow) · [Grab trên Google Play](https://play.google.com/store/apps/details?id=com.grabtaxi.passenger)
- Đếm gì: số review phản ánh thiếu món, giao sai món/đơn hoặc chậm gửi khiếu nại, nhận hỗ trợ hay hoàn tiền · trên tập nào: review công khai có chữ, 1–3 sao, lấy theo thứ tự mới nhất do Google Play trả về với thiết lập Việt Nam · lọc gì: loại mã review trùng và kiểm tra ngữ cảnh trước khi gắn nhãn. Với Grab, chỉ gắn nhãn cho phản ánh về đơn đồ ăn.
- **Mẫu số là gì:** 800 review ShopeeFood (706 một sao, 46 hai sao, 48 ba sao) và 1.200 review của ứng dụng Grab (1.085 một sao, 61 hai sao, 54 ba sao). Mỗi mẫu số gồm cả review về chủ đề khác. *(lỗi hay gặp nhất là mẫu số sai)*
- Script / công thức: [collect_reviews.py](collect_reviews.py) tạo mẫu và điền cột `nhan_goi_y`. Đếm ô có nhãn bằng `=COUNTIF(F2:F801,"?*")` cho ShopeeFood và `=COUNTIF(F2:F1201,"?*")` cho Grab. Đọc xác nhận 31 ứng viên ShopeeFood, giữ 15, rồi rà 95 dòng bằng từ khóa mở rộng và giữ thêm 9. Với Grab, đọc 18 ứng viên và 49 dòng bổ sung khớp cả từ khóa đồ ăn lẫn sự cố, xác nhận 7. Tính phần trăm bằng `x / N × 100` theo từng mẫu. Gộp các mã và bỏ mã lặp khi đếm dòng tổng.

## 2. Đọc trước, đếm sau

Đã đọc 30 dòng đầu của mẫu ShopeeFood đã xếp theo mức ưu tiên và từ điển cột. Các *kiểu* hành vi thấy được (trước khi định nghĩa thứ cần đếm):
- Khách đã nhận đơn nhưng thiếu món hoặc phần đã đặt, hoặc nhận món/đơn khác với thứ đã đặt. Các ca tự đặt nhầm hoặc sai địa chỉ được bỏ khỏi hai nhãn này.
- Khách gặp khó khi gửi khiếu nại, chờ phản hồi sau khi liên hệ, hoặc chờ hoàn tiền. Các ca chỉ chờ tài xế giao hoặc chỉ bị từ chối hoàn tiền được bỏ khỏi nhãn hỗ trợ chậm.

## 3. Kết quả

| Đếm gì | x / N | % | Ghi chú |
|---|---|---|---|
| ShopeeFood · Thiếu món | 5/800 | 0,63% | R064, R086, R216, R323, R556 |
| ShopeeFood · Giao sai món hoặc đơn | 4/800 | 0,50% | R216, R314, R556, R586 |
| ShopeeFood · Hỗ trợ hoặc hoàn tiền chậm | 18/800 | 2,25% | R003, R056, R139, R172, R285, R320, R323, R354, R370, R386, R406, R413, R460, R488, R510, R554, R750, R787 |
| **ShopeeFood · Có ít nhất một vấn đề** | **24/800** | **3,00%** | Đếm mỗi mã một lần. |
| GrabFood · Thiếu món | 2/1.200 | 0,17% | R049, R272 trong mẫu Grab |
| GrabFood · Giao sai món hoặc đơn | 1/1.200 | 0,08% | R100 trong mẫu Grab |
| GrabFood · Hỗ trợ hoặc hoàn tiền chậm | 5/1.200 | 0,42% | R013, R049, R489, R680, R966 trong mẫu Grab |
| **GrabFood · Có ít nhất một vấn đề** | **7/1.200** | **0,58%** | Đếm mỗi mã một lần. Mẫu số gồm cả các dịch vụ khác của Grab. |

Ghi dạng "x/N (y%)". "Nhiều bạn…" không phải số.

## 4. ≥5 ví dụ cụ thể (mã dòng / mã đã ẩn danh, không đoán ai là ai)

1. **ShopeeFood R003 · 24/11/2026 · 1 sao.** Khách kể đã chờ hai tháng vẫn chưa nhận khoản hoàn tiền cho đơn bị hủy.
2. **ShopeeFood R064 · 07/11/2026 · 1 sao.** “Quán giao món thiếu”. Khách kể nhận mã giảm giá sau khi báo thiếu món.
3. **ShopeeFood R086 · 01/11/2026 · 1 sao.** Khách kể có đơn tới nơi nhưng thiếu đồ.
4. **ShopeeFood R139 · 22/10/2026 · 1 sao.** “nó phản hồi lâu kinh khủng”. Khách kể phải chờ khi gửi báo cáo trên app.
5. **ShopeeFood R216 · 09/10/2026 · 1 sao.** Khách nói gặp giao sai hoặc thiếu đồ ăn nhiều lần gần đây.
6. **ShopeeFood R314 · 25/09/2026 · 1 sao.** “toàn giao sai món”. Khách phàn nàn giao sai lặp lại.
7. **ShopeeFood R320 · 24/09/2026 · 1 sao.** “đợi hơn 7 ngày”. Khách kể thời gian chờ được hoàn tiền.
8. **ShopeeFood R323 · 23/09/2026 · 1 sao.** “shop làm thiếu món”. Khách kể đã yêu cầu hỗ trợ rồi chờ phản hồi.
9. **ShopeeFood R354 · 19/09/2026 · 1 sao.** Khách đặt trà sữa, yêu cầu hoàn tiền và kể đã chờ mà chưa có câu trả lời.
10. **ShopeeFood R370 · 17/09/2026 · 1 sao.** Sau khi đơn bị hủy, khách phàn nàn phải đợi 7–14 ngày để được hoàn tiền.
11. **ShopeeFood R386 · 14/09/2026 · 1 sao.** Khách kể ba tháng sau khi quán hủy đơn vẫn chưa nhận tiền hoàn.
12. **ShopeeFood R406 · 12/09/2026 · 1 sao.** Khách kể app tự hủy đơn và phải chờ bảy ngày để được hoàn tiền.
13. **ShopeeFood R413 · 12/09/2026 · 1 sao.** Khách đã trả tiền trước, đơn bị hủy vì chưa có tài xế và tiền về sau vài ngày.
14. **ShopeeFood R460 · 03/09/2026 · 1 sao.** Khách mô tả phải qua nhiều bước mới gửi được khiếu nại.
15. **ShopeeFood R488 · 28/08/2026 · 1 sao.** Khách kể gần một giờ sau mới được tổng đài liên hệ về yêu cầu hủy đơn.
16. **ShopeeFood R510 · 25/08/2026 · 1 sao.** Khách muốn hủy đơn và kể đã liên hệ cả tiếng mà chưa gặp ai hỗ trợ.
17. **ShopeeFood R556 · 16/08/2026 · 1 sao.** Khách nhận sai đơn, thiếu món và hỏi app hay quán có trách nhiệm xử lý.
18. **ShopeeFood R586 · 12/08/2026 · 1 sao.** Khách nói nhận sai món dù vẫn bị tính đủ tiền.
19. **GrabFood R013 · 25/11/2026 · 1 sao.** “khiếu nại thì k phản hồi”. Khách kể đơn đồ ăn đã hủy mà vẫn bị yêu cầu thanh toán.
20. **GrabFood R049 · 21/11/2026 · 1 sao.** Combo “thiếu 2 miếng gà”. Khách có video mở đơn và kể đã chờ hỗ trợ, sau đó nhận voucher kèm điều kiện.
21. **GrabFood R100 · 14/11/2026 · 1 sao.** “giao sai đơn rồi”. Khách muốn có chỗ góp ý cho đơn thứ hai trong đơn gộp.
22. **GrabFood R272 · 27/10/2026 · 1 sao.** “quán giao thiếu món” là một trong những sự cố khách kể đã gặp trong tháng.
23. **GrabFood R489 · 11/10/2026 · 1 sao.** Khách đã trả tiền đơn đồ ăn chưa được giao và gửi khiếu nại mà chưa thấy Grab phản hồi.
24. **GrabFood R680 · 29/09/2026 · 1 sao.** “vẫn chưa hoàn tiền”. Khách kể đặt GrabFood ngày 23/09, chưa nhận đơn và đến 29/09 chưa thấy tiền về.
25. **GrabFood R966 · 15/09/2026 · 1 sao.** Khách kể chưa nhận đồ ăn dù đã trả tiền, rồi nhắn qua app mà chưa được phản hồi.

## 5. Giới hạn của data

Data cho biết người ta **làm gì**, không cho biết **vì sao**. Thiếu gì, lệch về phía nào: sàng lọc từ khóa có thể bỏ sót cách diễn đạt khác. Chọn review 1–3 sao khiến mẫu nghiêng về người phàn nàn. Mẫu Grab chứa nhiều loại dịch vụ, nên mỗi tỷ lệ chỉ mô tả mẫu của chính ứng dụng đó. Để tính tỷ lệ thiếu món trong tất cả đơn hàng cần số liệu đơn hàng.
→ Kiểm lại bằng phỏng vấn / khảo sát nào: phỏng vấn ít nhất 3 người ngoài nhóm từng nhận đơn thiếu món trong tháng qua. Hỏi họ đã báo qua đâu, phải gửi bằng chứng gì, chờ bao lâu và cuối cùng nhận được gì.
