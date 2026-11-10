# Rubric Day 03 — Tổng 100 điểm

**Phần bắt buộc 90 điểm + bonus tối đa 10 điểm = 100 điểm.** Không làm bonus thì tối đa 90 điểm.

## Phần bắt buộc (90)

| Tiêu chí | Điểm | Bằng chứng cần có | Không tính điểm khi |
|---|---:|---|---|
| Prompt và tool declaration | 15 | `system_prompt.md` bỏ chỉ dẫn xấu của starter, có rule routing; mỗi `description` trong `tools.yaml` nói rõ làm gì, khi nào dùng/không dùng, convention args; `send` có boundary xác nhận (`confirmed=true` chỉ sau khi user xác nhận) | Tên/tham số không khớp registry (`tests/test_tool_contract.py` đỏ), không có run |
| v0 đến v3 | 20 | Run v0, v1, v2, v3 trên `eval_base.json`; mỗi version **một** giả thuyết; `version_log.csv` có hash, metric trước/sau, đường dẫn run | Chỉ đổi nhãn version, thiếu run, run có lỗi provider |
| Tool mới + unit test | 15 | ≥ 1 tool mới có `tool.py`, `TOOL.md`, đăng ký trong `tools/__init__.py` + `tools.yaml`; ≥ 3 test/tool (happy path, input xấu, nhánh lỗi); `pytest` **0 failed** và 3 stub test của tool mới không còn `skip` | Test không assert gì, test gọi mạng thật, tool raise thay vì trả error dict |
| 10 case nhóm | 10 | `data/eval_group.json` đúng 5 single turn + 5 multi turn, có `expect` + `metadata.what_it_tests`, có ≥ 1 case route tới tool mới; run `--suite group` | Sao chép case có sẵn, thiếu cấu trúc hoặc run |
| UI và transcript | 10 | UI chạy được (Streamlit/Vercel/khác) theo lệnh trong REPORT, link dùng thử; transcript ≥ 3 lượt live (yêu cầu thường, thiếu thông tin rồi bổ sung, yêu cầu gửi/đăng) | Chỉ có ảnh chụp, UI che lỗi tool |
| Report | 15 | REPORT Phần A xong trước 16:30; Phần B có bảng v0–v3, failure analysis, eval nhóm, live chat, reflection, liên kết tới run/transcript | Nhận xét không có file hoặc commit đối chiếu |
| Làm nhóm | 5 | Bảng Team trong REPORT; mỗi thành viên có commit kỹ thuật | Chỉ ghi tên, không có commit đối chiếu |

**Run hợp lệ:** chỉ dùng run có `summary.provider_error_cases == 0` và `summary.measured_cases == summary.total_cases`. Một version không tăng điểm vẫn được tính quy trình nếu nhóm chạy thật, phân tích đúng và ghi trung thực.

## Bonus (tối đa 10)

| Bonus | Điểm | Bằng chứng |
|---|---:|---|
| Small Local Model Challenge (README Step 7) | 4 | ≥ 2 model local chạy base eval, ≥ 2 vòng tối ưu có log, bảng cloud vs local ở REPORT B7 |
| Hơn 3 tool mới (≥ 4 tool do nhóm tự viết) | 3 | Mỗi tool đủ `TOOL.md`, đăng ký, ≥ 3 test và có eval case route tới |
| Gửi Telegram thật sau xác nhận | 2 | Transcript cho thấy luồng: agent hỏi lại → user xác nhận → `send(confirmed=true)` → `status: sent` trên private channel của nhóm |
| Test challenge | 1 | Toàn suite `pytest` 0 skipped, **hoặc** regression test cho bug tìm được trong tool có sẵn (ghi ở REPORT B5) |

Tool có sẵn trong starter (`send`, `policy`, `papers`, `paper_text`) **không** tự được bonus; dùng chúng được tính trong phần bắt buộc. Đổi tên tool có sẵn không được tính là tool mới.

## Công thức

Điểm lab giữ trong thang 0–100: `max(0, min(100, điểm bắt buộc + bonus) - điểm trừ muộn)`. Mức trừ muộn theo thông báo Keycoach; xem [RULES.md](RULES.md).
