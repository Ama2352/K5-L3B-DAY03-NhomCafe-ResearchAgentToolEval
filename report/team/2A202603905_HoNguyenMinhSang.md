# Báo cáo cá nhân — Hồ Nguyễn Minh Sang — 2A202603905

## 1. Thông tin thành viên

- Họ tên: Hồ Nguyễn Minh Sang
- MSSV: 2A202603905
- Email: 26ai.sanghnm@vinuni.edu.vn
- GitHub: [Ama2352](https://github.com/Ama2352)
- Nhóm: NhomCafe — L3B

## 2. Phần việc phụ trách

- CP3: thêm tool mới, đăng ký tool và unit test.
- CP5: triển khai UI, hướng dẫn chạy, transcript live và báo cáo bằng chứng.
- Quản lý repo, tích hợp thay đổi của nhóm từ main vào nhánh Sang.

## 3. Đóng góp cụ thể

- Thêm `citations` để định dạng title/URL thành danh sách tham khảo;
  `source_domains` để lấy hostname duy nhất; `word_count` để đếm từ/ký tự.
  Các tool chạy local, không xác minh nguồn, đầu vào lỗi trả error dict.
- Có `TOOL.md`, đăng ký trong registry và tools.yaml, 3 test/tool cho happy path,
  input sai và nhánh lỗi. Case nhóm `G_CP3_citations_existing_source` kiểm tra
  model gọi tool mới khi đã có nguồn, không tìm kiếm hoặc fetch thừa. Sau tích hợp,
  case mẫu được thay bằng bộ 10 case CP4 (G01/G02/GM03 phủ ba tool mới); run mẫu vẫn giữ làm lịch sử.
- Làm UI Streamlit chat nhiều lượt, cấu hình thu gọn, theme nền xanh xám nhạt
  và chữ đậm; hiển thị tool call/lỗi và cho tải transcript JSON.
- Tái sử dụng `chat.run_model_tool_loop`, giữ nguyên backend của CLI. Phiên UI
  snapshot prompt/tools và hash để các thay đổi trong lúc làm CP2 không làm lẫn bằng chứng.
- Dùng Cloudflare Quick Tunnel để chia sẻ UI; kiểm tra chat và tải JSON qua link
  public, kiểm tra bố cục desktop/mobile 390px và dọn file kiểm tra tạm khỏi repo.
- Merge CP2 từ main, giữ cả nội dung CP2/CP5 khi giải quyết xung đột báo cáo.
  Chạy lại transcript v3 thay vì dùng log prompt cũ để kết luận về bản cuối.

## 4. Bằng chứng

- Commit `60a1efa`: tool mới và unit test; `c7f23ac`: UI và transcript;
  `966687f`: merge main vào Sang.
- Code: `starter_v0/tools/{citations,source_domains,word_count}/`,
  `starter_v0/app.py`, `starter_v0/ui_session.py`, `.streamlit/config.toml` trong starter.
- Test: `starter_v0/tests/test_tools_todo.py`, `test_ui_session.py`, `test_app.py`.
  Toàn suite ở lần kiểm tra sau merge: 92 passed, 17 skipped, 0 failed;
  các skip là stub có sẵn, không phải test tool mới.
- Run thật: `starter_v0/runs/v3-cp3-routing_B_group_openrouter_20261110T194332874245.json`:
  1/1 case đạt, 0 lỗi provider. Đây là kiểm tra CP3, không phải bộ CP4 đủ 10 case.
- Transcript `starter_v0/transcripts/v3_openrouter_20261110T194205268170.transcript.json`:
  7 lượt gồm tìm tin, đọc nguồn và gọi đúng cả ba tool mới.
- Transcript `starter_v0/transcripts/v3_openrouter_20261110T194257230039.transcript.json`:
  thiếu URL → hỏi URL bằng text → đọc URL bổ sung → hỏi xác nhận qua `clarify(yes_no)`;
  không gửi Telegram thật.
- AI/công cụ sử dụng: Codex hỗ trợ triển khai code/test, kiểm tra log và soạn tài liệu;
  pytest kiểm tra offline, Playwright kiểm tra UI, Git kiểm tra thay đổi/merge,
  OpenRouter `openai/gpt-4o-mini` cho transcript/eval thật. Không dùng kết quả fake
  provider trong unit test để thay thế bằng chứng chạy model thật.

## 5. Tự đánh giá

Phần tổng kết dưới đây dựa trên bằng chứng kỹ thuật; thành viên cần tự xác nhận
mức độ hiểu và bổ sung trải nghiệm học tập của mình trước khi nộp.

- Phần việc đã có bằng chứng: ba tool local, unit test, UI, xuất transcript,
  kiểm tra routing tool mới và tích hợp CP2. Unit test kiểm tra code tool;
  eval/transcript kiểm tra quyết định gọi tool của model — hai loại không thay thế nhau.
- Hạn chế còn lại: model OpenRouter hỏi URL bằng text, chưa gọi `clarify` ở lượt
  thiếu URL; link tunnel chỉ tồn tại khi tiến trình chạy; chưa có bonus gửi Telegram thật.
- Sau tích hợp, CP4 đã có đủ 10 case và run; việc cần phối hợp còn lại là một người ngoài nhóm xác nhận
  demo; nhóm chốt nhánh/commit nộp và hoàn thiện báo cáo của từng thành viên.
- Hướng cải thiện: thêm regression case cho việc hỏi lại bằng text thay vì control tool,
  kiểm tra routing của cả ba tool trên provider cuối và dùng hosting ổn định cho demo dài hạn.
