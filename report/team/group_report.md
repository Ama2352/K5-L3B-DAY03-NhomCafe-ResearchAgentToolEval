# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. **Xong trước Team showdown (16:30)** để team khác hiểu nhanh agent có tool gì, làm được gì. Có thể làm thêm poster `report/team/poster.html` hoặc `poster.svg`.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật. Hoàn thiện trước deadline nộp bài.
>
> Mỗi bảng phải trỏ được tới file thật: run JSON, transcript, commit. Cách chấm xem [RUBRIC.md](../../RUBRIC.md).

## 1. Thông tin nhóm

- Tên nhóm: NhomCafe
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
| clarify | hỏi lại người dùng khi thiếu thông tin (handle, URL, nội dung) và xin xác nhận có/không trước khi gửi | không |
| timeline | lấy các bài đăng gần đây của một tài khoản X/Twitter | không |
| social_search | tìm bài đăng X/Twitter theo từ khóa (Top/Latest) | không |
| lookup | tìm tin tức/thông tin trên web (`topic=news`, `timeframe`) | không |
| fetch | đọc nội dung của một URL do người dùng đưa | không |
| format | trình bày các item đã có thành bản tin markdown | không |
| send | gửi văn bản lên Telegram, chỉ sau khi người dùng xác nhận (`confirmed=true`) | không |
| policy | tìm trong tài liệu chính sách nội bộ | không |
| papers | tìm bài báo trên arXiv | không |
| paper_text | tải và trích text của một bài arXiv | không |
| citations | tạo danh sách tài liệu tham khảo đánh số từ tiêu đề và URL đã có | có |
| source_domains | lấy các hostname duy nhất từ danh sách URL nguồn | có |
| word_count | đếm từ và ký tự trong văn bản được cung cấp | có |

### A3. C?u h?i m?u ?? th?

1. Tìm 3 tin tức AI trong tuần này, kèm link nguồn.
2. Tweet mới nhất của Sam Altman là gì?
3. Đọc bài viết này giúp tôi. (Kiểm tra agent hỏi URL, rồi bổ sung URL.)
4. Đếm số từ trong đoạn: Research agents use tools.
5. Chuẩn bị gửi bản tin lên Telegram và hỏi xác nhận trước khi gửi.

## 3. Giải pháp

- **`system_prompt.md` (v1):** bỏ 3 chỉ dẫn xấu của starter (đoán thay vì hỏi, gửi ngay, ép một bước). Thêm rule: thiếu handle/URL thì gọi `clarify`; xin xác nhận `yes_no` trước khi `send`; câu ngoài phạm vi thì từ chối bằng text, không gọi tool.
- **`tools.yaml` (v2):** viết lại `description` của 10 tool gốc theo mẫu làm gì / khi nào dùng / khi nào không dùng. Quy ước tham số: `query` của `lookup` là từ khóa ngắn (không thêm "tin tức", "hôm nay"), `topic=news`, bảng `timeframe`, handle không có `@`, `search_type` Top/Latest, gọi một lần mỗi yêu cầu, `send` chỉ khi đã xác nhận.
- **Tool mới (CP3):** `citations` (tạo danh sách tham khảo đánh số từ title + URL), `source_domains` (lấy hostname duy nhất từ danh sách URL), `word_count` (đếm từ/ký tự). Cả ba chạy local, lỗi trả error dict. Agent gọi khi đã có dữ liệu nguồn hoặc văn bản cần đếm.

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Lấy từ `starter_v0/artifacts/version_log.csv` và `starter_v0/runs/*.json`. Chỉ dùng run có `provider_error_cases == 0` và `measured_cases == total_cases`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline | Đo hành vi chưa tối ưu trước khi sửa | – | 0.45 (case_accuracy; routing 0.60, args 0.45, multiturn 0.67) | `starter_v0/runs/v0_B_base_deepseek_20261110T174313805995.json` |
| v1 | `system_prompt.md` | Prompt gốc khuyến khích đoán và làm vội; thay bằng rule hỏi lại (`clarify`), xác nhận trước `send`, từ chối ngoài phạm vi | 0.45 | 0.65 (routing 0.80, args 0.65, multiturn 0.67); pass 9→13/20; sửa R08, R10, R11, R14 | `starter_v0/runs/v1_B_base_deepseek_20261110T182742199017.json` |
| v2 | `tools.yaml` (kèm 3 tool CP3 đã merge) | Mô tả tool một dòng nên model mở rộng `query`, gọi thừa `social_search`; viết lại description + quy ước tham số | 0.65 | 0.95 (routing 1.00, args 0.95, multiturn 1.00); pass 13→19/20; sửa R02, R03, R06, R13, M02, M06; còn R12 (`clarify` dùng `text` thay vì `yes_no`) | `starter_v0/runs/v2_B_base_deepseek_20261110T184518723180.json` |
| v3 | `system_prompt.md` | Model dùng `text` ở R12 vì prompt chưa tách xác nhận ý định gửi khỏi xin nội dung; tách thành 2 bước (`yes_no` trước, `text` sau) | 0.95 | 1.00 (routing 1.00, args 1.00, multiturn 1.00); pass 19→20/20; sửa R12, không case nào tụt | `starter_v0/runs/v3_B_base_deepseek_20261110T190413436138.json` |

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

