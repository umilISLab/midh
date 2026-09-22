import json

import pymupdf
import pytesseract
from PIL import Image


def render_pdf_page(pdf_path: str, page_number: int = 0, dpi: int = 200) -> Image.Image:
    doc = pymupdf.open(pdf_path)
    page = doc[page_number]
    pixmap = page.get_pixmap(dpi=dpi)
    return Image.frombytes("RGB", (pixmap.width, pixmap.height), pixmap.samples)


def ocr_page(image: Image.Image, lang: str = "ita") -> str:
    return pytesseract.image_to_string(image, lang=lang).strip()


def read_bytes(path: str, n: int = 32) -> bytes:
    with open(path, "rb") as f:
        return f.read(n)


def show_bytes(data: bytes) -> None:
    print(data)
    print(" ".join(format(byte, "08b") for byte in data))


def load_transcription(json_path: str, page_number: int, types: tuple = ("text",)) -> str:
    with open(json_path, encoding="utf-8") as f:
        entries = json.load(f)
    lines = [
        entry["content"]
        for entry in entries
        if entry["page_number_in_pdf"] == page_number and entry["type"] in types
    ]
    return "\n\n".join(lines)


def load_entries(json_path: str) -> list:
    with open(json_path, encoding="utf-8") as f:
        return json.load(f)
