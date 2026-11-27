# Data card — Dữ liệu bản chạy thử & đánh giá bài toán D1 (Khiếu nại đơn thiếu món)

> Điền ở guide bước 2.4 (bản đầu ở CP2, đủ ở CP3). Ôn lại: ngày 6 · lab ngày 6. Chấm ở rubric R4.
> Một trang. Mỗi dataset một mục. Không commit dữ liệu cá nhân thật hay nguyên file thu thập thô lên repo.

---

## Dataset 1 · `data/orders_db.json` (Đơn hàng mẫu & lịch sử khiếu nại tài khoản)

| Trường | Chi tiết |
|---|---|
| **Dùng để làm gì** | Nguồn tra cứu cho các công cụ trong `codebase/tools.py`: `get_order(order_id)`, `get_complaint_history(user_id)` và đối soát trong `check_claim_limit(order_id, item_name)` phục vụ bản chạy thử và bộ câu thử `eval/benchmark.csv`. |
| **Từ đâu** | Nhóm tự dựng có cấu trúc dựa trên định dạng hóa đơn đặt đồ ăn thực tế (ShopeeFood / GrabFood), không sử dụng dữ liệu BTC cấp của Track A. |
| **Xử lý những bước gì** | Ẩn danh 100% thông tin cá nhân (chỉ dùng mã người dùng `U1`, `U2`, `U3_ABUSE` và mã đơn `ORD-101` đến `ORD-104`); thiết kế dải giá món bao phủ cả vùng trong hạn mức (`10.000đ`–`42.000đ` ≤ `50.000đ`) và vượt hạn mức (`65.000đ`–`169.000đ` > `50.000đ`), kèm tài khoản bình thường (`0–1` lần/tháng) và tài khoản lạm dụng (`4` lần/tháng ≥ ngưỡng `3`). |
| **Số dòng / số đoạn** | **4 đơn hàng mẫu** (`ORD-101` Cơm Tấm Ba Ghiền, `ORD-102` Trà Sữa ToCoToCo, `ORD-103` Gà Rán KFC, `ORD-104` Pizza Hut — tổng cộng 9 dòng món ăn/đồ uống); **3 hồ sơ lịch sử tài khoản** (`U1`, `U2`, `U3_ABUSE`); **1 bản ghi chính sách dự phòng**. |
| **Phiên bản / ngày lấy** | v1.0 · Ngày 27/11/2026 |
| **Nhãn** | `synthetic` (dữ liệu giả lập phục vụ chạy thử công cụ) |
| **Giới hạn** | Quy mô gọn cho các kịch bản biên của lát cắt thiếu món; chưa kết nối cổng thanh toán/ví thật và chưa đối chiếu ảnh chụp hóa đơn bằng thị giác máy tính. |

**Data `synthetic` (nhóm tự sinh):**
- **Cách sinh & kiểm soát:** Thiết kế thủ công có chủ đích theo ma trận biên kiểm thử (cố định trong `data/orders_db.json`, không sinh ngẫu nhiên mỗi lần chạy để kết quả `eval` tái lập 100%).
- **Người kiểm & số dòng kiểm tay:** Đỗ Duy Tùng và Nguyễn Lâm Tùng đã kiểm tay **4/4 đơn hàng** và **3/3 hồ sơ tài khoản** khớp đơn giá — tổng tiền — điều kiện biên. Dữ liệu này **không dùng làm bằng chứng pain**.

---

## Dataset 2 · `data/policies.json` (Bảng chính sách bồi thường & hạn mức an toàn)

