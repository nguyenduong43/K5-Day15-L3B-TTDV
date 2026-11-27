# AI SPEC — Xử lý khiếu nại đơn giao đồ ăn thiếu món · Nhóm TTDV · Lớp L3B

> Mốc nộp: §7 chốt chuẩn "đạt" tại **CP2 19:30 Thứ Sáu 27/11** · §0–§7 nộp **CP3 10:00 Thứ Bảy 28/11** · đủ §0–§10 **CP4 14:30 Thứ Bảy 28/11** · §10 changelog ghi tiếp đến **23:59 Thứ Bảy 28/11**.
> Đầu mỗi mục ghi bước guide (`02-guide.md` trong repo đề) chỉ cách điền. Mỗi mục ngắn, có số và nguồn; chi tiết để ở file được trỏ tới. Xoá dòng hướng dẫn trong ngoặc vuông khi điền xong.

Track: [ ] A · [ ] B · [ ] C · [x] D · [ ] E — bài toán: D1 · Xử lý khiếu nại đơn giao đồ ăn thiếu món
Data BTC cấp đã dùng: Không (Track D nhóm tự tìm data theo quy định của BTC)

## §0. Hiện tại việc này diễn ra thế nào *(guide 1.1)*
- Luồng hiện tại của việc này trên app thật (ShopeeFood / GrabFood):
  1. Khách nhận đồ ăn, mở túi kiểm tra phát hiện thiếu 1 món (ví dụ: đặt cơm sườn + canh + trà sữa, nhưng thiếu ly trà sữa 35k).
  2. Khách vào app > Lịch sử đơn hàng > Bấm "Báo cáo sự cố / Trợ giúp".
  3. Chatbot rule-based hiện menu phân nhánh, bắt khách bấm từng nút để khai báo.
  4. Hệ thống yêu cầu chụp ảnh hoá đơn và toàn bộ đồ ăn đã nhận để đối chiếu.
  5. Chatbot tạo ticket hỗ trợ và thông báo: "Yêu cầu đã được ghi nhận, CSKH sẽ phản hồi qua email/tin nhắn trong 24h-48h". Khách mất bữa trọn vẹn, phải chịu tiền món thiếu trong khi chờ đợi.
- Công cụ / AI đang được dùng cho việc này: Chatbot theo cây quyết định (Shopee Help Center, Grab Help Center). Nguồn: Khảo sát thực tế tính năng Trợ giúp đơn hàng trên app Shopee và Grab (kiểm tra 27/11/2026).

## §1. Người dùng & bằng chứng *(guide 1.1, 1.2)*
- Người dùng chính (một vai cụ thể): Khách hàng cá nhân hoặc người đặt ăn trưa văn phòng qua app giao đồ ăn (ShopeeFood, GrabFood).
- Việc họ cố làm xong: Khiếu nại và nhận lại tiền bồi thường (hoặc voucher) cho món ăn bị thiếu trong đơn hàng vừa nhận.
- Hôm nay họ giải bằng gì, hỏng ở đâu, vì sao chưa bỏ: Giải bằng chatbot menu có sẵn trong app hoặc gọi hotline. Hỏng ở chỗ chatbot cứng nhắc, bắt làm thủ tục rườm rà, nhân viên xử lý rất chậm (vài giờ đến vài ngày) trong khi khách cần giải quyết ngay lúc đang ăn. Chưa bỏ vì vẫn cần dịch vụ giao đồ ăn mỗi ngày.
- Pain (KHÔNG chữ AI): Khách đặt đồ ăn khi nhận đơn bị thiếu một món, khiếu nại qua hệ thống hỗ trợ thì menu trả lời tự động cứng nhắc, nhân viên hỗ trợ phản hồi chậm sau nhiều giờ hoặc nhiều ngày, khiến khách mất tiền món thiếu và bữa ăn bị gián đoạn, ức chế.
- Bằng chứng — số chính + kết luận (chi tiết: `evidence/summary.md`): Đang đào 50 review 1-3 sao trên Google Play (ShopeeFood/Grab) và phỏng vấn trực tiếp 3 học viên trong lớp từng gặp sự cố thiếu món trong 1 tháng qua (tổng hợp tại CP2).

