# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. **Xong trước Team showdown (16:30)** để team khác hiểu nhanh agent có tool gì, làm được gì. Có thể làm thêm poster `report/team/poster.html` hoặc `poster.svg`.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật. Hoàn thiện trước deadline nộp bài.
>
> Mỗi bảng phải trỏ được tới file thật: run JSON, transcript, commit. Cách chấm xem [RUBRIC.md](../../RUBRIC.md).

## 1. Thông tin nhóm

- Tên nhóm:
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md)
- Provider/model dùng cho v0–v3: deepseek / `deepseek-chat`

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent

### A1. Agent này làm được gì

> 1–2 câu mô tả agent dùng để làm gì (cho team khác hiểu nhanh).

Ví dụ: "Research agent: tìm tin theo từ khóa / theo tài khoản, đọc URL, tổng hợp thành digest, và gửi lên Telegram khi được xác nhận."

**Cách chạy UI:**

> Lệnh chạy UI (ví dụ `streamlit run app.py`) và dependency đã thêm vào `starter_v0/requirements.txt`.

**Link dùng thử (deploy):**

> Dán link public để team khác mở thử ngay. Cách deploy nhanh bằng Cloudflare Tunnel xem README. Nếu deploy Vercel/Streamlit Cloud thì dán link đó.
>
> URL:

### A2. Tool agent có

> Liệt kê các tool agent đang dùng (gồm tool mới nhóm tự thêm). Mỗi tool 1 dòng: tên + làm được gì.

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | hỏi lại người dùng khi thiếu thông tin | không |
|  |  |  |
|  |  |  |

### A3. Câu hỏi mẫu để thử

> 3–5 câu hỏi/yêu cầu mẫu để team khác tự thử agent ngay.

1.
2.
3.

## 3. Giải pháp

> Tóm tắt các thay đổi chính trong `starter_v0/artifacts/system_prompt.md` và `starter_v0/artifacts/tools.yaml`, và tool mới nhóm viết (tên, làm gì, khi nào agent nên gọi).

-

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Lấy từ `starter_v0/artifacts/version_log.csv` và `starter_v0/runs/*.json`. Chỉ dùng run có `provider_error_cases == 0` và `measured_cases == total_cases`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline | Đo hành vi chưa tối ưu trước khi sửa | – | 0.45 (case_accuracy; routing 0.60, args 0.45, multiturn 0.67) | `starter_v0/runs/v0_B_base_deepseek_20261110T174313805995.json` |
| v1 |  |  |  |  |  |
| v2 |  |  |  |  |  |
| v3 |  |  |  |  |  |

### B2. Failure Analysis

Lấy từ `results[*].result.failures` trong run JSON.

Run v0: 9/20 PASS (`case_accuracy` 0.45), `provider_error_cases == 0`, `measured_cases == total_cases == 20`. Run file: `starter_v0/runs/v0_B_base_deepseek_20261110T174313805995.json`.

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| R10_missing_handle | missing_info | `timeline(screenname=sama, limit=5)` | Không nói handle nhưng model đoán `sama` thay vì `clarify` (prompt bảo "pick a well-known account") | Prompt: thiếu handle thì gọi `clarify` |
| R11_missing_url | missing_info | `fetch(url=https://www.theverge.com/)` | Không có URL nhưng model đoán URL (prompt bảo "assume a likely URL") | Prompt: thiếu URL thì gọi `clarify` |
| R12_confirm_before_send | wrong_boundary | `send(text=<tự bịa bản tin>, confirmed=true)` | Gửi ngay với `confirmed=true`, không hỏi xác nhận, nội dung tự bịa (prompt bảo "just go ahead") | Prompt + `tools.yaml`: chỉ `send` sau khi user xác nhận |
| R08_out_of_scope | out_of_scope | `send(text=<lời giải nguyên hàm>, confirmed=true)` | Câu hỏi toán ngoài phạm vi, model gửi câu trả lời lên Telegram thay vì trả lời text | Prompt: ngoài phạm vi thì trả lời text, không gọi tool |
| R14_out_of_scope_coding | out_of_scope | `send(text=<code fibonacci>, confirmed=true)` | Như R08 với câu hỏi viết code | Như R08 |
| R02_search_tweets_routing | wrong_tool (extra_tool_call) | `social_search(GPT-5, Top)` + `social_search(GPT-5, Latest)` | Đúng tool nhưng gọi thừa lần thứ hai | Prompt: một yêu cầu một lần gọi, không lặp tool |
| R06_timeframe_arg | wrong_arg_value (extra_tool_call) | `lookup(timeframe=week)` ×2 (query tiếng Việt, rồi tiếng Anh) | Gọi lặp `lookup` với query dịch sang tiếng Anh | Như R02 |
| R03_web_news_routing | wrong_tool | `lookup(query="tin tức AI nổi bật hôm nay", topic=news)` + `social_search` | `query` bị mở rộng (expected `AI`), thêm `social_search` thừa | `tools.yaml`: `query` là từ khoá ngắn, không thêm "tin tức", "hôm nay" vì đã có `topic`, `timeframe`; chỉ dùng tool được hỏi |
| R13_parallel_web_and_tweets | wrong_tool (wrong_arg_value) | `lookup(query="tin tức AI hôm nay")` + `social_search(AI)` | Đúng 2 tool nhưng `query` của `lookup` bị mở rộng | Như R03 |
| M02_carryover_timeframe | wrong_arg_value | `lookup(query="robotics news", timeframe=day)` | Thêm "news" vào query (expected `robotics`) | Như R03 |
| M06_switch_tool | wrong_tool (wrong_arg_value) | `lookup(query="OpenAI news", timeframe=week)` | Thêm "news" vào query (expected `OpenAI`) | Như R03 |

