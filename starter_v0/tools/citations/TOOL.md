---
name: citations
track: core
kind: local_formatter
requires_env: []
inputs: [items]
outputs: [references, count, error]
side_effect: false
---
# citations

Định dạng tiêu đề và URL HTTP(S) đã cung cấp thành danh sách tài liệu tham khảo đánh số. Tool không truy xuất hoặc xác minh nguồn. Đầu vào không hợp lệ trả về một dictionary chứa lỗi.
