# Source code

Toàn bộ source code của lab nằm trong folder này. Chạy mọi lệnh từ `starter_v0/`.

- File bắt đầu chạy: `run_eval.py` (chạy eval), `chat.py` (chat live), `scripts/preflight_provider.py` (kiểm tra provider).
- Cách chạy: `python run_eval.py --provider openrouter --version v0 --suite base --eval-cases data/eval_base.json`; `python chat.py --provider openrouter --version v3`; `pytest`.
- Input: `artifacts/system_prompt.md`, `artifacts/tools.yaml`, bộ case `data/*.json`, API key trong `.env` (mẫu ở `.env.example`).
- Output: `runs/*.json` (kết quả eval), `transcripts/*.transcript.json` (chat live), `analysis/*.csv` (nếu chạy `scripts/parse_runs.py`).
- File học viên được sửa: `artifacts/system_prompt.md`, `artifacts/tools.yaml`, `artifacts/version_log.csv`, `data/eval_group.json`, `tools/` (thêm tool mới và đăng ký trong `tools/__init__.py`), `tests/test_tools_todo.py`, code UI và `requirements.txt`. Không sửa nội dung case trong `data/eval_base.json`.

Chi tiết từng bước xem [README.md](../README.md) ở root; cấu hình API key xem [docs/TOOL-SETUP.md](../docs/TOOL-SETUP.md).

# CP5 — UI, live chat và bàn giao demo

## Chạy UI

Chạy mọi lệnh ứng dụng từ `starter_v0/`. Trên Windows:

```powershell
.\.venv\Scripts\python.exe -m pip install --no-cache-dir -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py --global.developmentMode false
```

Trên macOS/Linux, thay `.\.venv\Scripts\python.exe` bằng `.venv/bin/python`.
Mở http://localhost:8501 và nhập câu hỏi để bắt đầu. Mặc định dùng OpenRouter;
nếu dùng provider khác, mở **Cài đặt** trước khi gửi câu hỏi đầu tiên.
Model để trống sẽ dùng mặc định của provider. Nhãn phiên bản là nhãn bằng chứng
của các file hiện tại, không phải chức năng checkout phiên bản; nhập đúng nhãn
mà CP2 đã bàn giao trong Cài đặt.

Mỗi trình duyệt có phiên riêng. **Cuộc trò chuyện mới** đưa về màn hình bắt đầu;
câu hỏi đầu tiên đọc prompt/tools hiện tại và tạo transcript mới. Transcript
cũ trên đĩa vẫn còn. Cấu hình được giữ cố định trong phiên; tạo cuộc trò chuyện
mới để thay đổi. Phiên đang mở không tự
nạp thay đổi CP2: prompt, declarations và hash được giữ cố định cho cả phiên.
History giữ tối đa 5 cặp user/assistant, giống mặc định của CLI.

UI sử dụng `chat.run_model_tool_loop`, không tạo một agent/routing riêng.
Mục **Xem hoạt động** có các vòng model, arguments và kết quả tool; lỗi tool/provider
được hiển thị. Transcript tự lưu sau mỗi lượt vào `transcripts/` và có nút tải
JSON. Nếu ghi đĩa lỗi, UI báo lỗi và vẫn cho tải bản đang giữ trong bộ nhớ.

## Link dùng thử

Link đã thử chat và tải transcript thành công:
https://weeks-yield-consolidated-dom.trycloudflare.com

Đây là link của phiên tunnel hiện tại, không phải hosting cố định.

Chạy Streamlit ở terminal thứ nhất. Nếu máy đã có `cloudflared`, ở terminal khác:

```powershell
cloudflared tunnel --url http://localhost:8501
```

Copy URL HTTPS thực tế do lệnh trả về vào mục A1 của group report. Nhờ một người
ngoài nhóm mở link và chạy một câu hỏi mẫu. Link tạm chỉ hoạt động khi cả hai
tiến trình còn chạy. Nếu chưa cài, hướng dẫn lab ở README có lệnh cài Windows;
có thể dùng Streamlit Cloud thay thế. Không đưa `.env` vào Git.

## Kịch bản kiểm tra live sau khi tích hợp CP2

Chạy CLI theo yêu cầu checkpoint, với version thực tế (ví dụ khi đã bàn giao v3):

```powershell
.\.venv\Scripts\python.exe chat.py --provider openrouter --version v3
```

1. `Đếm số từ trong đoạn: Research agents use tools.`
2. `Đọc bài viết này giúp tôi.` — quan sát việc hỏi URL.
3. Trả lời `URL là https://example.com/`.
4. `Chuẩn bị gửi nội dung "Bản tin thử nghiệm CP5" lên Telegram. Tôi chưa xác nhận gửi; hãy hỏi xác nhận nội dung trước.`
5. Chỉ nếu muốn thử gửi thật vào private channel của nhóm và đã cấu hình bot,
   tự xác nhận chính xác nội dung ở lượt sau. Gửi thật là bonus; không bắt buộc cho UI.
6. `/exit`, đọc transcript và điền B4 bằng tool call/kết quả thực tế.

Đã chạy một smoke session thật bằng OpenRouter trên artifact snapshot hiện tại:
`starter_v0/transcripts/v0-cp5-smoke_openrouter_20261110T183625534828.transcript.json`.
Nhãn `v0-cp5-smoke` là nhãn kiểm tra CP5, không phải run baseline v0 hay bản tối
ưu v3. Phiên này có lỗi đoán URL khi thiếu thông tin; không được ghi là pass
luồng hỏi lại. Cần kiểm tra lại trên bản cuối CP2 và bổ sung bằng chứng.

## Phối hợp file

- CP5 sở hữu `app.py`, `ui_session.py`, các test UI, tài liệu này và phần A/B4/UI trong report.
- CP2 tiếp tục sửa prompt/tools/version log và B1/B2; CP4 sửa eval nhóm và B3.
- UI dùng registry và declarations có sẵn; không cần sửa bộ base eval hay tool code.
- Các test offline dùng fake provider và thư mục tạm; không phải transcript live nộp bài.
- Thông tin thành viên, báo cáo cá nhân và commit đóng góp do thành viên tự khai trung thực.

## Kiểm tra kỹ thuật

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Tham khảo API UI và công cụ kiểm thử: [Streamlit chat input](https://docs.streamlit.io/develop/api-reference/chat/st.chat_input),
[Streamlit AppTest](https://docs.streamlit.io/develop/api-reference/app-testing/st.testing.v1.apptest).
