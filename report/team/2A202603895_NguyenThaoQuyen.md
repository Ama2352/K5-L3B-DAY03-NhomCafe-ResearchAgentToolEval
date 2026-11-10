# Báo cáo cá nhân — Nguyễn Thảo Quyên - 2A202603895

## 1. Thông tin thành viên

- Họ tên: Nguyễn Thảo Quyên
- MSSV: 2A202603895
- Email: 26ai.quyennt@vinuni.edu.vn

## 2. Phần việc phụ trách

- CP1: setup môi trường, thêm provider DeepSeek, chạy baseline v0, phân tích lỗi (bảng B2).
- CP2: tối ưu prompt và tool declaration qua v1, v2, v3, ghi `version_log.csv` và bảng B1.

## 3. Đóng góp cụ thể

- **Provider DeepSeek:** thêm `starter_v0/providers/deepseek_provider.py` (kế thừa `OpenAIProvider`, dùng model `deepseek-chat`), đăng ký trong `providers/__init__.py`, `run_eval.py`, `chat.py`, `scripts/preflight_provider.py`.
- **v0 (baseline):** 9/20 pass, `case_accuracy` 0.45. Phân loại 11 case FAIL theo loại lỗi (`missing_info`, `wrong_boundary`, `out_of_scope`, `wrong_tool`, `wrong_arg_value`) và nguyên nhân trong bảng B2.
- **v1 (sửa `system_prompt.md`):** bỏ chỉ dẫn đoán thay vì hỏi, gửi ngay, ép một bước; thêm rule hỏi lại bằng `clarify`, xin xác nhận trước khi `send`, từ chối câu ngoài phạm vi. Kết quả 0.45 → 0.65 (13/20).
- **v2 (sửa `tools.yaml`):** viết lại `description` của 10 tool gốc (khi nào dùng/không dùng) và quy ước tham số (`query` ngắn, `topic=news`, bảng `timeframe`, handle không có `@`, `search_type`, gọi một lần). Kết quả 0.65 → 0.95 (19/20). v2 gồm cả 3 tool mới của CP3 đã merge từ `main`.
- **v3 (sửa `system_prompt.md`):** tách xác nhận gửi/đăng thành hai bước (`clarify yes_no` xác nhận ý định trước, rồi mới hỏi nội dung nếu thiếu). Kết quả 0.95 → 1.00 (20/20), không case nào tụt.
- **Bonus Telegram thật:** tạo bot qua BotFather và kênh private `Nhomcafe`, thêm bot làm admin, lấy chat id bằng `getUpdates`, điền `TELEGRAM_BOT_TOKEN`/`TELEGRAM_CHAT_ID` vào `starter_v0/.env` (file bị `.gitignore` loại). Thử tool `send` trực tiếp (`status: sent`), rồi chat live 7 lượt bằng `chat.py` với bản v3 (DeepSeek): hỏi tweet, bổ sung URL sau khi agent xin link, và đăng bản tin lên Telegram sau khi xác nhận (`send(confirmed=true)`, `status: sent`, tin nhắn hiện trong kênh). Ghi bảng B4 và dòng bonus Telegram trong B5 của báo cáo nhóm.
- **Quét bí mật trước khi commit:** kiểm tra toàn bộ `transcripts/` và `runs/` không chứa token Telegram.

## 4. Bằng chứng

- File/commit/PR:
  - Commit: `b6cabe6` (provider DeepSeek), `aee80bb` (v0 + B2), `2382810` (v1), `2b10ae5` (v2), `415cd21` (v3), `a8684c7` (`TEAM.md`).
  - PR: #1, #3, #4, #5 vào `main`.
  - Run: `starter_v0/runs/v0_B_base_deepseek_20261110T174313805995.json`, `v1_B_base_deepseek_20261110T182742199017.json`, `v2_B_base_deepseek_20261110T184518723180.json`, `v3_B_base_deepseek_20261110T190413436138.json` (cả bốn run đều có `provider_error_cases = 0`, `measured_cases = 20`).
  - `starter_v0/artifacts/version_log.csv`; bảng B1, B2 trong `report/team/group_report.md`.
  - Telegram: transcript `starter_v0/transcripts/v3_deepseek_20261111T000241323945.transcript.json` (lượt 6–7: hỏi xác nhận rồi `send` trả `status: sent`); bảng B4 và dòng bonus Telegram trong B5 của `report/team/group_report.md`; nhánh `docs/live-chat-telegram-evidence`.
- AI/công cụ đã dùng và cách tự kiểm tra kết quả:
  - Dùng Claude Code để đọc repo, viết `deepseek_provider.py`, soạn nội dung `system_prompt.md` và `tools.yaml`, và tóm tắt run JSON; hướng dẫn tạo bot/kênh Telegram và đọc transcript chat live.
  - Cách kiểm tra: tự chạy `scripts/preflight_provider.py` và `run_eval.py` bằng API thật; đọc `failures`, `actual_tool_calls` trong run JSON để đối chiếu từng case FAIL, không dựa vào lời AI; chạy `pytest` (86 passed, 0 failed) để xác nhận `tools.yaml` vẫn khớp code; kiểm tra run hợp lệ qua `provider_error_cases` và `measured_cases`.

## 5. Tự đánh giá

Qua quá trình thực hiện, em đã học được cách đọc và phân tích log để xác định nguyên nhân lỗi, từ đó lựa chọn hướng cải thiện phù hợp giữa việc chỉnh sửa `system_prompt.md` và `tools.yaml`. Kết quả đánh giá cho thấy `case_accuracy` tăng từ 0.45 ở v0 lên 1.00 ở v3; routing tăng từ 0.60 lên 1.00 và multiturn tăng từ 0.67 lên 1.00.

Tuy nhiên, kết quả 1.00 mới được kiểm chứng trên bộ base gồm 20 case, trong khi prompt và mô tả tool đã được tối ưu dựa trên chính bộ dữ liệu này. Vì vậy, vẫn có khả năng mô hình bị overfitting và chưa đảm bảo khả năng tổng quát hóa. Số liệu của nhóm ủng hộ lo ngại này: v3 chạy trên bộ group (10 case do nhóm tự viết) đạt 9/10 (0.90), thấp hơn 1.00 ở bộ base (`starter_v0/runs/v3_B_group_deepseek_20261110T191743257537.json`). Em chưa kiểm thử v3 trên bộ extension. Ngoài ra, cách xử lý case R12 ở v3 là một lựa chọn thiết kế nhằm đáp ứng yêu cầu của bộ evaluation, không phải cách xử lý duy nhất hợp lý.

**Bài học rút ra:** Em hiểu rõ hơn vai trò của việc phân tích lỗi trước khi tối ưu hệ thống. Không phải lỗi nào cũng cần sửa prompt; có những trường hợp cần làm rõ mô tả tool, điều kiện sử dụng hoặc quy ước tham số để cải thiện khả năng routing và thực thi của Agent.
