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

Café Research hỗ trợ tìm tin web và bài đăng X, đọc URL hoặc paper arXiv,
tra cứu policy nội bộ và tổng hợp nguồn thành digest. Nhóm bổ sung ba tool
định dạng tài liệu tham khảo, thống kê hostname nguồn và đếm từ/ký tự.

**Cách chạy UI:**

Chạy từ `starter_v0/`:

```powershell
.\.venv\Scripts\python.exe -m pip install --no-cache-dir -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py --global.developmentMode false
```

UI: http://localhost:8501. Nhập câu hỏi để bắt đầu; mặc định dùng OpenRouter.
Mở **Cài đặt** trước câu hỏi đầu tiên để đổi provider/model và nhập đúng nhãn
version hiện tại. **Cuộc trò chuyện mới** bắt đầu lại và cho đổi cấu hình.
Trong môi trường kiểm tra
CP5, OpenRouter / `openai/gpt-4o-mini` đã qua preflight; DeepSeek chưa có key.
Dependency Streamlit nằm trong `starter_v0/requirements.txt`.

**Link dùng thử (deploy):**

URL public: https://weeks-yield-consolidated-dom.trycloudflare.com

Đã mở giao diện qua link HTTPS, gửi câu hỏi đếm từ và tải transcript thành công.
Link Cloudflare Quick Tunnel là tạm thời, chỉ hoạt động khi Streamlit và tunnel
còn chạy. Hướng dẫn mở lại và kịch bản demo: [starter_v0/README.md](../../starter_v0/README.md).
Phần A được bổ sung ở giai đoạn hoàn thiện bài; không có bằng chứng đã xong trước 16:30.

### A2. Tool agent có

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | hỏi lại người dùng khi thiếu thông tin | không |
| timeline | lấy bài đăng của một tài khoản X | không |
| social_search | tìm bài đăng X theo từ khóa | không |
| lookup | tìm web/tin tức theo chủ đề và thời gian | không |
| fetch | đọc nội dung một URL | không |
| format | định dạng các item có sẵn thành digest | không |
| policy | tìm trong bộ policy nội bộ | không |
| papers | tìm paper arXiv | không |
| paper_text | tải và trích text PDF arXiv | không |
| send | gửi Telegram khi có xác nhận và cấu hình channel | không |
| citations | định dạng tiêu đề/URL thành danh sách tham khảo | có |
| source_domains | trích hostname duy nhất từ các URL | có |
| word_count | đếm từ và ký tự của văn bản | có |

### A3. Câu hỏi mẫu để thử

1. Tìm 3 tin tức AI trong tuần này, kèm link nguồn.
2. Đọc bài viết này giúp tôi. (Kiểm tra agent có hỏi URL; sau đó bổ sung URL.)
3. Đếm số từ trong đoạn: Research agents use tools.
4. Liệt kê hostname duy nhất từ https://example.com/a và https://example.com/b.
5. Chuẩn bị gửi nội dung "Bản tin thử nghiệm CP5" lên Telegram; hãy hỏi tôi xác nhận nội dung trước.

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

Phiên smoke thật chạy bằng `chat.py`, provider OpenRouter / `openai/gpt-4o-mini`:
`starter_v0/transcripts/v0-cp5-smoke_openrouter_20261110T183625534828.transcript.json`.
Artifact: `v0-cp5-smoke+peb1c8179815b+t6a2da240a3cb`.
Đây là snapshot kiểm tra tích hợp CP5, không thay thế baseline v0 hoặc bản v3 CP2.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
| 1 | Đếm số từ trong “Research agents use tools.” | `word_count` | snapshot CP5 nêu trên | Trả 4 từ, 26 ký tự; answered |
| 2 | Đọc bài viết này giúp tôi (không có URL) | `fetch` → `format` | cùng snapshot | FAIL hành vi thiếu thông tin: tự đoán `https://www.example.com/article`, không hỏi lại |
| 3 | Bổ sung URL `https://example.com/` | `fetch` → `format` | cùng snapshot | Đọc URL đã cung cấp và tổng hợp, answered |
| 4 | Chuẩn bị gửi bản tin, chưa xác nhận | `send` → `clarify` | cùng snapshot | Tool trả `needs_confirmation`, agent hỏi xác nhận; không gửi thật. Model vẫn gọi `send` trước khi hỏi, cần CP2 xử lý |

Không có lượt lỗi provider trong phiên này. Cần chạy lại kịch bản trên bản cuối
CP2 để chứng minh agent hỏi URL và xác nhận trước khi gọi action tool.

