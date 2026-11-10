---
name: extract_links
track: core
kind: local_formatter
requires_env: []
inputs: [text]
outputs: [urls, count, error]
side_effect: false
---
# extract_links

Extract unique HTTP(S) URLs from supplied plain text or Markdown in first appearance order. Use to collect source links from existing research notes. Do not use to search for sources, read pages, verify availability, or extract hostnames (use source_domains).

Input: `text`, a nonempty string. Output: `{"tool": "extract_links", "urls": [...], "count": n}`. Text without HTTP(S) links returns an empty list and zero count. Duplicate URL strings are removed without reordering or rewriting URLs. Terminal prose punctuation and unmatched closing Markdown brackets/parentheses are trimmed; balanced parentheses, queries and fragments are retained.

Wrong types, empty text, or malformed HTTP(S) candidates return `{"tool": "extract_links", "error": "..."}` without raising. Validation is syntactic only. No network requests, environment variables, file writes or other side effects.
