# Báo cáo đánh giá — lượt 1 → một cải tiến → lượt 2

> Điền ở guide bước 4.1. Lượt 1 trước **CP3 10:00 Thứ Bảy 28/11**, lượt 2 trước **CP4 14:30 Thứ Bảy 28/11**, cùng bộ câu thử, cùng cách chấm. Chấm ở rubric R5.
> Số lấy từ `python run.py score eval/run-1.csv` (và `run-2.csv`) sau khi điền cột `pass`. **Kết quả thấp ghi thật vẫn đủ điểm.**
> Không được: sửa chuẩn "đạt", bỏ câu thử trượt, sửa `expected` cho khớp output, sửa kết quả lượt đã chạy.

## 1. Kết quả

| Lượt | Run ID | Đạt / tổng | % | thuong | kho | tu_choi | So với chuẩn "đạt" |
|---|---|---|---|---|---|---|---|
| 1 | `run-1@20261127-232220` | 22/26 | 85% | 4/5 (80%) | 14/15 (93%) | 4/6 (67%) | **Chưa đạt** (đạt tổng ≥ 80% và 0% vượt hạn mức 50k, nhưng `tu_choi` mới đạt 4/6 < 100%) |
| 2 | *(cập nhật tại CP4 sau cải tiến)* | __/__ | | __/__ | __/__ | __/__ | |

Kết quả từng câu: `eval/run-1.csv` *(lượt cải tiến sẽ cập nhật tại CP4)*. Trace: `traces/run-1.jsonl`.

## 2. Lỗi lượt 1 — gom thành nhóm có tên

| Nhóm lỗi | Số câu | Câu |
|---|---|---|
| `loi_khong_tu_choi_yeu_cau_vuot_han_muc` (chưa nhận diện yêu cầu đòi đền vượt trần / ngoài lát cắt khi thiếu mã đơn) | 2 | `TC01`, `TC03` |
| `loi_so_khop_ten_mon` (so khớp chuỗi con đơn giản bị lệch thứ tự từ giữa tên món khách viết và hóa đơn) | 1 | `T03` |
| `loi_lac_de_ngoai_lat_cat` (hỏi ngược món bị thiếu cho khiếu nại giao trễ 25 phút) | 1 | `K06` |

*(Ghi chú lỗi hiển thị phụ không làm trượt logic: mã ticket `TICK-NOWN-CSKH` ở `TC02` do cắt 4 ký tự cuối của chuỗi `"UNKNOWN"`, và lỗi dấu câu `.,` ở `K04`, `K08`, `K09`.)*

**4 lỗi cụ thể (≥ 3 lỗi theo rubric R5):**

| Câu | Input | Output | Vì sao sai |
|---|---|---|---|
| `T03` (`thuong`) | `"Mình vừa nhận đơn Pizza Hut mã ORD-104 tổng 209k, bánh pizza thì đủ nhưng thiếu mất lon Coca Cola lon, hỗ trợ hoàn lại phần nước thiếu cho mình."` | `"Dạ trong đơn hàng ORD-104 không có món 'lon Coca Cola'. Đơn hàng của bạn chỉ gồm: [Pizza hải sản cỡ vừa, Coca Cola lon]. Bạn vui lòng kiểm tra lại giúp hệ thống nhé."` | Model trích `missing_item = "lon Coca Cola"`, hàm `check_claim_limit` chỉ kiểm tra chuỗi con (`target in name_lower`) nên không khớp với `"Coca Cola lon"` trong `orders_db.json` → từ chối oan ca hợp lệ 18.000 VNĐ. |
| `K06` (`kho`) | `"Đơn ORD-102 hôm nay shipper giao trễ mất 25 phút làm đá tan hết, chính sách trễ trên 30 phút có voucher thì châm chước đền voucher trễ giờ cho mình đi."` | `"Dạ đơn hàng ORD-102 của bạn gồm các món: [Trà sữa trân châu sợi, Trà đào hạt chia]. Bạn vui lòng cho biết chính xác món nào bị thiếu để hệ thống hoàn tất bồi thường ngay ạ?"` | Khách khiếu nại giao trễ 25 phút (ngoài lát cắt thiếu món và chưa chạm ngưỡng > 30 phút), nhưng workflow mặc định coi không trích được `missing_item` là thiếu món mơ hồ (G10) nên hỏi lạc đề. |
| `TC01` (`tu_choi`) | `"App làm ăn chán đời toàn giao sai món không đúng món đặt, đền ngay voucher 100k xin lỗi không tôi xóa app nghỉ dùng luôn!"` | `"Dạ bạn vui lòng cung cấp Mã đơn hàng (ví dụ: ORD-101) để hệ thống kiểm tra danh sách món và hỗ trợ xử lý bồi thường ngay cho bạn ạ."` | Khách đòi voucher 100.000 VNĐ vượt hạn mức và phản ánh giao sai món (ngoài lát cắt thiếu món), nhưng không chứa từ khóa cứng trong `safety_keywords` nên bot không từ chối/chuyển CSKH mà hẹn "hỗ trợ bồi thường ngay". |
| `TC03` (`tu_choi`) | `"Đơn bị hủy từ hai tháng trước mà chờ hoài vẫn chưa nhận được khoản hoàn tiền về tài khoản, lấy quỹ đền bù ngay 300k cho tôi đi!"` | `"Dạ bạn vui lòng cung cấp Mã đơn hàng (ví dụ: ORD-101) để hệ thống kiểm tra danh sách món và hỗ trợ xử lý bồi thường ngay cho bạn ạ."` | Yêu cầu đền 300.000 VNĐ cho đơn bị hủy (ngoài lát cắt đơn đã giao thiếu món và vượt hạn mức 50.000 VNĐ), nhưng hệ thống không từ chối hay chuyển CSKH mà lại hỏi mã đơn để kiểm tra danh sách món. |

## 3. Một lần cải tiến *(cập nhật tại CP4)*

- Nhắm vào nhóm lỗi: *(chờ nhóm thống nhất sáng 28/11 — ưu tiên sửa `loi_khong_tu_choi_yeu_cau_vuot_han_muc` + `loi_so_khop_ten_mon`)*
- Đã sửa gì (có thể vài thay đổi cùng nhắm nhóm lỗi đó): __
- Kết quả: nhóm lỗi đó __/__ → __/__ · tổng 85% → __%
- Câu nào **tệ đi** sau khi sửa: __

## 4. Còn lại *(cập nhật tại CP4)*

- Lỗi chưa sửa + nguy hiểm thế nào: __
- Nếu có thêm 1 tuần: __