## §2. Impact & quyết định chọn *(guide 1.3)*

| Hướng | Bao nhiêu người gặp | Bao nhiêu lần / tháng | Mỗi lần tốn gì | Impact / tháng | Làm kịp không | Chọn? |
|---|---|---|---|---|---|---|
| **D1. Xử lý khiếu nại đơn thiếu món** | ~3.000 đơn sự cố / 100k đơn | 1–2 lần / khách thường xuyên | Khách mất 35k tiền món thiếu + 15 phút bực bội; nhân viên CSKH mất 10 phút xử lý thủ công | Tiết kiệm ~350 giờ CSKH/tháng, giảm thời gian giải quyết từ 24h xuống 30 giây | Có (lát cắt gọn, ranh giới AI/code rõ) | **CHỌN** |
| D2. Đặt đơn nhóm có ràng buộc | ~1.000 đơn nhóm văn phòng | 2–4 lần / tháng | Người đặt mất 20–30 phút gom món, tính tiền, check dị ứng | Tiết kiệm thời gian đặt đơn | Khó kịp (logic gom giỏ & menu nhiều biến) | Loại |
| D3. Trả hàng, hoàn tiền sàn TMĐT | ~5.000 đơn đổi trả / tháng | 1 lần / vài tháng | 2–5 ngày chờ đợi, nguy cơ tranh chấp giữa người mua và người bán | Giảm tải trọng tài sàn | Khó kịp (chu trình trả hàng dài ngày, nhiều bên) | Loại |

- **Impact / tháng** của hướng chọn = 3.000 ca khiếu nại × 70% ca giải quyết tự động × 10 phút CSKH = 21.000 phút (~350 giờ nhân viên / tháng) *(tự ước tính trên quy mô 100.000 đơn/tháng)*.
- Hướng ĐÃ LOẠI + vì sao: Hướng D2 (gom đơn nhóm) và D3 (trả hàng sàn) bị loại vì phạm vi lớn, chu trình xử lý kéo dài nhiều bên, khó kiểm chứng và demo trọn vẹn trong 2 phút của hackathon.
- Số lần / tháng của từng kiểu người dùng (dùng cho persona ở §8):
  - Khách văn phòng đặt thường xuyên: 15–20 đơn/tháng, khiếu nại 1–2 lần/tháng.
  - Khách thỉnh thoảng đặt: 2–4 đơn/tháng, khiếu nại 1 lần / 3 tháng.
  - Khách khiếu nại nhiều lần / bất thường: 4–5 lần khiếu nại/tháng.

## §3. Giải pháp tương tự *(guide 2.1)*
- [sản phẩm / tính năng gần giống]: một điều đáng học · một điều đáng né · mình khác gì

## §4. Thiết kế *(guide 2.2, 3.2)*
- **Lát cắt MỘT CÂU** (1 người dùng · 1 việc · 1 quyết định AI · 1 kết quả):
- Không làm (≥3 điều):
- **Sơ đồ** (ảnh / Mermaid / draw.io): [chèn ở đây]
- **Hình dạng:** [ ] workflow cố định · [ ] một agent · [ ] nhiều agent — 2 dòng lý do, và vì sao **không** chọn hình dạng phức tạp hơn:
- **AI dựa vào đâu** — mỗi công cụ (khớp `codebase/tools.py`):

  | Công cụ | Input | Output | Tác động ra ngoài? |
  |---|---|---|---|
  |  |  |  |  |

