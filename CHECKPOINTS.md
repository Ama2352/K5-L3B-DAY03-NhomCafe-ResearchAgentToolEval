# Checkpoints Day 03

**Làm nhóm.** Các mốc dưới đây là checkpoint tại lớp, **không phải deadline**. Deadline nộp bài là 23:59 ngày học (GMT+7); xem [SUBMISSION.md](SUBMISSION.md).

| Mốc | Giờ | Cần làm | Sản phẩm | Tự kiểm tra |
|---|---|---|---|---|
| CP0 | Trước 15:00 | Tạo repo nhóm, chia việc, setup `.env` theo [TOOL-SETUP.md](TOOL-SETUP.md) | Repo chung, bảng Team trong REPORT | Preflight provider pass; `pytest` chạy được (contract + example xanh, TODO đang skipped) |
| CP1 | 15:00 | Chạy baseline v0 chưa sửa artifact; dựng khung UI | Run base v0, dòng v0 trong `version_log.csv` | `provider_error_cases == 0`; đã gán loại lỗi cho các case FAIL |
| CP2 | 15:30 | Sửa prompt/tools cho v1; viết ít nhất 1 tool mới kèm test | Run v1, tool mới + ≥ 3 test | `pytest` 0 failed; `test_tool_contract.py` xanh |
| CP3 | 16:00 | Viết 10 case nhóm (5 single + 5 multi turn); làm v2 | `data/eval_group.json`, run group, run v2 | Có ≥ 1 case route tới tool mới |
| CP4 | 16:30 | **Team showdown**: demo sản phẩm; REPORT Phần A (hoặc poster) là tài liệu phụ trợ | REPORT Phần A, link dùng thử UI | Team khác mở được link và thử câu hỏi mẫu |
| CP5 | 17:30 | Làm v3; hoàn thiện REPORT Phần B | Run v3, version log đủ v0–v3, transcript ≥ 3 lượt | Mỗi version có giả thuyết, hash và đường dẫn run |
| FINAL | 23:59 | Rà checklist trong [SUBMISSION.md](SUBMISSION.md), push GitHub, từng thành viên nộp link repo trên LMS | Repo hoàn chỉnh trên GitHub | Mở repo, run và link thật trên GitHub |

Bonus (Small Local Model, thêm tool, gửi Telegram thật, test challenge) làm sau khi phần bắt buộc đã đủ; xem [RUBRIC.md](RUBRIC.md).
