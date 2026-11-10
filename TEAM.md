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
<<<<<<< HEAD
|   1 | Vũ Ngọc Quỳnh Anh | 2A202603875 | 26ai.anhvnq@vinuni.edu.vn | qavu2407-lang | CP4: 10 eval case nhóm (5 single + 5 multi turn), chạy group eval v1–v3, phân tích B3; bonus Test challenge (0 skipped) |
|   2 | Nguyễn Thảo Quyên |   2A202603895   |   26ai.quyennt@vinuni.edu.vn    |    100678carwyn   | CP1–CP2: provider DeepSeek, baseline v0, tối ưu prompt (v1) và tools.yaml (v2) |
=======
|   1 | Vũ Ngọc Quỳnh Anh | 2A202603875 | 26ai.anhvnq@vinuni.edu.vn | qavu2407-lang | CP4: 10 eval case nhóm (5 single + 5 multi turn), chạy group eval v1–v3, phân tích B3 |
|   2 | Nguyễn Thảo Quyên |   2A202603895   |   26ai.quyennt@vinuni.edu.vn    |    100678carwyn   | CP1–CP2: provider DeepSeek, baseline v0, tối ưu prompt (v1, v3) và tools.yaml (v2); bonus: gửi Telegram thật |
>>>>>>> origin/docs/live-chat-telegram-evidence
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
- CP2: tối ưu v1 (`system_prompt.md`), v2 (`tools.yaml`) và v3 (`system_prompt.md`).
- Bonus: gửi Telegram thật sau khi người dùng xác nhận; chat live bản v3 để lấy transcript.

### Đóng góp cụ thể

- Thêm `providers/deepseek_provider.py` và đăng ký trong `run_eval.py`, `chat.py`, `scripts/preflight_provider.py`.
- Chạy v0 (0.45), phân tích 11 case FAIL theo loại lỗi và nguyên nhân.
- v1: bỏ chỉ dẫn đoán/gửi vội/ép một bước, thêm rule hỏi lại, xác nhận trước khi gửi, từ chối ngoài phạm vi (0.45 → 0.65).
- v2: viết lại description 10 tool gốc và quy ước tham số (0.65 → 0.95).
- v3: tách xác nhận gửi/đăng thành hai bước, `yes_no` trước rồi mới hỏi nội dung (0.95 → 1.00 trên bộ base).
- Telegram: tạo bot và kênh private, cấu hình `.env` (gitignored), chat live 7 lượt bằng v3, `send(confirmed=true)` trả `status: sent`; quét `transcripts/` và `runs/` không có token.
- Viết B1, B2, A2, A3, B6 và phần Telegram của B4/B5 trong `report/team/group_report.md`.

### Bằng chứng

- Commit `b6cabe6` (provider DeepSeek), `aee80bb` (v0 + B2), `2382810` (v1), `2b10ae5` (v2), `415cd21` (v3); Telegram trên nhánh `docs/live-chat-telegram-evidence`.
- Run: `starter_v0/runs/v0_B_base_deepseek_20261110T174313805995.json`, `v1_..._20261110T182742199017.json`, `v2_..._20261110T184518723180.json`, `v3_..._20261110T190413436138.json`.
- Transcript Telegram: `starter_v0/transcripts/v3_deepseek_20261111T000241323945.transcript.json`.
- `starter_v0/artifacts/version_log.csv`, bảng B1, B2, B4 và B5 trong `report/team/group_report.md`.
- Báo cáo cá nhân: [2A202603895_NguyenThaoQuyen.md](report/team/2A202603895_NguyenThaoQuyen.md).

## Vũ Ngọc Quỳnh Anh

### Phần việc phụ trách

- CP4: thiết kế và viết 10 eval case nhóm trong `data/eval_group.json` (5 single turn + 5 multi turn).
- Chạy group eval qua các version v1, v2, v3 và viết bảng B3 trong group report.
- Bonus Test challenge (Step 4b): điền các stub test còn skip, cập nhật mục B5.

### Đóng góp cụ thể

- Viết case kiểm tra route tới tool mới: G01 (`word_count`), G02 (`source_domains`), GM03 (`citations`).
- Viết case cho các quy ước tham số mà bộ base chưa phủ: G03 (handle có `@`, câu tiếng Anh), G04 (`timeframe=year`), GM05 (đổi `timeframe` week → month).
- Viết case boundary khi gửi: GM01 (đã xác nhận → `send(confirmed=true)`), GM02 (huỷ → không gọi tool), GM04 (sửa nội dung sau khi xác nhận → phải hỏi lại).
- Viết G05 (tên mơ hồ "Apple" → `clarify(response_type="choice")`), case duy nhất test `choice`; fail ổn định ở v1–v3, chỉ ra khoảng trống trong prompt mà bộ base (20/20) không bắt được.
- Thay GM04 cũ (`clarify_then_word_count`) bằng `GM04_reconfirm_after_edit` để test boundary chặt hơn.
- Kết quả group: v1 7/10 → v2 9/10 → v3 9/10.
- Viết 14 unit test cho tool có sẵn trong `starter_v0/tests/test_tools_todo.py`, xoá 3 stub mẫu; toàn suite 110 passed, 0 skipped, 0 failed.

### Bằng chứng

