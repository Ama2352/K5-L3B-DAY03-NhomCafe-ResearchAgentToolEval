# Team

## Thông tin nhóm

- Tên nhóm: NhomCafe
- Lớp: L3B
- Repo nhóm: `K5-L3B-DAY03-NhomCafe-ResearchAgentToolEval`
- URL repo: https://github.com/Ama2352/K5-L3B-DAY03-NhomCafe-ResearchAgentToolEval
- Nhánh nộp: `main`; nhánh đang làm phần CP5: `Sang`.
- Commit chốt: `2c12687` (cập nhật lại khi chốt bài nộp)
- Commit phần UI và bằng chứng CP5: `c7f23ac`.

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 |Vũ Ngọc Quỳnh Anh|2A202603875  |   26ai.anhvnq@vinuni.edu.vn     |    https://github.com/qavu2407-lang    |         |
|   2 | Nguyễn Thảo Quyên |   2A202603895   |   26ai.quyennt@vinuni.edu.vn    |    100678carwyn   | CP1–CP2: provider DeepSeek, baseline v0, tối ưu prompt (v1) và tools.yaml (v2) |
|   3 | Hồ Nguyễn Minh Sang |  2A202603905  |   26ai.sanghnm@vinuni.edu.vn    | Ama2352 | CP3: tool mới + unit test; CP5: UI, transcript, báo cáo; quản lý repo, merge PR |

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

## Hồ Nguyễn Minh Sang — 2A202603905

### Phần việc phụ trách

- CP3: ba tool local `citations`, `source_domains`, `word_count`, đăng ký và unit test.
- CP5: UI Streamlit, hướng dẫn chạy, link dùng thử, transcript live và phần báo cáo tương ứng.
- Quản lý repo nhóm: kiểm tra, xử lý xung đột và merge PR vào nhánh `main`.

### Đóng góp cụ thể

- Bổ sung 9 test cho ba tool; giữ contract registry/declaration/TOOL.md đồng bộ.
- Tạo giao diện chat tối giản, theme sáng đồng nhất, cấu hình provider/model/version,
  hiển thị hoạt động và lỗi, lưu/tải transcript. Mỗi phiên giữ nguyên prompt/tools và hash.
- Kiểm tra UI qua Cloudflare Tunnel, thử desktop/mobile; chạy lại CLI trên v3 sau khi merge CP2.
- Thêm case `G_CP3_citations_existing_source` để kiểm tra route tool mới; bàn giao CP4
  bổ sung 4 single turn và 5 multi turn còn lại, không coi một case này là hoàn thành CP4.
- Có sử dụng Codex hỗ trợ code, test, phân tích log và soạn báo cáo; bằng chứng từ chạy thật.

### Bằng chứng

- Commit `60a1efa` (tool/test), `c7f23ac` (UI/evidence), `4ec301c` (tích hợp PR vào main).
- Báo cáo cá nhân: [2A202603905_HoNguyenMinhSang.md](report/team/2A202603905_HoNguyenMinhSang.md).
- Run routing: `starter_v0/runs/v3-cp3-routing_B_group_openrouter_20261110T194332874245.json` (1/1 đạt).
- Transcript v3: `starter_v0/transcripts/v3_openrouter_20261110T194205268170.transcript.json`
  và `v3_openrouter_20261110T194257230039.transcript.json`.
