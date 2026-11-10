# Team

## Thông tin nhóm

- Tên nhóm: NhomCafe
- Lớp: L3B
- Repo nhóm: `K5-L3B-DAY03-NhomCafe-ResearchAgentToolEval`
- URL repo: https://github.com/Ama2352/K5-L3B-DAY03-NhomCafe-ResearchAgentToolEval
- Nhánh nộp: `main` (đang làm trên `feature/prompt-v1`)
- Commit chốt: `2c12687` (cập nhật lại khi chốt bài nộp)

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Vũ Ngọc Quỳnh Anh | 2A202603875 | 26ai.anhvnq@vinuni.edu.vn | qavu2407-lang | CP4: 10 eval case nhóm (5 single + 5 multi turn), chạy group eval v1–v3, phân tích B3 |
|   2 | Nguyễn Thảo Quyên |   2A202603895   |   26ai.quyennt@vinuni.edu.vn    |    100678carwyn   | CP1–CP2: provider DeepSeek, baseline v0, tối ưu prompt (v1) và tools.yaml (v2) |
|   3 | Hồ Nguyễn Minh Sang |  2A202603905  |   26ai.sanghnm@vinuni.edu.vn    | Ama2352 | CP3: tool mới (citations, source_domains, word_count) + unit test; quản lý repo, merge PR |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

Sao chép mục dưới đây cho từng thành viên.

## Nguyễn Thảo Quyên

### Phần việc phụ trách

- CP1: setup môi trường, thêm provider DeepSeek, chạy baseline v0, phân tích lỗi (B2).
- CP2: tối ưu v1 (`system_prompt.md`) và v2 (`tools.yaml`).

### Đóng góp cụ thể

- Thêm `providers/deepseek_provider.py` và đăng ký trong `run_eval.py`, `chat.py`, `scripts/preflight_provider.py`.
- Chạy v0 (0.45), phân tích 11 case FAIL theo loại lỗi và nguyên nhân.
- v1: bỏ chỉ dẫn đoán/gửi vội/ép một bước, thêm rule hỏi lại, xác nhận trước khi gửi, từ chối ngoài phạm vi (0.45 → 0.65).
- v2: viết lại description 10 tool gốc và quy ước tham số (0.65 → 0.95).

### Bằng chứng

- Commit `b6cabe6` (provider DeepSeek), `aee80bb` (v0 + B2), `2382810` (v1); v2 trên nhánh `feature/tools-v2` (cập nhật hash sau khi commit).
- Run: `starter_v0/runs/v0_B_base_deepseek_20261110T174313805995.json`, `v1_..._20261110T182742199017.json`, `v2_..._20261110T184518723180.json`.
- `starter_v0/artifacts/version_log.csv`, bảng B1 và B2 trong `report/team/group_report.md`.

## Vũ Ngọc Quỳnh Anh

### Phần việc phụ trách

- CP4: thiết kế và viết 10 eval case nhóm trong `data/eval_group.json` (5 single turn + 5 multi turn).
- Chạy group eval qua các version v1, v2, v3 và viết bảng B3 trong group report.

### Đóng góp cụ thể

- Viết case kiểm tra route tới tool mới: G01 (`word_count`), G02 (`source_domains`), GM03 (`citations`).
- Viết case cho các quy ước tham số mà bộ base chưa phủ: G03 (handle có `@`, câu tiếng Anh), G04 (`timeframe=year`), GM05 (đổi `timeframe` week → month).
- Viết case boundary khi gửi: GM01 (đã xác nhận → `send(confirmed=true)`), GM02 (huỷ → không gọi tool), GM04 (sửa nội dung sau khi xác nhận → phải hỏi lại).
- Viết G05 (tên mơ hồ "Apple" → `clarify(response_type="choice")`), case duy nhất test `choice`; fail ổn định ở v1–v3, chỉ ra khoảng trống trong prompt mà bộ base (20/20) không bắt được.
- Thay GM04 cũ (`clarify_then_word_count`) bằng `GM04_reconfirm_after_edit` để test boundary chặt hơn.
- Kết quả group: v1 7/10 → v2 9/10 → v3 9/10.

### Bằng chứng

- Commit `5684527` (10 case + run v1/v2 + bảng B3), `8ff7412` (run v3), `011b9ce` (B3 v3 + giải thích G05).
- Run: `starter_v0/runs/v1_B_group_deepseek_20261110T184513176042.json`, `v2_B_group_deepseek_20261110T190540806261.json`, `v3_B_group_deepseek_20261110T191743257537.json`.
- Bảng B3 trong `report/team/group_report.md`.