Runs (deepseek-chat):
- v1: `starter_v0/runs/v1_B_group_deepseek_20261110T184513176042.json` — **7/10 PASS (0.70)** (chạy với GM04 cũ `GM04_clarify_then_word_count`, đã thay sau đó)
- v2: `starter_v0/runs/v2_B_group_deepseek_20261110T190540806261.json` — **9/10 PASS (0.90)** (bộ case hiện tại)
- v3: `starter_v0/runs/v3_B_group_deepseek_20261110T191743257537.json` — **9/10 PASS (0.90)** (bộ case hiện tại, version chốt)

| Case ID | What It Tests | Expected Tool/Behavior | Result v1 | Result v2 | Result v3 |
|---|---|---|---|---|---|
| G01_word_count_route | Yêu cầu đếm từ → route tới tool mới `word_count`, truyền nguyên văn text | `word_count(text="Hôm nay trời đẹp quá")` | PASS | PASS | PASS |
| G02_source_domains_route | Hỏi tên miền của các URL đã có → dùng tool mới `source_domains`, không `fetch` | `source_domains(urls=[3 URL])` | PASS | PASS | PASS |
| G03_handle_strip_at_english | Câu tiếng Anh, handle có `@` → bỏ `@`, giữ `limit` | `timeline(screenname="karpathy", limit=3)` | PASS | PASS | PASS |
| G04_timeframe_year | "năm nay" → `timeframe=year` (base chỉ test day/week) | `lookup(topic="news", timeframe="year")` | FAIL — `timeframe=week` + gọi thừa `social_search` | PASS | PASS |
| G05_ambiguous_choice | "Apple" mơ hồ (công ty/trái cây) → hỏi lại dạng lựa chọn thay vì đoán | `clarify(response_type="choice")` | FAIL — gọi luôn `lookup` + `social_search` | FAIL — gọi luôn `lookup(query="Apple")` | FAIL — gọi luôn `lookup(query="Apple", timeframe="week")` |
| GM01_confirm_then_send | Lượt 2 user đã xác nhận → gửi với `confirmed=true` | `send(confirmed=true)` | PASS | PASS | PASS |
| GM02_cancel_send | User huỷ ở lượt 2 → không gọi tool nào | `no_tool` | PASS | PASS | PASS |
| GM03_citations_after_sources | Dùng nguồn user đưa ở lượt 1 cho tool mới `citations`, không search lại | `citations` (chỉ chấm tên tool) | PASS | PASS | PASS |
| GM04_reconfirm_after_edit | User đã xác nhận ở lượt 2 nhưng lượt 3 sửa nội dung → phải hỏi xác nhận lại với nội dung mới, không gửi luôn | `clarify(response_type="yes_no")` | — (case mới, thay GM04 cũ) | PASS | PASS |
| GM05_timeframe_widen | Giữ `topic=news`, đổi `timeframe` week → month theo lượt 2 | `lookup(topic="news", timeframe="month")` | FAIL — args đúng nhưng gọi thừa `social_search` | PASS | PASS |

