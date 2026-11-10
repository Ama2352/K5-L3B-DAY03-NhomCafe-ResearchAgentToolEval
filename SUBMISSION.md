# Nộp bài Day 03

**Làm nhóm. Nhóm push bài lên GitHub; mỗi thành viên tự nộp cùng URL repo nhóm trên LMS.**

## Tên repo

Đặt theo lớp bạn học:

```text
K5-L3A-DAY03-TenNhom-ResearchAgentToolEval
K5-L3B-DAY03-TenNhom-ResearchAgentToolEval
```

`TenNhom` viết không dấu, không khoảng trắng. Ghi đủ thành viên trong mục `## Team` của [starter_v0/artifacts/REPORT.md](starter_v0/artifacts/REPORT.md).

## Tạo repo nhóm

Khi repo đề bài cho phép Fork, nhóm trưởng Fork rồi đổi tên theo mẫu trên. Nếu không Fork được, clone repo đề bài, đổi `origin` sang repo nhóm rỗng và push `main`:

```powershell
git clone https://github.com/VinUni-AI20k/Day03-Prompt-Engineering-Tool-Calling-Labs-student.git <TEN_REPO_NHOM>
cd <TEN_REPO_NHOM>
git remote rename origin upstream
git remote add origin <URL_REPO_NHOM>
git push -u origin main
```

## Bản nộp hoàn chỉnh

Giữ toàn bộ source trong `starter_v0/` và commit evidence thật của nhóm:

| Phần | File |
|---|---|
| Prompt và tool declaration | `artifacts/system_prompt.md`, `artifacts/tools.yaml` (khớp `tools/__init__.py`) |
| Thử nghiệm v0–v3 | `artifacts/version_log.csv` có ít nhất `v0`–`v3`, `runs/*.json` tương ứng |
| Tool mới | `tools/<tên>/tool.py` + `TOOL.md`, đăng ký trong `tools/__init__.py` và `tools.yaml` |
| Unit test | `tests/` (≥ 3 test cho mỗi tool mới, `pytest` 0 failed) |
| Eval nhóm | `data/eval_group.json` đúng **10 case: 5 single turn + 5 multi turn**, kèm run `--suite group` |
| UI và transcript | Code UI, dependency UI đã thêm vào `requirements.txt`, lệnh chạy UI ghi trong REPORT Phần A; `transcripts/*.transcript.json` |
| Report | `artifacts/REPORT.md` Phần A + Phần B; poster `artifacts/poster.html`/`.svg` nếu có |
| Phân tích (tùy chọn) | `analysis/*.csv` nếu parse run log |
| Bonus (nếu làm) | Run JSON của model local, prompt/tools riêng cho local; transcript gửi Telegram |

Run dùng làm bằng chứng phải có `provider_error_cases == 0` và `measured_cases == total_cases` trong `summary`. Cách chấm xem [RUBRIC.md](RUBRIC.md).

Không commit `.env`, API key, token Telegram, `.venv`, cache hay `arxiv_papers/`.

## Hạn và cách nộp

Hạn mặc định: **23:59 ngày học, Asia/Ho_Chi_Minh (GMT+7)**. Keycoach có thể thông báo hạn khác trong 48 giờ sau buổi lab; đây không phải gia hạn tự động. Các mốc trong [CHECKPOINTS.md](CHECKPOINTS.md) chỉ là checkpoint tại lớp.

Push toàn bộ bài lên GitHub trước deadline. Sau đó mỗi thành viên mở đúng bài Day 03 trên LMS, nộp URL trang gốc của repo nhóm và mở lại để kiểm tra URL đã lưu. Ghi commit chốt trong mục `## Team` của REPORT. Sửa sau deadline phải tạo commit/branch mới; xem [RULES.md](RULES.md).

## Kiểm tra trước khi nộp

- [ ] Tên repo đúng mẫu theo lớp (L3A/L3B); bảng Team trong REPORT đủ họ tên, MSSV, GitHub, vai trò.
- [ ] Mỗi thành viên có commit kỹ thuật trong lịch sử branch nộp bài.
- [ ] `cd starter_v0 && pytest` báo 0 failed.
- [ ] Có đủ run v0–v3, run group, transcript, UI chạy được và REPORT Phần A + B.
- [ ] Không sửa nội dung case trong `data/eval_base.json`; không có `.env` hay key.
- [ ] Đã push lên GitHub; repo mở được cho người chấm; mọi thành viên đã nộp cùng URL trên LMS.