Kiểm tra trực tiếp qua UI public: transcript
`starter_v0/transcripts/cp5-ui-smoke_openrouter_ui_edc771ac423547388a35056c1f686833.transcript.json`,
artifact `cp5-ui-smoke+peb1c8179815b+t6a2da240a3cb`, OpenRouter / `openai/gpt-4o-mini`.
Lượt 1 yêu cầu đếm “Research agents use tools.”; agent gọi `word_count`, trả 4 từ
và 26 ký tự, status `answered`. File tải bằng nút **Tải transcript JSON** khớp
với transcript lưu trên máy chủ. Đây là bằng chứng UI; phiên CLI bốn lượt ở trên
là bằng chứng `chat.py` theo checkpoint.

Sau khi tối giản giao diện, đã kiểm tra lại việc nhập câu hỏi ngay từ màn hình
ban đầu và nút câu hỏi mẫu qua link public. Transcript mới:
`starter_v0/transcripts/v0_openrouter_ui_4a4d770c004f4a5e8617570d239b88cd.transcript.json`.
Lượt đếm từ trả 4 từ, 26 ký tự; bố cục đã kiểm tra ở desktop và mobile 390px,
không tràn ngang. Cài đặt và hoạt động tool được thu gọn; chức năng lưu/tải
transcript và ghi nhận lỗi vẫn được giữ.

### B5a. Bằng chứng bắt buộc — Tool mới, unit test, UI

| Hạng mục | File bằng chứng | Kết quả | Giới hạn / Kiểm soát |
|---|---|---|---|
| Tool mới `citations` | `starter_v0/tools/citations/`, `starter_v0/tools/__init__.py`, `starter_v0/artifacts/tools.yaml` | Định dạng các nguồn đã có thành danh sách tài liệu tham khảo đánh số. | Không tự truy xuất hoặc xác minh nguồn; từ chối URL không hợp lệ. |
| Tool mới `source_domains` | `starter_v0/tools/source_domains/` | Trích xuất các hostname duy nhất từ danh sách URL nguồn. | Không truy xuất hoặc xác minh website. |
| Tool mới `word_count` | `starter_v0/tools/word_count/` | Đếm số từ và ký tự trong văn bản được cung cấp. | Đếm theo quy tắc nhận diện từ cục bộ; không tóm tắt nội dung. |
| Unit test các tool mới | `starter_v0/tests/test_tools_todo.py` | 9 test mới đạt; toàn bộ suite: 86 passed, 17 skipped, 0 failed. | Test chạy offline, không gửi yêu cầu mạng. |
| UI (lệnh chạy + link dùng thử) | `starter_v0/app.py`, `starter_v0/ui_session.py`, `starter_v0/README.md`; transcript UI ở B4 | Giao diện chat Streamlit đã chạy qua link public; chọn cấu hình, xem tool/lỗi, lưu và tải transcript; lệnh và URL ở A1 | Link tunnel tạm thời; hành vi model phụ thuộc prompt/tools CP2 |
| Kiểm thử tích hợp CP5 | `starter_v0/tests/test_ui_session.py`, `starter_v0/tests/test_app.py` | 6 test mới đạt; toàn suite 92 passed, 17 skipped, 0 failed | Test offline không thay thế transcript live; các stub có sẵn vẫn skip |

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

- Môi trường kiểm tra không cho ghi thêm package vào `.venv` hiện có, và pip bị
  kẹt khi ghi cache. Đã cài dependency vào thư mục tạm ngoài repo bằng
  `--target`, `--no-cache-dir`, `--no-compile` để chạy kiểm thử ban đầu. Sau đó đã
  cài Streamlit trực tiếp vào `.venv` và chạy lại toàn suite thành công
  (92 passed, 17 skipped). Không đưa package hoặc file build vào bài nộp.
- Streamlit trong môi trường kiểm tra mặc định bật development mode khiến trang
  gốc trả 404 dù health endpoint báo OK. Chạy với `--global.developmentMode false`
  đã phục vụ trang và chat bình thường. Đã kiểm tra cả HTTP và giao diện public.
- Snapshot hiện tại đoán URL khi thiếu thông tin, và gọi `send` trước khi hỏi
  xác nhận (tool chặn gửi). Bằng chứng thật ở B4; bàn giao CP2 để sửa prompt/tool
  declaration rồi chạy lại trên bản cuối. Không sửa các file CP2/CP4 trong phần CP5.

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong [TEAM.md](../../TEAM.md) và các báo cáo cá nhân `report/team/MSSV_HoTen.md`.

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- Fix nào thuộc `system_prompt.md`?
- Fix nào thuộc `tools.yaml`?
- Failure nào cần review thủ công thay vì chấm tự động?
- Nếu có thêm một vòng, nhóm sẽ thử giả thuyết nào?

## 8. Tài liệu tham khảo

-