| Trường | Chi tiết |
|---|---|
| **Dùng để làm gì** | Nguồn quy tắc cho công cụ `get_policy(issue_type)` và bộ chặn rủi ro bằng code Python `check_claim_limit()` nhằm ngăn 100% hành vi tự động bồi thường vượt trần. |
| **Từ đâu** | Nhóm chuẩn hóa thành cấu trúc JSON từ khảo sát luồng Trợ giúp đơn hàng công khai trên ShopeeFood / GrabFood (kiểm tra ngày 27/11/2026, `spec.md` §0) và ngưỡng an toàn đã chốt ở `spec.md` §4. |
| **Xử lý những bước gì** | Tách thành 1 khối ràng buộc toàn cục (`global_constraints`: trần tự duyệt `50.000 VNĐ/món`, tối đa `< 3` lần khiếu nại/30 ngày, không tự hoàn phí ship) và các quy tắc theo loại sự cố kèm điều kiện chuyển chuyên viên (`escalation_triggers`). |
| **Số dòng / số đoạn** | **1 khối `global_constraints`** và **4 nhóm chính sách sự cố**: `missing_item` (trần 50k), `wrong_item` (trần 30k), `spilled_damaged` (trần 25k), `food_safety_hazard` (trần 0đ — bắt buộc chuyển CSKH ưu tiên `HIGH`). |
| **Phiên bản / ngày lấy** | v1.0 · Ngày 27/11/2026 |
| **Nhãn** | `synthetic` (quy tắc mô phỏng chuẩn hóa từ luồng trợ giúp công khai) |
| **Giới hạn** | Áp dụng một mức trần cố định `50.000 VNĐ` cho lát cắt thiếu món; thực tế sàn thương mại điện tử có thể phân tầng hạn mức theo hạng thành viên và lịch sử uy tín của quán đối tác. |

---

## Dataset 3 · Review công khai Google Play (`evidence/data-mining.md`)

| Trường | Chi tiết |
|---|---|
| **Dùng để làm gì** | Đào bằng chứng pain thực tế (`evidence/data-mining.md`) và trích xuất **9/26 câu thử thực tế** (`source = data_that`, đạt 34,6% ≥ 1/3 bộ câu thử) trong `eval/benchmark.csv`. |
| **Từ đâu** | Review công khai mức 1–3 sao trên Google Play Việt Nam của **ShopeeFood** (`com.deliverynow`, đăng 01/07–26/11/2026) và **Grab** (`com.grabtaxi.passenger`, đăng 12/09–26/11/2026). |
| **Xử lý những bước gì** | Thu thập bằng script `evidence/collect_reviews.py` → loại mã trùng → gắn nhãn gợi ý bằng biểu thức chính quy → đọc xác nhận thủ công ngữ cảnh đơn đồ ăn → ẩn danh hoàn toàn người viết, chỉ lưu thống kê và **25 ví dụ mã hóa** (`R003`…`R966`) trong `evidence/data-mining.md` (không commit file `raw-reviews-*.csv` lên repo). |
| **Số dòng / số đoạn** | Mẫu số quét **2.000 review** (**800 review ShopeeFood** + **1.200 review Grab**) → xác nhận **24/800 review ShopeeFood (3,00%)** và **7/1.200 review Grab (0,58%)** phản ánh thiếu món, giao sai món hoặc hỗ trợ/hoàn tiền chậm; trích **25 ví dụ** tại `evidence/data-mining.md`. |
| **Phiên bản / ngày lấy** | Thu thập ngày 27/11/2026 (17:24 và 17:41 giờ Việt Nam) — thực hiện bởi Nguyễn Ngọc Vinh |
| **Nhãn** | `thật` (dữ liệu review công khai, đã ẩn danh) |
| **Giới hạn** | Mẫu chỉ lấy nhóm 1–3 sao nên nghiêng về người dùng bức xúc; mẫu Grab gồm cả dịch vụ gọi xe/giao hàng nên tỷ lệ review đồ ăn thấp hơn ShopeeFood; nội dung review không kèm mã đơn nội bộ nên khi đưa vào `eval/benchmark.csv` đóng vai trò kiểm thử luồng thiếu thông tin (G10) và yêu cầu ngoài phạm vi. |
