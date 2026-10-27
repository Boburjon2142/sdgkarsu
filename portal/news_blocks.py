import json

from django.core.exceptions import ValidationError


FORMAT = "sdg-news-blocks-v1"


def parse_news_blocks(value):
    try:
        document = json.loads(value)
    except (ValueError, TypeError):
        return None
    if not isinstance(document, dict) or document.get("format") != FORMAT:
        return None
    blocks = document.get("blocks")
    if not isinstance(blocks, list) or len(blocks) > 100:
        raise ValidationError("Eng ko'pi 100 ta blok qo'shish mumkin.")
    for block in blocks:
        if not isinstance(block, dict):
            raise ValidationError("Yangilik bloki noto'g'ri.")
        if block.get("type") == "text" and isinstance(block.get("text"), str):
            continue
        if block.get("type") == "table":
            rows = block.get("rows")
            if isinstance(rows, list) and 1 <= len(rows) <= 50:
                columns = len(rows[0]) if isinstance(rows[0], list) else 0
                if 1 <= columns <= 20 and all(
                    isinstance(row, list) and len(row) == columns and all(isinstance(cell, str) for cell in row)
                    for row in rows
                ):
                    continue
        raise ValidationError("Jadval 1–50 qator va 1–20 ustundan iborat bo'lishi kerak.")
    return blocks


def news_plain_text(value):
    blocks = parse_news_blocks(value)
    if blocks is None:
        return value
    return " ".join(
        block["text"] if block["type"] == "text" else " ".join(cell for row in block["rows"] for cell in row)
        for block in blocks
    )
