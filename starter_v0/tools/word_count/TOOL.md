---
name: word_count
track: core
kind: local_formatter
requires_env: []
inputs: [text]
outputs: [word_count, character_count, error]
side_effect: false
---
# word_count

Đếm từ và ký tự trong văn bản được cung cấp trên máy; không tóm tắt hoặc truy xuất nội dung. Đầu vào không hợp lệ trả về một dictionary chứa lỗi.