- **Mức tự động:** [ ] AI gợi ý, người quyết · [ ] AI tự làm khi chắc, chuyển người khi không · [ ] AI tự làm — lý do (sai thì ai chịu gì, sửa đắt hay rẻ):
- **Chỗ chặn rủi ro** (rủi ro lớn nhất của lát cắt bị chặn ở đâu, bằng gì):
- **Chỗ người duyệt** (việc AI không được tự làm):
- **Nguyên tắc thiết kế** (≥3, bắt buộc G10):

  | Nguyên tắc | Chỗ cụ thể trên sơ đồ / trong bản chạy thử |
  |---|---|
  | G10 — thu hẹp phạm vi khi không chắc |  |
  |  |  |
  |  |  |

- Phần nào còn giả (công cụ trả dữ liệu giả, model chế độ giả…) — ghi rõ, không giả làm thật:

## §5. Chỗ khó — 4 lớp + ≥6 kịch bản + 2 tấn công *(guide 2.3)*

| Kịch bản | Lớp (1–4) | Hành vi mong muốn (nói gì, hiện gì, cho làm gì tiếp) | Câu thử |
|---|---|---|---|
|  |  |  |  |
| *(tấn công)* |  |  |  |
| *(tấn công)* |  |  |  |

(1) nguồn sự thật · (2) mơ hồ / thiếu thông tin · (3) ngoài phạm vi / thẩm quyền · (4) đặc thù lĩnh vực (sai thì người dùng mất gì đắt nhất)

## §6. Bốn đường đi của trải nghiệm
- Mọi thứ suôn sẻ: · Không chắc (lớp 2): · Không có căn cứ (lớp 1): · Người dùng sửa:
- Bị đòi ngoài phạm vi (lớp 3): · Trường hợp đặc thù lĩnh vực (lớp 4):

## §7. Đánh giá & chuẩn "đạt" *(guide 2.4, 4.1)*
- Data card: `data/DATA_CARD.md` · bộ câu thử: `eval/benchmark.csv` — __ câu (thuong __ · kho __ · tu_choi __) · metric: `eval/metric_spec.yaml` (__ metric)
- **Chuẩn "đạt"** (chốt **trước 19:30 Thứ Sáu 27/11**, giữ nguyên đến 23:59 Thứ Bảy 28/11): "Đạt khi ≥ __% câu qua, và __"
- Kết quả: lượt 1 __/__ (__%) · lượt 2 __/__ (__%) — run ID: __ / __ → chi tiết `eval/report.md`, hồ sơ `eval/README.md`

## §8. Chi phí khi dùng thật *(guide 4.2)*
- Persona + giá: `cost/personas.yaml` · lượt mô phỏng: `cost/simulate-__.csv` (__ phiên)
- Chi phí / task thành công: __ (model __) · __ (model __)
- Chi phí / tháng ở quy mô thật: thấp __ · cơ sở __ · cao __ → chi tiết `cost/cost-estimate.md`
- So với impact / người / tháng (§2): đáng làm không, vì sao:

## §9. Rủi ro & an toàn
- Dữ liệu: đã ẩn danh gì, không thu gì, không đưa gì vào model gói miễn phí:
- AI **không được** làm gì kể cả khi người dùng yêu cầu:
- Ai có thể bị hại nếu AI sai, và nhóm chặn thế nào:

## §10. Phân công & changelog
- Phân công có tên (theo chặng, chia cặp — guide "Cách chia việc"): __
- Dùng AI vào việc gì (2–3 dòng; chi tiết `docs/ai-usage.md`):
- Nhật ký thay đổi — **mọi thay đổi sau CP2 19:30 Thứ Sáu 27/11 phải có dòng ở đây**:

**CP2 → CP4** (vd thu hẹp lát cắt, hỏi thêm người dùng, lần cải tiến trước lượt 2)

| Thời điểm | Đổi gì | Vì sao (trỏ về câu thử / lỗi / bằng chứng nào) |
|---|---|---|
|  |  |  |

**Sau CP4 (đến 23:59 Thứ Bảy 28/11)** (sửa theo góp ý — không sửa chuẩn "đạt", câu thử, số bằng chứng, kết quả các lượt đã chạy)

| Thời điểm | Đổi gì | Vì sao |
|---|---|---|
|  |  |  |
