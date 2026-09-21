import io
import zlib

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from scipy.fft import dctn, idctn

from nlp.images import draw_numbers

FORMATS = [
    ("BMP", "senza compressione", "BMP", {}),
    ("PNG", "senza perdita", "PNG", {}),
    ("WebP lossless", "senza perdita", "WEBP", {"lossless": True}),
    ("JPEG qualità 95", "con perdita", "JPEG", {"quality": 95}),
    ("JPEG qualità 75", "con perdita", "JPEG", {"quality": 75}),
    ("JPEG qualità 50", "con perdita", "JPEG", {"quality": 50}),
    ("JPEG qualità 10", "con perdita", "JPEG", {"quality": 10}),
    ("WebP qualità 75", "con perdita", "WEBP", {"quality": 75}),
]

STANDARD_RESOLUTIONS = [
    ("VGA", 640, 480),
    ("HD", 1280, 720),
    ("Full HD", 1920, 1080),
    ("4K", 3840, 2160),
    ("Fotocamera 12 Mpixel", 4000, 3000),
]


def raw_size(height: int, width: int, channels: int = 3) -> int:
    return height * width * channels


def encode(image: np.ndarray, file_format: str, **params) -> bytes:
    buffer = io.BytesIO()
    Image.fromarray(image).save(buffer, format=file_format, **params)
    return buffer.getvalue()


def decode(data: bytes) -> np.ndarray:
    return np.array(Image.open(io.BytesIO(data)).convert("RGB"))


def compare_formats(image: np.ndarray, formats: list = FORMATS) -> list:
    rows = []
    for name, kind, file_format, params in formats:
        data = encode(image, file_format, **params)
        error = np.abs(decode(data).astype(int) - image.astype(int)).mean()
        rows.append({"name": name, "kind": kind, "size": len(data), "error": error})
    return rows


def print_format_table(rows: list, original_size: int) -> None:
    print(f"{'formato':<18}{'tipo':<22}{'dimensione (kB)':>16}{'rapporto':>10}{'errore medio':>14}")
    for row in rows:
        ratio = original_size / row["size"]
        print(f"{row['name']:<18}{row['kind']:<22}{row['size'] / 1000:>16,.1f}{ratio:>9.1f}x{row['error']:>14.2f}")


def print_standard_sizes() -> None:
    print(f"{'standard':<34}{'pixel':>12}{'dimensione non compressa (MB)':>32}")
    for name, width, height in STANDARD_RESOLUTIONS:
        print(f"{name + f' ({width}x{height})':<34}{width * height:>12,}{raw_size(height, width) / 1e6:>32.1f}")


def show_quality_comparison(image: np.ndarray, qualities: list, box: tuple) -> None:
    top, bottom, left, right = box
    _, axes = plt.subplots(1, len(qualities) + 1, figsize=(4 * (len(qualities) + 1), 4.5))

    axes[0].imshow(image[top:bottom, left:right])
    axes[0].set_title("Originale (dettaglio)")
    for ax, quality in zip(axes[1:], qualities):
        data = encode(image, "JPEG", quality=quality)
        ax.imshow(decode(data)[top:bottom, left:right])
        ax.set_title(f"JPEG qualità {quality} ({len(data) / 1000:,.0f} kB)")

    for ax in axes:
        ax.set_xticks([])
        ax.set_yticks([])
    plt.tight_layout()
    plt.show()


JPEG_QUANTIZATION_TABLE = np.array([
    [16, 11, 10, 16, 24, 40, 51, 61],
    [12, 12, 14, 19, 26, 58, 60, 55],
    [14, 13, 16, 24, 40, 57, 69, 56],
    [14, 17, 22, 29, 51, 87, 80, 62],
    [18, 22, 37, 56, 68, 109, 103, 77],
    [24, 35, 55, 64, 81, 104, 113, 92],
    [49, 64, 78, 87, 103, 121, 120, 101],
    [72, 92, 95, 98, 112, 100, 103, 99],
])


def rle_encode(values: list) -> list:
    runs = []
    for value in values:
        if runs and runs[-1][0] == value:
            runs[-1][1] += 1
        else:
            runs.append([value, 1])
    return [tuple(run) for run in runs]


def lzw_encode(text: str) -> tuple:
    dictionary = {chr(code): code for code in range(256)}
    learned = {}
    codes = []
    current = ""
    for character in text:
        if current + character in dictionary:
            current += character
        else:
            codes.append(dictionary[current])
            dictionary[current + character] = len(dictionary)
            learned[len(dictionary) - 1] = current + character
            current = character
    codes.append(dictionary[current])
    return codes, learned


def reduce_palette(image: np.ndarray, colors: int = 256) -> tuple:
    quantized = Image.fromarray(image).quantize(colors)
    palette = np.array(quantized.getpalette()[: colors * 3]).reshape(-1, 3)
    return np.array(quantized), palette


def sub_filter(image: np.ndarray) -> np.ndarray:
    filtered = image.copy()
    filtered[:, 1:] = image[:, 1:] - image[:, :-1]
    return filtered


def deflate_size(array: np.ndarray) -> int:
    return len(zlib.compress(array.tobytes(), 9))


def value_entropy(values: np.ndarray) -> float:
    counts = np.bincount(values.ravel().astype(np.int64) % 256, minlength=256)
    probabilities = counts[counts > 0] / counts.sum()
    return float(-(probabilities * np.log2(probabilities)).sum())


def grayscale(image: np.ndarray) -> np.ndarray:
    return image.mean(axis=2).astype(np.uint8)


def jpeg_block_demo(block: np.ndarray) -> tuple:
    coefficients = dctn(block.astype(float) - 128, norm="ortho")
    quantized = np.round(coefficients / JPEG_QUANTIZATION_TABLE).astype(int)
    reconstructed = idctn(quantized * JPEG_QUANTIZATION_TABLE, norm="ortho") + 128
    return coefficients, quantized, np.clip(np.round(reconstructed), 0, 255).astype(int)


def show_jpeg_block(gray: np.ndarray, top: int, left: int) -> None:
    block = gray[top:top + 8, left:left + 8]
    coefficients, quantized, reconstructed = jpeg_block_demo(block)

    _, axes = plt.subplots(1, 5, figsize=(20, 4.3))
    axes[0].imshow(block, cmap="gray", vmin=0, vmax=255)
    axes[0].set_title("Blocco 8x8 originale")
    draw_numbers(axes[1], block.astype(int), title="Valori dei pixel", fontsize=8)
    draw_numbers(axes[2], np.round(coefficients).astype(int), title="Dopo la DCT", fontsize=8)
    draw_numbers(axes[3], quantized, title=f"Dopo la quantizzazione ({int((quantized != 0).sum())} non nulli)", fontsize=8)
    axes[4].imshow(reconstructed, cmap="gray", vmin=0, vmax=255)
    axes[4].set_title("Blocco ricostruito")

    for ax in (axes[0], axes[4]):
        ax.set_xticks([])
        ax.set_yticks([])
    plt.tight_layout()
    plt.show()
