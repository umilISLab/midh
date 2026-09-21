import matplotlib.pyplot as plt
import numpy as np


def smiley() -> np.ndarray:
    return np.array([
        [0, 0, 1, 1, 1, 1, 0, 0],
        [0, 1, 0, 0, 0, 0, 1, 0],
        [1, 0, 1, 0, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 0, 1, 0, 1],
        [1, 0, 0, 1, 1, 0, 0, 1],
        [0, 1, 0, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 1, 1, 0, 0],
    ])


def gradient(rows: int = 2, cols: int = 8) -> np.ndarray:
    row = np.linspace(0, 255, cols).astype(int)
    return np.tile(row, (rows, 1))


def quantize(image: np.ndarray, bits: int) -> np.ndarray:
    levels = 2 ** bits
    level_index = np.floor(image / 256 * levels)
    return np.round(level_index * 255 / (levels - 1)).astype(int)


def draw_image(ax, image: np.ndarray, vmax: int, title: str = None) -> None:
    ax.imshow(image, cmap="gray", vmin=0, vmax=vmax)
    ax.set_xticks([])
    ax.set_yticks([])
    if title:
        ax.set_title(title)


def draw_numbers(ax, image: np.ndarray, title: str = None, fontsize: int = 9) -> None:
    rows, cols = image.shape
    ax.set_xlim(-0.5, cols - 0.5)
    ax.set_ylim(rows - 0.5, -0.5)
    ax.hlines(np.arange(-0.5, rows), -0.5, cols - 0.5, colors="lightgray", linewidth=0.8)
    ax.vlines(np.arange(-0.5, cols), -0.5, rows - 0.5, colors="lightgray", linewidth=0.8)
    for row in range(rows):
        for col in range(cols):
            ax.text(col, row, str(image[row, col]), ha="center", va="center", fontsize=fontsize)
    ax.set_xticks([])
    ax.set_yticks([])
    if title:
        ax.set_title(title)


def show_image(image: np.ndarray, vmax: int = 1, title: str = None) -> None:
    _, (ax_image, ax_numbers) = plt.subplots(1, 2, figsize=(8, 4))
    draw_image(ax_image, image, vmax, title="Come la vede una persona")
    draw_numbers(ax_numbers, image, title="Come la vede la macchina")
    if title:
        plt.suptitle(title)
    plt.tight_layout()


def show_quantization(image: np.ndarray, bits_list: list) -> None:
    _, axes = plt.subplots(len(bits_list), 2, figsize=(9, 1.7 * len(bits_list)))
    for (ax_image, ax_numbers), bits in zip(axes, bits_list):
        quantized = quantize(image, bits)
        draw_image(ax_image, quantized, vmax=255, title=f"{bits} bit per pixel ({2 ** bits} livelli)")
        draw_numbers(ax_numbers, quantized)
    plt.tight_layout()
    plt.show()


def color_patches() -> np.ndarray:
    return np.array([
        [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)],
        [(0, 255, 255), (255, 0, 255), (255, 255, 255), (0, 0, 0)],
        [(255, 128, 0), (128, 128, 128), (128, 0, 0), (0, 128, 128)],
        [(255, 192, 203), (139, 69, 19), (128, 0, 128), (0, 0, 128)],
    ], dtype=np.uint8)


def to_hex(image: np.ndarray) -> np.ndarray:
    rows, cols, _ = image.shape
    return np.array([[f"#{image[r, c, 0]:02X}{image[r, c, 1]:02X}{image[r, c, 2]:02X}" for c in range(cols)] for r in range(rows)])


def keep_channel(image: np.ndarray, channel: int) -> np.ndarray:
    isolated = np.zeros_like(image)
    isolated[:, :, channel] = image[:, :, channel]
    return isolated


def show_channels(image: np.ndarray) -> None:
    names = ["rosso (R)", "verde (G)", "blu (B)"]
    _, axes = plt.subplots(2, 4, figsize=(15, 7.5))

    axes[0, 0].imshow(image)
    axes[0, 0].set_xticks([])
    axes[0, 0].set_yticks([])
    axes[0, 0].set_title("Come la vede una persona")
    draw_numbers(axes[1, 0], to_hex(image), title="Codice esadecimale del pixel", fontsize=8)

    for channel, name in enumerate(names):
        ax_top, ax_bottom = axes[0, channel + 1], axes[1, channel + 1]
        ax_top.imshow(keep_channel(image, channel))
        ax_top.set_xticks([])
        ax_top.set_yticks([])
        ax_top.set_title(f"Canale {name}")
        draw_numbers(ax_bottom, image[:, :, channel], title=f"Valori del canale {name}", fontsize=9)

    plt.tight_layout()
    plt.show()


def load_image(path: str) -> np.ndarray:
    return plt.imread(path)


def show_real_channels(image: np.ndarray) -> None:
    names = ["rosso (R)", "verde (G)", "blu (B)"]
    _, axes = plt.subplots(1, 4, figsize=(16, 6))

    axes[0].imshow(image)
    axes[0].set_title("Immagine originale")
    for channel, name in enumerate(names):
        axes[channel + 1].imshow(keep_channel(image, channel))
        axes[channel + 1].set_title(f"Canale {name}")

    for ax in axes:
        ax.set_xticks([])
        ax.set_yticks([])
    plt.tight_layout()
    plt.show()
