import re


def word_count(text):
    if not isinstance(text, str) or not text.strip():
        return {"tool": "word_count", "error": "text phải là chuỗi không rỗng"}
    words = re.findall(r"[^\W_]+(?:[\u2019\x27-][^\W_]+)*", text, flags=re.UNICODE)
    if not words:
        return {"tool": "word_count", "error": "Văn bản không chứa từ nào"}
    return {"tool": "word_count", "word_count": len(words), "character_count": len(text)}