Nhận xét: v2 (viết lại mô tả tool + bảng `timeframe`) sửa được 2 lỗi gọi thừa `social_search` (G04, GM05) và lỗi `timeframe=year` (G04). v3 chỉ sửa rule xác nhận trước khi `send` nên kết quả bộ group giữ nguyên 9/10; các case boundary (GM01, GM02, GM04) vẫn PASS, không case nào tụt.

**Vì sao giữ G05 dù bộ base đã đạt 1.00:**

- **Lỗi có thật và lặp lại ổn định:** fail ở cả v1, v2, v3 với cùng một hành vi — model không hỏi lại mà tự chọn nghĩa "Apple = công ty" rồi gọi `lookup`. Đây là lỗi duy nhất bộ base (20/20 ở v3) không phát hiện ra.
- **Phủ phần chưa ai test:** `clarify` có 3 giá trị `response_type` (`text`, `yes_no`, `choice`). Bộ base và extension chỉ test `text` và `yes_no`; G05 là case duy nhất test `choice`.
- **Đúng nguyên tắc của prompt:** prompt yêu cầu không đoán khi thiếu thông tin (R10, R11). Một tên có nhiều nghĩa là thông tin chưa đủ để chọn đúng nguồn; model đoán thay vì để user chọn.
- **Nguyên nhân gốc:** `system_prompt.md` (dòng 7) chỉ nói gọi `clarify` khi **thiếu** chi tiết (handle, URL), không có rule cho trường hợp **mơ hồ**, và không nhắc tới `response_type="choice"` → model không có lý do để hỏi.
- **Giới hạn của case (tự nhận):** "tìm **tin** về Apple" nghiêng mạnh về nghĩa công ty (Tavily cũng trả về Apple Inc.), nên hành vi của model có thể coi là hợp lý với người dùng thông thường. Vì vậy G05 nên đọc là bằng chứng cho một **khoảng trống trong prompt** (không có rule xử lý tên mơ hồ), không phải model trả lời sai hoàn toàn. Hướng cải thiện cho vòng sau: thêm rule "tên có nhiều nghĩa → `clarify(response_type="choice")` liệt kê các nghĩa", và cân nhắc thêm case với tên mơ hồ rõ hơn (ví dụ `timeline` cho "Jordan", nơi đoán sai handle là lỗi thật).

Run CP3 lịch sử `starter_v0/runs/v3-cp3-routing_B_group_openrouter_20261110T194332874245.json`
đạt 1/1, 0 lỗi provider cho case mẫu `G_CP3_citations_existing_source` trước khi
hợp nhất CP4. Khi tích hợp PR #8/#9, giữ đúng bộ 10 case CP4 ở trên; case mẫu
được thay bằng độ phủ G01, G02 và GM03 cho cả ba tool mới. Run 1/1 không phải
kết quả chạy lại bộ CP4 hiện tại.

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

Không có lượt lỗi provider trong phiên cũ này. Đã chạy lại trên bản cuối CP2
như phần bằng chứng v3 bên dưới; giữ log cũ để thể hiện lỗi trước tối ưu.

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

**Phiên chat live bản v3 (DeepSeek `deepseek-chat`, 7 lượt, chạy bằng `chat.py`):**
`starter_v0/transcripts/v3_deepseek_20261111T000241323945.transcript.json`,
artifact `v3+p0b60553f4971+t256b66de201d`. Phiên này chạy sau khi tối ưu CP2 nên là bằng chứng so sánh với phiên v0 ở trên.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
| 1 | tweet mới nhất của Sam Altman là gì? | `timeline(screenname=sama, limit=5)` | v3 | Trả tweet mới nhất kèm link; answered |
| 2 | tóm tắt 5 tweet mới nhất giúp mình | `timeline(screenname=sama, limit=5)` | v3 | Không hỏi lại tài khoản vì lượt 1 đã nêu Sam Altman; suy ra từ ngữ cảnh, hợp lý |
| 3 | trình bày bình thường là được, không cần đào sâu | (không gọi tool) | v3 | Trình bày lại từ dữ liệu đã có |
| 4 | đọc giúp mình báo cáo này đi (không có URL) | (không gọi tool) | v3 | Hỏi lại xin link bằng văn bản, không đoán URL. Khác phiên v0 ở trên (agent từng đoán `https://www.example.com/article`), nhưng hai phiên dùng model khác nhau (OpenRouter `gpt-4o-mini` và DeepSeek `deepseek-chat`) nên không phải so sánh trực tiếp |
| 5 | https://example.com | `fetch(url=https://example.com)` | v3 | Đọc đúng URL vừa bổ sung; nhận xét đây là trang ví dụ, không phải báo cáo |
| 6 | đăng lên telegram: bản tin thử nghiệm của Nhomcafe | (không gọi tool) | v3 | Hỏi xác nhận trước khi đăng, chưa gửi |
| 7 | đồng ý gửi đi | `send(text=..., confirmed=true)` | v3 | Tool trả `status: sent`; tin nhắn hiện trong kênh Telegram private của nhóm |

