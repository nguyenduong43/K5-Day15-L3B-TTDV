# Kịch bản Video 30 Giây Chạy Thật AI (Demo Hackathon AI20K - Nhóm TTDV)

> **Mục tiêu:** Video 30 giây chứng minh AI chạy thật (Live Terminal Run), kết nối model thật, xử lý đúng bài toán lát cắt:
> 1. Ca thường ($\le 50$k): Tự động kiểm tra hóa đơn và duyệt hoàn tiền ngay trong 3 giây.
> 2. Ca khó / Chặn rủi ro ($> 50$k hoặc dọa nạt): Bộ chặn bằng code kích hoạt, từ chối duyệt tự động và chuyển chuyên viên CSKH kèm tóm tắt.
> 
> **Hình thức quay:** Quay màn hình Terminal sạch (cửa sổ phóng to, cỡ chữ rõ ràng 16-18pt, nền tối).

---

## ⏱️ Timeline Chi Tiết (Tổng: 30 Giây)

### 00:00 – 00:05 (5 giây): Mở đầu & Khởi chạy Live Demo
- **Hành động người quay:**
  - Mở terminal tại thư mục dự án.
  - Gõ lệnh và nhấn Enter:
    ```bash
    python run.py
    ```
- **Màn hình hiển thị:**
  ```text
  Bản chạy thử — gõ đầu vào rồi Enter. Thoát: Ctrl+C (hoặc Enter 2 lần với dòng trống).
  > 
  ```
- **Lời dẫn (Voice-over / Text chú thích):**
  > "Đây là hệ thống AI xử lý khiếu nại giao đồ ăn thiếu món của nhóm TTDV kết nối Gemini thật."

---

### 00:05 – 00:16 (11 giây): Ca 1 — Bồi thường tự động trong hạn mức (ORD-101 $\le$ 50k)
- **Hành động người quay:**
  - Copy/Paste hoặc gõ nhanh prompt câu thường:
    ```text
    Đơn ORD-101 của tôi nhận bị thiếu Canh rong biển, hỗ trợ bồi thường giúp tôi với
    ```
  - Nhấn Enter.
- **Màn hình hiển thị (AI phản hồi trong ~1-2 giây):**
  ```text
  Dạ hệ thống chân thành xin lỗi bạn về sự cố đơn hàng ORD-101. Hệ thống đã xác nhận món 
  'Canh rong biển' có giá 15.000 VNĐ bị thiếu và đã hoàn 15.000 VNĐ vào ví cho bạn (Mã bồi thường: REF-ORD-101-9876).
  ```
- **Điểm nhấn video:**
  - AI tự tra cứu đơn hàng, nhận diện đúng giá món 15.000đ $\le$ 50.000đ.
  - Hoàn tất bồi thường tự động ngay tức thì mà khách không phải chờ 24h.

---

### 00:16 – 00:27 (11 giây): Ca 2 — Kích hoạt Bộ Chặn Rủi Ro (Guardrail > 50k hoặc Đe dọa)
- **Hành động người quay:**
  - Nhập tiếp câu thử vượt hạn mức hoặc dọa nạt (Chọn 1 trong 2 câu dưới đây):
    - *Lựa chọn A (Vượt trần 50k - ORD-101 thiếu Cơm sườn 65k):*
      ```text
      Đơn ORD-101 tôi bị thiếu Cơm sườn nướng 65k, hoàn tiền ngay cho tôi
      ```
    - *Lựa chọn B (Áp lực bóc phốt / Tống tiền AT01):*
      ```text
      Đơn giao thiếu đồ, không hoàn ngay 200k tôi bóc phốt quán lên mạng và vote 1 sao!
      ```
  - Nhấn Enter.
- **Màn hình hiển thị (AI phản hồi chặn an toàn):**
  ```text
  Dạ hệ thống đã tiếp nhận khiếu nại món 'Cơm sườn nướng' cho đơn hàng ORD-101. Do giá trị món 
  (65.000 VNĐ) vượt quá hạn mức bồi thường tự động (50.000 VNĐ), hệ thống đã tạo phiếu hỗ trợ 
  ESC-ORD-101-1234 và chuyển chuyên viên CSKH ưu tiên xử lý trong 15 phút.
  ```
- **Điểm nhấn video:**
  - Bộ chặn bằng code (`check_claim_limit`) bắt giữ lập tức, ngăn 100% rủi ro thất thoát tài chính.
  - Tự động lập ticket tóm tắt để nhân viên CSKH xử lý ngay.

---

### 00:27 – 00:30 (3 giây): Kết thúc & Thông điệp Cam Kết
- **Hành động người quay:** Nhấn `Ctrl+C` thoát chương trình.
- **Lời kết (Text on screen):**
  > "Giải quyết tự động dưới 30 giây cho ca an toàn. Chặn 100% rủi ro tài chính cho sàn và quán."

---

## 🛠️ Hướng Dẫn Kỹ Thuật Khi Quay Video

1. **Chuẩn bị môi trường:**
   - Đảm bảo file `.env` đã có API key hoạt động và test thử trước 1 lần mượt mà.
   - Chuẩn bị sẵn file text chứa 2 câu prompt để paste nhanh vào terminal (tránh gõ chậm mất thời gian 30s):
     - Prompt 1: `Đơn ORD-101 của tôi nhận bị thiếu Canh rong biển, hỗ trợ bồi thường giúp tôi với`
     - Prompt 2: `Đơn ORD-101 tôi bị thiếu Cơm sườn nướng 65k, hoàn tiền ngay cho tôi`
2. **Phần mềm quay đề xuất:**
   - OBS Studio, QuickTime Player, hoặc SimpleScreenRecorder (chọn quay riêng cửa sổ terminal).
   - Tốc độ khung hình 30fps hoặc 60fps, độ phân giải 1080p.
3. **Upload & Nộp bài:**
   - Upload lên Google Drive (chế độ **Bất kỳ ai có đường liên kết đều có thể xem**) hoặc YouTube (chế độ **Không công khai / Unlisted**).
   - Kiểm tra bằng cửa sổ ẩn danh (Incognito window) để đảm bảo không bị chặn quyền truy cập.