- Commit `5684527` (10 case + run v1/v2 + bảng B3), `8ff7412` (run v3), `011b9ce` (B3 v3 + giải thích G05).
- Run: `starter_v0/runs/v1_B_group_deepseek_20261110T184513176042.json`, `v2_B_group_deepseek_20261110T190540806261.json`, `v3_B_group_deepseek_20261110T191743257537.json`.
- Bảng B3 trong `report/team/group_report.md`.
- Test challenge: `starter_v0/tests/test_tools_todo.py`, mục B5 trong `report/team/group_report.md`.

## Hồ Nguyễn Minh Sang — 2A202603905

### Phần việc phụ trách

- CP3: xây dựng tool mới, tài liệu contract, đăng ký tool và unit test.
- CP5: UI Streamlit, hướng dẫn chạy, link dùng thử, transcript live và phần báo cáo tương ứng.
- Bonus: tool thứ tư `extract_links` và Small Local Model Challenge qua Ollama.
- Quản lý repo nhóm: kiểm tra, xử lý xung đột và merge PR vào nhánh `main`.

### Đóng góp cụ thể

- Viết ba tool local `citations` (định dạng danh sách nguồn), `source_domains`
  (lấy hostname duy nhất), `word_count` (đếm từ/ký tự); viết `TOOL.md`, đăng ký
  trong `tools/__init__.py` và `artifacts/tools.yaml`, bổ sung 9 unit test
  kiểm tra đầu vào hợp lệ, input sai và nhánh lỗi.
- Tạo giao diện chat tối giản, theme sáng đồng nhất, cấu hình provider/model/version,
  hiển thị hoạt động và lỗi, lưu/tải transcript. Mỗi phiên giữ nguyên prompt/tools và hash.
- Kiểm tra UI qua Cloudflare Tunnel, thử desktop/mobile; chạy lại CLI trên v3 sau khi merge CP2.
- Thêm case mẫu `G_CP3_citations_existing_source` để kiểm tra route tool mới trước
  tích hợp CP4. Sau tích hợp, bộ chính giữ 10 case CP4, gồm G01/G02/GM03 phủ ba tool mới;
  run 1/1 của case mẫu được giữ làm bằng chứng lịch sử.
- Tái sử dụng `chat.run_model_tool_loop` cho UI, giữ cùng backend với CLI;
  chạy transcript v3 kiểm tra tìm tin, đọc nguồn, gọi ba tool mới, hỏi URL còn
  thiếu và hỏi xác nhận trước khi gửi. Phân biệt test offline với log model thật.
- Bổ sung tool thứ tư `extract_links` để trích URL HTTP(S) duy nhất từ văn bản,
  giữ thứ tự và bỏ trùng; viết tài liệu, đăng ký, 3 test và bộ eval bonus riêng.
  Run routing đạt 2/2, không thay đổi bộ eval nhóm 10 case.
- Thực hiện Small Local Model Challenge với Llama 3.2 3B và Qwen 2.5 1.5B;
  xây dựng hai vòng prompt local, so sánh Qwen với cùng giới hạn sinh:
  6/20 → 7/20 → 9/20. Chạy cloud đối chiếu và kiểm tra ngược prompt v5 đạt 20/20;
  lưu cấu hình tái hiện, prompt, run JSON, metric và hash trong version log;
  phân tích lỗi và giới hạn của kết quả tại B7 báo cáo nhóm.
- Bổ sung hướng dẫn chạy và bằng chứng CP3/CP5, sửa lỗi mã hóa tiếng Việt,
  hoàn thiện tài liệu tham khảo và các mục bonus liên quan trong báo cáo nhóm.
- Quản lý repo, review và tích hợp PR của các thành viên vào `main`; phối hợp
  xử lý conflict, đối chiếu quy định nộp bài, chạy test sau tích hợp, kiểm tra
  secret trong log và loại file tạm khỏi phần nộp. Phần viết test challenge 4b
  và gửi Telegram thật do hai thành viên khác thực hiện.

### Bằng chứng

- Commit `60a1efa` (tool/test), `c7f23ac` (UI/evidence), `4ec301c` (tích hợp PR vào main).
- Commit `fde2934`: tool thứ tư, eval routing 2/2 và bằng chứng bonus local.
- Code: `starter_v0/tools/{citations,source_domains,word_count,extract_links}/`,
  `starter_v0/app.py`, `starter_v0/ui_session.py`; test tool và UI trong `starter_v0/tests/`.
- Run tool thứ tư: `starter_v0/runs/v3-bonus4_B_group_openrouter_20261110T235346123648.json`.
- Bonus local: `starter_v0/artifacts/system_prompt_local_v4.md`,
  `starter_v0/artifacts/system_prompt_local_v5.md`, `starter_v0/artifacts/ollama_qwen_eval.json`,
  `starter_v0/artifacts/tools_cloud_v3.yaml`; các run dẫn ở B7 và `starter_v0/artifacts/version_log.csv`.
- Báo cáo nhóm: hướng dẫn UI tại A1, bằng chứng CP3/CP5 tại B4/B5,
  bonus local tại B7 và phần tài liệu tham khảo.
- Báo cáo cá nhân: [2A202603905_HoNguyenMinhSang.md](report/team/2A202603905_HoNguyenMinhSang.md).
- Run routing: `starter_v0/runs/v3-cp3-routing_B_group_openrouter_20261110T194332874245.json` (1/1 đạt).
- Transcript v3: `starter_v0/transcripts/v3_openrouter_20261110T194205268170.transcript.json`
  và `v3_openrouter_20261110T194257230039.transcript.json`.