Nhận xét: ở lượt 4 và 6 agent hỏi lại bằng văn bản chứ không gọi tool `clarify`, khác với eval base mong đợi `clarify`. Hành vi vẫn đúng (hỏi trước, không đoán, không gửi khi chưa xác nhận). Một phiên chat chưa đủ để kết luận nguyên nhân (có thể chỉ là biến thiên giữa các lần chạy của model); cần review thủ công nếu muốn kết luận.

### B5a. Bằng chứng bắt buộc — Tool mới, unit test, UI

**Bằng chứng live sau tích hợp CP2 v3:** OpenRouter / `openai/gpt-4o-mini`,
artifact `v3+pcb7f408bd8ea+te7248b8f4ae5`.
Hash khác run DeepSeek v3 do CRLF/LF; nội dung prompt/tools sau chuẩn hóa xuống dòng khớp.

| Transcript | Lượt | Kết quả thực tế |
|---|---|---|
| `starter_v0/transcripts/v3_openrouter_20261110T194257230039.transcript.json` | 1 | Thiếu URL: hỏi người dùng cung cấp link bằng text, không đoán URL; không gọi tool `clarify` (hạn chế routing) |
| cùng file | 2 | Người dùng bổ sung `https://example.com/`; gọi `fetch`, trả nội dung nguồn |
| cùng file | 3 | Nội dung gửi đã có nhưng chưa xác nhận: gọi `clarify(response_type=yes_no)`, chờ user; không gọi `send` |
| `starter_v0/transcripts/v3_openrouter_20261110T194205268170.transcript.json` | 1 | Gọi `lookup` tìm 3 tin AI trong tuần, trả link nguồn |
| cùng file | 4–6 | Gọi đúng `word_count`, `source_domains`, `citations`; các tool trả kết quả thật |

Cả hai phiên đều không lỗi provider. Phiên 7 lượt đọc một bài đã có trong ngữ
cảnh ở lượt 2; không dùng lượt này làm bằng chứng hỏi lại khi thiếu URL.
Phiên 3 lượt là kiểm tra CLI tự động nhập kịch bản qua `chat.py`, không phải
xác nhận của người ngoài nhóm. Chưa có bằng chứng người ngoài nhóm dùng thử.

| Hạng mục | File bằng chứng | Kết quả | Giới hạn / Kiểm soát |
|---|---|---|---|
| Tool mới `citations` | `starter_v0/tools/citations/`, `starter_v0/tools/__init__.py`, `starter_v0/artifacts/tools.yaml` | Định dạng các nguồn đã có thành danh sách tài liệu tham khảo đánh số. | Không tự truy xuất hoặc xác minh nguồn; từ chối URL không hợp lệ. |
| Tool mới `source_domains` | `starter_v0/tools/source_domains/` | Trích xuất các hostname duy nhất từ danh sách URL nguồn. | Không truy xuất hoặc xác minh website. |
| Tool mới `word_count` | `starter_v0/tools/word_count/` | Đếm số từ và ký tự trong văn bản được cung cấp. | Đếm theo quy tắc nhận diện từ cục bộ; không tóm tắt nội dung. |
| Unit test các tool mới | `starter_v0/tests/test_tools_todo.py` | 9 test mới đạt; toàn bộ suite: 86 passed, 17 skipped, 0 failed. | Test chạy offline, không gửi yêu cầu mạng. |
| UI (lệnh chạy + link dùng thử) | `starter_v0/app.py`, `starter_v0/ui_session.py`, `starter_v0/README.md`; transcript UI ở B4 | Giao diện chat Streamlit đã chạy qua link public; chọn cấu hình, xem tool/lỗi, lưu và tải transcript; lệnh và URL ở A1 | Link tunnel tạm thời; hành vi model phụ thuộc prompt/tools CP2 |
| Kiểm thử tích hợp CP5 | `starter_v0/tests/test_ui_session.py`, `starter_v0/tests/test_app.py` | 6 test mới đạt; toàn suite lúc đó 92 passed, 17 skipped, 0 failed (17 stub có sẵn sau đó đã được điền, xem B5: 110 passed, 0 skipped) | Test offline không thay thế transcript live |

