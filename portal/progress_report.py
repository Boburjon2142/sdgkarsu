import json
import re
from functools import lru_cache
from pathlib import Path

from django.conf import settings


@lru_cache(maxsize=1)
def get_food_security_sections():
    path = Path(settings.BASE_DIR) / "data" / "food_security_nutrition_program.json"
    return [
        section for section in json.loads(path.read_text(encoding="utf-8"))
        if section["title"] != "Approval"
    ]


@lru_cache(maxsize=1)
def get_progress_report_sections():
    path = Path(settings.BASE_DIR) / "data" / "sdg_progress_report_2024_2025.json"
    return json.loads(path.read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def get_collective_agreement_pages():
    path = Path(settings.BASE_DIR) / "data" / "collective_agreement_2026_2028.json"
    pages = json.loads(path.read_text(encoding="utf-8"))
    return [
        {"number": page["number"], "paragraphs": [
            re.sub(r"~\s*\d+\s*~", "", " ".join(paragraph.split())).strip()
            for paragraph in page["paragraphs"]
            if not paragraph.strip().isdigit()
        ]}
        for page in pages if 5 < page["number"] < 75
    ]


@lru_cache(maxsize=1)
def get_collective_agreement_sections():
    sections = []
    current = None
    for page in get_collective_agreement_pages():
        for text in page["paragraphs"]:
            if not text:
                continue
            is_heading = bool(re.match(r"^[IVXLCDM]+\.\s", text) or re.match(r"^Ilova\s", text))
            is_heading = is_heading or text == "JAMOA SHARTNOMASIGA ILOVALAR"
            if is_heading:
                # Some extracted headings include the first numbered clause.
                parts = re.split(r"\s+(?=\d+\.\d+\.)", text, maxsplit=1)
                title = parts[0]
                current = {"title": title, "paragraphs": []}
                sections.append(current)
                if len(parts) > 1:
                    current["paragraphs"].append(parts[1])
            else:
                if current is None:
                    current = {"title": "Umumiy qoidalar", "paragraphs": []}
                    sections.append(current)
                current["paragraphs"].append(text)
    return sections
