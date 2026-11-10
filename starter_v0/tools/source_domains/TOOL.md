---
name: source_domains
track: core
kind: local_formatter
requires_env: []
inputs: [urls]
outputs: [domains, count, error]
side_effect: false
---
# source_domains

Trích xuất các hostname duy nhất từ danh sách URL HTTP(S) đã cung cấp; không truy cập hoặc xác minh website. Đầu vào không hợp lệ trả về một dictionary chứa lỗi.
