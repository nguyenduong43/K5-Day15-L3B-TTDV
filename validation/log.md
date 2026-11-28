# Người dùng thử *(bonus)*

> Điền ở guide bước 4.3 — 2–3 người ngoài nhóm, ~10 phút / người, theo 5 nhịp: làm quen · bối cảnh · giao việc · quan sát · hỏi sau. Ôn lại: ngày 5, ngày 13. Chấm ở rubric Bonus.
> Không ghi tên: ghi vai. Hành vi quan sát được nặng hơn lời nói; toàn lời khen = phiên chưa đạt, giao việc khó hơn.
> Người dùng thử **không thay được** bằng chứng pain ở `evidence/`.

| Người thử (vai) | Việc giao (theo kết quả, không theo nút) | Quan sát (làm gì đầu tiên, chỗ do dự, chỗ hiểu sai) | Trích nguyên văn | Mức nghiêm trọng (cao / vừa / thấp) |
|---|---|---|---|---|
| Sinh viên hay đặt cơm trưa qua app (U1) | Đơn ORD-101 bị thiếu món **Canh rong biển**. Báo thiếu món và giải thích kết quả nhận được sau khi gửi. | Bấm đúng vào đơn ORD-101 ngay lập tức. Tuy nhiên khi chọn xong món thiếu, người dùng khựng lại ~6 giây ở màn hình kết quả vì thông báo chỉ ghi "Đã ghi nhận khiếu nại", không rõ được hoàn tiền hay quán sẽ giao bù. | *"Ủa báo xong rồi nhưng giờ mình ngồi đợi shipper quay lại đưa canh hay app tự cộng tiền lại vào ví vậy?"* | Cao |
| Nhân viên văn phòng hay đặt đồ ăn nhóm (U2) | Đơn ORD-104 bị thiếu **Pizza hải sản cỡ vừa**. Báo thiếu món và cho biết ai sẽ xử lý tiếp, bản thân cần làm gì. | Nhìn lướt qua danh sách đơn, bấm nhầm vào nút "Liên hệ hỗ trợ" ở góc dưới thay vì chọn trực tiếp trong chi tiết đơn ORD-104. Sau khi quay lại và gửi báo cáo thành công, người dùng không chắc bên quán hay bên app sẽ xử lý, cũng không biết có cần chụp ảnh hóa đơn/túi đồ giữ lại làm bằng chứng không. | *"Gửi xong rồi mà không thấy ghi ai duyệt, nhỡ lát tổng đài gọi bắt chụp ảnh túi đồ ăn mà mình lỡ vứt rồi thì sao?"* | Vừa |

Câu hỏi sau: *"Nếu mai không được dùng nữa, bạn thấy: rất tiếc / hơi tiếc / không sao?"* → 0 / 2 / 0

## Tổng hợp

- Chủ đề lặp nhiều nhất: **Thiếu thông tin trạng thái tiếp theo (Next-step clarity)** — Cả hai người dùng đều thao tác gửi báo cáo khá nhanh nhưng đều lúng túng sau khi bấm gửi: không rõ hình thức đền bù (hoàn tiền hay giao bù), không rõ bộ phận nào tiếp nhận và bản thân có cần giữ hiện trường/chụp ảnh thêm không.
- Sửa gì trước demo (ghi `spec.md` §10): Cập nhật màn hình/thông báo xác nhận sau khi gửi báo thiếu món: hiển thị rõ **(1) Phương án xử lý dự kiến** (VD: Hoàn tiền tự động trong X phút), **(2) Bên phụ trách xử lý** (Bộ phận CSKH / Đối tác nhà hàng), và **(3) Hành động cần làm của khách** (VD: Không cần thao tác thêm / Giữ lại hóa đơn nếu có).
- Giữ gì và vì sao: Giữ luồng chọn đơn và tích chọn món bị thiếu trực tiếp trên giao diện đơn hàng vì cả 2 người đều tìm thấy và hoàn thành thao tác này trong dưới 15 giây mà không cần hướng dẫn.
- Để dành sau: Bổ sung tính năng tải ảnh minh chứng trực tiếp lúc báo thiếu món và theo dõi tiến độ xử lý khiếu nại theo thời gian thực (real-time status tracker).