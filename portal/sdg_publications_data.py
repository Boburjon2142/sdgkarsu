from pathlib import Path
import re
from typing import Dict, List, Tuple
from zipfile import ZipFile
from xml.etree import ElementTree as ET


SDG_PUBLICATION_FOLDER = Path(__file__).resolve().parents[1] / "data" / "sdg_publications"

SDG_GOAL_META = {
    1: {"title_en": "SDG 1: No poverty", "title_uz": "SDG 1: Kambag'allikka barham"},
    2: {"title_en": "SDG 2: Zero hunger", "title_uz": "SDG 2: Ochlikka barham"},
    3: {"title_en": "SDG 3: Good health and well-being", "title_uz": "SDG 3: Sog'liq va farovonlik"},
    4: {"title_en": "SDG 4: Quality education", "title_uz": "SDG 4: Sifatli ta'lim"},
    5: {"title_en": "SDG 5: Gender equality", "title_uz": "SDG 5: Gender tenglik"},
    6: {"title_en": "SDG 6: Clean water and sanitation", "title_uz": "SDG 6: Toza suv va sanitariya"},
    7: {"title_en": "SDG 7: Affordable and clean energy", "title_uz": "SDG 7: Arzon va toza energiya"},
    8: {"title_en": "SDG 8: Decent work and economic growth", "title_uz": "SDG 8: Munosib mehnat va iqtisodiy o'sish"},
    9: {"title_en": "SDG 9: Industry, innovation and infrastructure", "title_uz": "SDG 9: Sanoat, innovatsiya va infratuzilma"},
    10: {"title_en": "SDG 10: Reduced inequalities", "title_uz": "SDG 10: Tengsizlikni qisqartirish"},
    11: {"title_en": "SDG 11: Sustainable cities and communities", "title_uz": "SDG 11: Barqaror shaharlar va jamoalar"},
    12: {"title_en": "SDG 12: Responsible consumption and production", "title_uz": "SDG 12: Mas'uliyatli iste'mol va ishlab chiqarish"},
    13: {"title_en": "SDG 13: Climate action", "title_uz": "SDG 13: Iqlim chorasi"},
    14: {"title_en": "SDG 14: Life below water", "title_uz": "SDG 14: Suv ostidagi hayot"},
    15: {"title_en": "SDG 15: Life on land", "title_uz": "SDG 15: Quruqlikdagi hayot"},
    16: {"title_en": "SDG 16: Peace, justice and strong institutions", "title_uz": "SDG 16: Tinchlik, adolat va samarali institutlar"},
    17: {"title_en": "SDG 17: Partnerships for the goals", "title_uz": "SDG 17: Maqsadlar yo'lida hamkorlik"},
}

PUBLICATION_TYPES = {
    "Article",
    "Conference Paper",
    "Review",
    "Book Chapter",
    "Retracted",
    "Conference Paper • Open access",
    "Conference Paper •  Open access",
}

WORD_NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

VENUE_MARKERS = [
    "International Journal",
    "Journal",
    "Conference",
    "Proceedings",
    "Web of Conferences",
    "Transactions",
    "Plos One",
    "Chemosphere",
    "Bylye Gody",
    "Frontiers",
    "Catalysis",
    "Science Progress",
    "Stochastic Models",
    "Phytochemistry",
    "Genetic Resources",
    "Nordic Journal",
    "Aip Conference Proceedings",
    "Bio Web of Conferences",
    "Geojournal of Tourism and Geosites",
    "Indian Journal",
    "Wseas Transactions",
    "Innovative Infrastructure Solutions",
    "Applied Modeling Techniques",
    "National Journal",
    "Proceedings of SPIE",
    "ACM International Conference",
    "Chaos Solitons and Fractals",
    "Surfaces and Interfaces",
    "Chemical Papers",
    "Journal of Nanostructures",
    "Frontiers in Agronomy",
    "Eurasian Journal of Soil Science",
    "International Journal of Aquatic Research and Environmental Studies",
]


def _normalize_publication_kind(value: str) -> str:
    return " ".join(value.replace("\xa0", " ").split())


def _read_docx_paragraphs(path: Path) -> List[str]:
    with ZipFile(path) as archive:
        xml = archive.read("word/document.xml")

    root = ET.fromstring(xml)
    paragraphs = []
    for paragraph in root.findall(".//w:p", WORD_NS):
        text = "".join((node.text or "") for node in paragraph.findall(".//w:t", WORD_NS)).strip()
        if text:
            paragraphs.append(text)
    return paragraphs


def _extract_publication_meta(citation: str) -> Tuple[str, str, str]:
    normalized = citation.replace("\xa0", " ").strip()
    year_match = re.search(r"(19|20)\d{2}(?!.*(19|20)\d{2})", normalized)
    year = year_match.group(0) if year_match else ""

    split_index = -1
    for marker in VENUE_MARKERS:
        marker_index = normalized.find(marker)
        if marker_index != -1 and (split_index == -1 or marker_index < split_index):
            split_index = marker_index

    authors = normalized[:split_index].rstrip(" ,.;") if split_index != -1 else normalized
    if split_index != -1:
        venue_end = year_match.start() if year_match else len(normalized)
        venue = normalized[split_index:venue_end].rstrip(" ,.;")
    else:
        venue = ""
    return authors, venue, year


def _extract_titles(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []

    paragraphs = _read_docx_paragraphs(path)
    titles = []
    index = 0
    while index < len(paragraphs) - 2:
        kind = _normalize_publication_kind(paragraphs[index])
        if kind in PUBLICATION_TYPES:
            title = paragraphs[index + 1]
            citation = paragraphs[index + 2]
            authors, venue, year = _extract_publication_meta(citation)
            titles.append(
                {
                    "type": kind,
                    "title": title,
                    "authors": authors,
                    "venue": venue,
                    "year": year,
                    "citation": citation,
                }
            )
            index += 3
        else:
            index += 1
    return titles


def get_sdg_publication_data() -> Dict[int, Dict[str, object]]:
    result = {}
    for goal_number, meta in SDG_GOAL_META.items():
        titles = _extract_titles(SDG_PUBLICATION_FOLDER / f"SDG {goal_number}.docx")
        result[goal_number] = {
            **meta,
            "intro_en": f"Article titles linked to {meta['title_en']}.",
            "intro_uz": f"{meta['title_uz']} bo'yicha maqola nomlari.",
            "articles": titles,
        }
    return result
