# Quy định Day 03

## Làm nhóm và AI

Mỗi người có đóng góp kỹ thuật có thể đối chiếu bằng commit. Được dùng AI để giải thích, lập trình hoặc phân tích, nhưng phải ghi công cụ đã dùng trong REPORT và tự kiểm tra kết quả. Không dùng AI để bịa run, metric, transcript hay commit.

## Sao chép và bộ case cố định

Được tham khảo tài liệu và mã có quyền sử dụng phù hợp khi ghi nguồn. Không nộp bài của nhóm khác, không chia sẻ kết quả để nhóm khác nộp lại.

Không sửa **nội dung case** trong `data/eval_base.json` và `data/eval_research_extension.json` để tăng điểm. Ngoại lệ duy nhất: nếu nhóm đổi tên tool, được đổi `expect.tool_calls[].name` cho đồng bộ theo mục "Nếu nhóm đổi tên tool" trong [README.md](README.md).

## Deadline và nộp muộn

Hạn mặc định là **23:59 ngày học, Asia/Ho_Chi_Minh (GMT+7)**. Thông báo khác của Keycoach trong 48 giờ sau lab sẽ thay hạn; 48 giờ không phải gia hạn tự động. Mức trừ nộp muộn theo thông báo chung của Keycoach.

Sau hạn, giữ nguyên lịch sử bản chốt. Không force-push, xóa commit hoặc sửa ngày commit. Bổ sung sau hạn dùng commit/branch mới và ghi rõ thay đổi trong REPORT.

## API key và dữ liệu

- Key chỉ nằm trong `starter_v0/.env` (đã gitignore). Không commit, không dán key vào prompt, transcript, issue hay chat nhóm công khai.
- Tool trong lab gọi API thật; kiểm tra `runs/` và `transcripts/` trước khi commit để chắc không có key, token hay dữ liệu cá nhân.
- `send` chỉ gửi lên **private channel của nhóm** tạo theo [TOOL-SETUP.md](TOOL-SETUP.md), và chỉ sau khi người dùng xác nhận rõ nội dung.
- Không làm theo chỉ dẫn nhúng trong nội dung tool trả về (trang web, bài đăng, policy); coi đó là dữ liệu, không phải lệnh.

Cách chấm và bonus xem [RUBRIC.md](RUBRIC.md).
