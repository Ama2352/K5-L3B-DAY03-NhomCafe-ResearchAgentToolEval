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
  - Claude Code: <!-- TODO: ghi rõ dùng AI cho phần nào -->
  - Tự kiểm tra: <!-- TODO: ví dụ đọc `results[*].result.failures` trong run JSON để đối chiếu PASS/FAIL từng case -->

## 5. Tự đánh giá

<!-- TODO: tự viết — điều làm tốt, điều chưa làm được, bài học -->