Mỗi tool có các test cho đầu vào hợp lệ, đầu vào sai và nhánh lỗi. Ví dụ, unit test kiểm tra URL không hợp lệ được trả về dưới dạng error dict; eval routing không chứng minh được code tool xử lý đúng đầu vào đó.

### B5. Bonus Evidence

Kiểm tra khi tích hợp PR #7/#8/#9: phát hiện lỗi HTTP Telegram có thể chứa bot
token trong URL của thông báo lỗi. Đã che token tại `tools/send/tool.py` trước
khi trả kết quả cho model/UI/transcript. Regression test offline
`tests/test_ui_session.py::test_send_failure_redacts_token_before_model_and_transcript`
đã bắt lỗi trước khi sửa và đạt sau khi sửa; giữ loại lỗi và mã HTTP để chẩn đoán.
Toàn suite sau tích hợp: **93 passed, 17 skipped, 0 failed**. Không gửi Telegram
thật trong test; đây là bằng chứng regression test cho tool có sẵn.

Test challenge (0 skipped): đã điền 14 stub `pytest.skip(TODO)` trong
`starter_v0/tests/test_tools_todo.py` cho `clarify`, `format`, `send`, `lookup`,
`fetch`, `timeline`, `social_search`, `policy`; xoá 3 stub mẫu
`test_my_new_tool_*` vì 9 test cho `citations`, `source_domains`, `word_count` đã có.
Test gọi API dùng `fake_http` và assert cả request gửi đi (URL, json, params) lẫn kết
quả trả về; test `policy` kiểm tra dòng chèn lệnh trong mục "Injection probe" nằm ở
`untrusted_text`, không lọt vào `facts`. Các test mới không phát hiện thêm bug trong
tool có sẵn. Toàn suite: **110 passed, 0 skipped, 0 failed** (`cd starter_v0 && pytest -q`).

Chỉ điền nếu nhóm làm bonus (ghi riêng, tối đa 10 điểm). Tool có sẵn (`send`, `policy`, `papers`, `paper_text`) không tự được bonus.

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Small Local Model | xem B7 |  |  |
| Hơn 3 tool mới (≥ 4) |  |  |  |
<<<<<<< HEAD
| `send` gửi thật lên Telegram sau xác nhận | transcript |  |  |
| Test challenge (0 skipped / regression test) | `pytest` output; `starter_v0/tests/test_tools_todo.py`; `starter_v0/tests/test_ui_session.py::test_send_failure_redacts_token_before_model_and_transcript` | Cả hai tiêu chí: toàn suite 110 passed, 0 skipped, 0 failed; 1 bug tìm được trong `send` (lộ bot token trong thông báo lỗi HTTP) đã sửa và giữ regression test | Test chạy offline, mọi HTTP bị chặn và mock bằng `fake_http`; không thay thế kiểm thử live với API thật |
=======
| `send` gửi thật lên Telegram sau xác nhận | `starter_v0/transcripts/v3_deepseek_20261111T000241323945.transcript.json` (lượt 6–7) | Luồng đủ: yêu cầu đăng → agent hỏi xác nhận → user đồng ý → `send(confirmed=true)` → `status: sent`; tin nhắn hiện trong kênh private của nhóm | Chỉ gửi lên kênh private của nhóm, chỉ sau khi xác nhận; token nằm trong `.env` (gitignored) và đã quét transcript/run không thấy token |
| Test challenge (0 skipped / regression test) | `pytest` output |  |  |
>>>>>>> origin/docs/live-chat-telegram-evidence

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
- Snapshot CP5 trước khi tích hợp CP2 đoán URL khi thiếu thông tin, và gọi `send` trước khi hỏi
  xác nhận (tool chặn gửi). Bằng chứng thật ở B4; bàn giao CP2 để sửa prompt/tool
  declaration rồi chạy lại trên bản cuối. Không sửa các file CP2/CP4 trong phần CP5.