Nhóm nguyên nhân: (1) prompt khuyến khích đoán → R10, R11, R12; (2) thiếu boundary khi gửi và ngoài phạm vi → R08, R12, R14; (3) thiếu convention của `query`/gọi lặp trong `tools.yaml` → R02, R03, R06, R13, M02, M06.

### B3. Team Eval Cases

Liệt kê đúng 10 case trong `starter_v0/data/eval_group.json` (5 single turn + 5 multi turn).

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
|  |  |  |  |

### B4. Live Chat Evidence

Lấy từ `starter_v0/transcripts/*.transcript.json`.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
|  |  |  |  |  |

### B5a. Bằng chứng bắt buộc — Tool mới, unit test, UI

| Hạng mục | File bằng chứng | Kết quả | Giới hạn / Kiểm soát |
|---|---|---|---|
| Tool mới `citations` | `starter_v0/tools/citations/`, `starter_v0/tools/__init__.py`, `starter_v0/artifacts/tools.yaml` | Định dạng các nguồn đã có thành danh sách tài liệu tham khảo đánh số. | Không tự truy xuất hoặc xác minh nguồn; từ chối URL không hợp lệ. |
| Tool mới `source_domains` | `starter_v0/tools/source_domains/` | Trích xuất các hostname duy nhất từ danh sách URL nguồn. | Không truy xuất hoặc xác minh website. |
| Tool mới `word_count` | `starter_v0/tools/word_count/` | Đếm số từ và ký tự trong văn bản được cung cấp. | Đếm theo quy tắc nhận diện từ cục bộ; không tóm tắt nội dung. |
| Unit test các tool mới | `starter_v0/tests/test_tools_todo.py` | 9 test mới đạt; toàn bộ suite: 86 passed, 17 skipped, 0 failed. | Test chạy offline, không gửi yêu cầu mạng. |
| UI (lệnh chạy + link dùng thử) | Chưa hoàn thành | Chưa hoàn thành | Chưa hoàn thành |

Mỗi tool có các test cho đầu vào hợp lệ, đầu vào sai và nhánh lỗi. Ví dụ, unit test kiểm tra URL không hợp lệ được trả về dưới dạng error dict; eval routing không chứng minh được code tool xử lý đúng đầu vào đó.

### B5. Bonus Evidence

Chỉ điền nếu nhóm làm bonus (ghi riêng, tối đa 10 điểm). Tool có sẵn (`send`, `policy`, `papers`, `paper_text`) không tự được bonus.

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Small Local Model | xem B7 |  |  |
| Hơn 3 tool mới (≥ 4) |  |  |  |
| `send` gửi thật lên Telegram sau xác nhận | transcript |  |  |
| Test challenge (0 skipped / regression test) | `pytest` output |  |  |

Test challenge: số bug tìm được trong tool có sẵn (nếu có), cách sửa, và test regression tương ứng.

### B7. Small Local Model Challenge (bonus)

Chỉ điền nếu nhóm làm bonus này.

| Version | Model (provider) | Prompt/Tools | case_accuracy | tool_routing | argument | multiturn | Run File |
|---|---|---|---|---|---|---|---|
| v3 | (cloud) | v3 |  |  |  |  |  |
| v3-<model> | (ollama) | v3 |  |  |  |  |  |
| v3-<model> | (ollama) | v3 |  |  |  |  |  |
| v4-local |  |  |  |  |  |  |  |
| v5-local |  |  |  |  |  |  |  |

Lỗi đặc thù của model nhỏ (đếm từ run JSON):

| Failure Pattern | Count | Example Case | Fix Tried | Helped? |
|---|---|---|---|---|
| wrong / hallucinated tool |  |  |  |  |
| invalid JSON args (`_invalid_json_arguments`) |  |  |  |  |
| no tool call / answered directly |  |  |  |  |
| missed `clarify` |  |  |  |  |
| repeated / unnecessary calls |  |  |  |  |

- Cái gì giúp model nhỏ gọi tool đúng hơn nhất? Bằng chứng?
- Bản prompt tối ưu cho local chạy trên model cloud thì sao?
- Khi nào nhóm sẽ chọn model local thay vì cloud cho agent này?

## 5. Khó khăn và cách xử lý

> Khó khăn chính và cách nhóm xử lý. Nếu gặp lỗi kỹ thuật (provider lỗi, hết quota API, tool không chạy), mô tả lỗi và dẫn bằng chứng: run JSON, log, ảnh chụp.

-

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong [TEAM.md](../../TEAM.md) và các báo cáo cá nhân `report/team/MSSV_HoTen.md`.

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- Fix nào thuộc `system_prompt.md`?
- Fix nào thuộc `tools.yaml`?
- Failure nào cần review thủ công thay vì chấm tự động?
- Nếu có thêm một vòng, nhóm sẽ thử giả thuyết nào?

## 8. Tài liệu tham khảo

-
