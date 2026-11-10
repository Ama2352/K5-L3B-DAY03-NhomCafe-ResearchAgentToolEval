# Báo cáo cá nhân — VuNgocQuynhAnh-2A202603875

## 1. Thông tin thành viên

- Họ tên: Vũ Ngọc Quỳnh Anh
- MSSV: 2A202603875
- Email: 26ai.anhvnq@vinuni.edu.vn

## 2. Phần việc phụ trách

- CP4: thiết kế và viết 10 eval case nhóm trong `starter_v0/data/eval_group.json` (5 single turn + 5 multi turn).
- Chạy group eval qua các version v1, v2, v3 và viết bảng B3 trong `report/team/group_report.md`.

## 3. Đóng góp cụ thể

- Viết case kiểm tra route tới tool mới: G01 (`word_count`), G02 (`source_domains`), GM03 (`citations`).
- Viết case cho các quy ước tham số mà bộ base chưa phủ: G03 (handle có `@`, câu tiếng Anh), G04 (`timeframe=year`), GM05 (đổi `timeframe` week → month).
- Viết case boundary khi gửi: GM01 (đã xác nhận → `send(confirmed=true)`), GM02 (huỷ → không gọi tool), GM04 (sửa nội dung sau khi xác nhận → phải hỏi lại).
- Viết G05 (tên mơ hồ "Apple" → `clarify(response_type="choice")`), case duy nhất test `choice`; fail ổn định ở v1–v3, chỉ ra khoảng trống trong prompt mà bộ base (20/20) không bắt được.
- Thay GM04 cũ (`clarify_then_word_count`) bằng `GM04_reconfirm_after_edit` để test boundary chặt hơn.
- Kết quả group: v1 7/10 → v2 9/10 → v3 9/10.

## 4. Bằng chứng

- File/commit/PR:
  - Commit `5684527` (10 case + run v1/v2 + bảng B3), `8ff7412` (run v3), `011b9ce` (B3 v3 + giải thích G05).
  - Run: `starter_v0/runs/v1_B_group_deepseek_20261110T184513176042.json`, `starter_v0/runs/v2_B_group_deepseek_20261110T190540806261.json`, `starter_v0/runs/v3_B_group_deepseek_20261110T191743257537.json`.
  - Bảng B3 trong `report/team/group_report.md`.
- AI/công cụ đã dùng và cách tự kiểm tra kết quả:
  - Claude Code: dùng để rà lại các việc còn thiếu so với `SUBMISSION.md`/`README.md`, merge `main` vào nhánh, và soạn nháp phần đóng góp trong `TEAM.md` và báo cáo này từ commit và run JSON có sẵn. Ngoài ra dùng AI gợi ý ý tưởng case và format JSON cho `eval_group.json`; nội dung case và kết quả được tự kiểm tra lại bằng run thật như bên dưới.
  - Tự kiểm tra: mỗi case trong `eval_group.json` đều chạy thật bằng `run_eval.py --suite group` với deepseek-chat; đọc `results[*].result.failures` trong run JSON để đối chiếu PASS/FAIL và tool call thực tế của từng case trước khi ghi vào bảng B3. Chỉ dùng run có `provider_error_cases == 0` và `measured_cases == total_cases`. Kiểm tra lại số liệu báo cáo (7/10, 9/10, 9/10) với `summary` của 3 file run. `pytest` (test_tool_contract) xanh sau khi thêm case, nghĩa là tên tool và tham số trong case khớp với `tools.yaml`.

## 5. Tự đánh giá

**Làm tốt:**
- Bộ case nhóm phủ được những phần bộ base chưa test: 3 tool mới, `timeframe=year`, handle có `@` trong câu tiếng Anh, sửa nội dung sau khi đã xác nhận, và `clarify(response_type="choice")`.
- G05 tìm ra một khoảng trống trong prompt (không có rule cho tên mơ hồ) mà bộ base đạt 20/20 không phát hiện được.

**Chưa làm được:**
- G05 vẫn fail ở v3; nhóm chưa thử thêm rule "tên nhiều nghĩa → `clarify(choice)`" để kiểm chứng.
- Case G05 chưa tốt: "tin về Apple" nghiêng mạnh về nghĩa công ty, nên hành vi của model có thể coi là hợp lý. Một case mơ hồ rõ hơn (ví dụ handle "Jordan") sẽ thuyết phục hơn.
- Run group v1 chạy với GM04 cũ, nên kết quả v1 không so sánh trực tiếp được với v2/v3.

**Bài học:**
- Điểm cao trên một bộ eval không có nghĩa là agent tốt: prompt đã được chỉnh theo chính bộ base, nên cần case ngoài base để thấy lỗi thật.
- Viết case cần tách rõ "model sai" với "case mơ hồ": đọc tool call thực tế trong run JSON trước khi kết luận.