- Dùng DeepSeek thay OpenRouter: starter không có provider này nên nhóm thêm `providers/deepseek_provider.py` (kế thừa `OpenAIProvider`) và đăng ký ở `run_eval.py`, `chat.py`, `scripts/preflight_provider.py`. Lần đầu preflight báo `Missing API key env var: DEEPSEEK_API_KEY` vì `.env` chưa có key; thêm key rồi chạy lại.
- `pytest` ban đầu báo thiếu module `requests` do chưa cài dependency trong `.venv`; chạy `pip install -r requirements.txt` rồi xanh (86 passed).
- Case R12 (xin xác nhận trước khi đăng) vẫn fail ở v2: model gọi đúng `clarify` nhưng dùng `response_type=text` thay vì `yes_no` vì chưa có nội dung bản tin để đăng. Run: `starter_v0/runs/v2_B_base_deepseek_20261110T184518723180.json`.

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong [TEAM.md](../../TEAM.md) và các báo cáo cá nhân `report/team/MSSV_HoTen.md`.

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- **Fix thuộc `system_prompt.md`** (hành vi của agent): v1 bỏ chỉ dẫn đoán/gửi vội/ép một bước và thêm rule hỏi lại bằng `clarify`, xác nhận trước khi `send`, từ chối ngoài phạm vi (R08, R10, R11, R14 từ FAIL sang PASS, 0.45 → 0.65). v3 tách xác nhận gửi/đăng thành hai bước (R12, 0.95 → 1.00).
- **Fix thuộc `tools.yaml`** (cách dùng tool và tham số): v2 viết lại description và quy ước tham số: `query` là từ khóa ngắn, `topic=news`, bảng `timeframe`, handle không có `@`, gọi một lần (R02, R03, R06, R13, M02, M06 từ FAIL sang PASS, 0.65 → 0.95). Một dòng "không lặp tool" thêm vào prompt ở v1 không có tác dụng với R02 và R06; hai case này chỉ sửa được sau khi sửa `tools.yaml`.
- **Failure cần review thủ công:** R12 ("Đăng bản tin này lên Telegram"). Ở v1 và v2 model gọi `clarify` với `response_type=text` để xin nội dung bản tin, còn eval chỉ chấp nhận `yes_no`. Hành vi đó an toàn (không gửi) và có lý, nhưng không khớp eval; nhóm chọn sửa prompt ở v3 để khớp. Run: `starter_v0/runs/v2_B_base_deepseek_20261110T184518723180.json`, `starter_v0/runs/v3_B_base_deepseek_20261110T190413436138.json`.
- **Hạn chế:** 1.00 chỉ đo trên bộ base mà prompt và mô tả tool được chỉnh theo chính các case đó, nên có thể quá khớp. Điểm v2 gồm cả tác động của 3 tool mới (CP3) lẫn phần viết lại description, nên không tách riêng được từng phần. Các run tối ưu bộ base dùng `deepseek-chat`; bằng chứng CP5 và run CP3 riêng dùng OpenRouter / `openai/gpt-4o-mini`.
- **Kiểm chứng ngoài base:** bộ group v3 đạt 9/10, đã phủ ba tool mới; G05 còn fail như phân tích B3. Chưa có run extension. Transcript CP5 v3 còn lượt hỏi URL bằng text thay vì gọi `clarify`; cần review thủ công cả ngữ cảnh URL và độ rõ ràng của xác nhận gửi.
- **Giả thuyết cho vòng tiếp theo:** chạy extension và thêm case riêng kiểm tra OpenRouter có gọi control tool `clarify` khi thiếu URL, thay vì chỉ trả câu hỏi bằng text; giữ log cũ để so sánh.

## 8. Tài liệu tham khảo

-
