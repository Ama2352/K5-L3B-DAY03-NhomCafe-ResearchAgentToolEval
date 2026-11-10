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

Số liệu (lấy từ run JSON): case_accuracy 0.45 → 0.65 → 0.95 → 1.00 qua v0–v3; routing 0.60 → 1.00; multiturn 0.67 → 1.00.

Điều chưa chắc chắn: 1.00 chỉ đo trên bộ base mà prompt và mô tả tool được chỉnh theo chính các case đó, nên có thể quá khớp. Chưa chạy v3 trên bộ extension và bộ group để kiểm chứng. Case R12 chỉ pass sau v3 và hành vi "xác nhận trước khi hỏi nội dung" là một lựa chọn thiết kế để khớp eval, không phải cách duy nhất hợp lý.

> Sau khi làm bài này em học được cách đọc log, nên cân nhắc khi nào nên sửa prompt khi nào nên sửa tools. 
