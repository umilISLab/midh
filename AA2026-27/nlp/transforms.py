import io

import ipywidgets as widgets
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import display
from matplotlib.patches import Rectangle
from scipy.ndimage import correlate

from nlp.images import draw_image, draw_numbers

CHANNEL_NAMES = ["R", "G", "B"]

KERNELS = {
    "Sfocatura": np.ones((3, 3)) / 9,
    "Nitidezza": np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]),
    "Bordi": np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]]),
    "Rilievo": np.array([[-2, -1, 0], [-1, 1, 1], [0, 1, 2]]),
}


def apply_kernel(region: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    if region.ndim == 2:
        return correlate(region, kernel, mode="nearest")
    return np.stack([correlate(region[:, :, c], kernel, mode="nearest") for c in range(region.shape[2])], axis=2)


def random_noise(region: np.ndarray) -> np.ndarray:
    rng = np.random.default_rng(0)
    return rng.integers(0, 256, region.shape).astype(float)


def negative(region: np.ndarray) -> np.ndarray:
    return 255 - region


def brighter(region: np.ndarray) -> np.ndarray:
    return region + 60


def darker(region: np.ndarray) -> np.ndarray:
    return region - 60


def threshold(region: np.ndarray) -> np.ndarray:
    return np.where(region >= 128, 255.0, 0.0)


def blur(region: np.ndarray) -> np.ndarray:
    return apply_kernel(region, KERNELS["Sfocatura"])


def sharpen(region: np.ndarray) -> np.ndarray:
    return apply_kernel(region, KERNELS["Nitidezza"])


def edges(region: np.ndarray) -> np.ndarray:
    return np.abs(apply_kernel(region, KERNELS["Bordi"]))


def emboss(region: np.ndarray) -> np.ndarray:
    return apply_kernel(region, KERNELS["Rilievo"]) + 128


RANDOM_TRANSFORMATIONS = {"Rumore casuale": random_noise}

POINT_FILTERS = {
    "Negativo": negative,
    "Più chiaro": brighter,
    "Più scuro": darker,
    "Soglia (bianco/nero)": threshold,
}

KERNEL_FILTERS = {
    "Sfocatura": blur,
    "Nitidezza": sharpen,
    "Bordi": edges,
    "Rilievo": emboss,
}

ALL_TRANSFORMATIONS = {**RANDOM_TRANSFORMATIONS, **POINT_FILTERS, **KERNEL_FILTERS}


def small_matrix() -> np.ndarray:
    matrix = np.full((8, 8), 50)
    matrix[2:6, 2:6] = 200
    return matrix


def to_uint8(values: np.ndarray) -> np.ndarray:
    return np.clip(np.round(values), 0, 255).astype(np.uint8)


def apply_transformation(image: np.ndarray, transform, rows: tuple, cols: tuple, channels: list, strength: float = 1.0) -> np.ndarray:
    top, bottom = rows
    left, right = cols
    channel_indices = [CHANNEL_NAMES.index(name) for name in channels]
    result = image.astype(float)

    if bottom <= top or right <= left or not channel_indices:
        return to_uint8(result)

    region = result[top:bottom, left:right][:, :, channel_indices]
    transformed = transform(region)
    result[top:bottom, left:right, channel_indices] = (1 - strength) * region + strength * transformed
    return to_uint8(result)


def explain_kernel_at(matrix: np.ndarray, kernel: np.ndarray, row: int, col: int) -> None:
    neighborhood = matrix[row - 1:row + 2, col - 1:col + 2]
    products = neighborhood * kernel
    print(f"Vicinato 3x3 attorno al pixel ({row}, {col}):\n{neighborhood}\n")
    print(f"Nucleo (kernel):\n{np.round(kernel, 2)}\n")
    print(f"Prodotti elemento per elemento:\n{np.round(products, 1)}\n")
    print(f"Somma dei prodotti = nuovo valore del pixel: {products.sum():.1f}")


def show_filter_examples(matrix: np.ndarray, filters: dict) -> None:
    rows = len(filters) + 1
    _, axes = plt.subplots(rows, 2, figsize=(9, 3.6 * rows))
    panels = [("Originale", matrix)] + [(name, to_uint8(function(matrix.astype(float)))) for name, function in filters.items()]

    for (ax_image, ax_numbers), (name, values) in zip(axes, panels):
        draw_image(ax_image, values, vmax=255)
        ax_image.set_ylabel(name, fontsize=12)
        draw_numbers(ax_numbers, values, fontsize=9)
    axes[0, 0].set_title("Come la vede una persona")
    axes[0, 1].set_title("Come la vede la macchina")
    plt.tight_layout()
    plt.show()


def make_comparison_figure(image: np.ndarray, edited: np.ndarray, rows: tuple, cols: tuple):
    fig, axes = plt.subplots(1, 2, figsize=(11, 7))
    axes[0].imshow(image)
    axes[0].set_title("Originale, con la regione scelta")
    axes[1].imshow(edited)
    axes[1].set_title("Dopo la trasformazione")
    axes[0].add_patch(Rectangle((cols[0], rows[0]), cols[1] - cols[0], rows[1] - rows[0], fill=False, edgecolor="yellow", linewidth=2))
    for ax in axes:
        ax.set_xlabel("colonna (x)")
        ax.set_ylabel("riga (y)")
    fig.tight_layout()
    return fig


def draw_comparison(image: np.ndarray, edited: np.ndarray, rows: tuple, cols: tuple) -> None:
    make_comparison_figure(image, edited, rows, cols)
    plt.show()


def show_filter_gallery(image: np.ndarray, filters: dict) -> None:
    panels = [("Originale", image)]
    height, width = image.shape[:2]
    for name, function in filters.items():
        panels.append((name, apply_transformation(image, function, (0, height), (0, width), CHANNEL_NAMES)))

    columns = 5
    grid_rows = -(-len(panels) // columns)
    _, axes = plt.subplots(grid_rows, columns, figsize=(4 * columns, 5.6 * grid_rows))
    for ax in axes.ravel():
        ax.axis("off")
    for ax, (name, panel) in zip(axes.ravel(), panels):
        ax.imshow(panel)
        ax.set_title(name)
    plt.tight_layout()
    plt.show()


def interactive_editor(image: np.ndarray, transformations: dict) -> None:
    height, width = image.shape[:2]
    style = {"description_width": "90px"}
    layout = widgets.Layout(width="520px")

    row_range = widgets.IntRangeSlider(value=[height // 5, height // 2], min=0, max=height, description="Righe (y)", continuous_update=False, style=style, layout=layout)
    col_range = widgets.IntRangeSlider(value=[width // 5, width * 4 // 5], min=0, max=width, description="Colonne (x)", continuous_update=False, style=style, layout=layout)
    channel_boxes = [widgets.Checkbox(value=True, description=name, indent=False, layout=widgets.Layout(width="60px")) for name in CHANNEL_NAMES]
    transformation = widgets.Dropdown(options=list(transformations), description="Trasformazione", style=style, layout=layout)
    strength = widgets.FloatSlider(value=1.0, min=0, max=1, step=0.05, description="Intensità", continuous_update=False, style=style, layout=layout)

    controls = [row_range, col_range, *channel_boxes, transformation, strength]
    picture = widgets.Image(format="png")
    caption = widgets.Label()
    last_state = {}

    def refresh(change=None):
        state = tuple(tuple(value) if isinstance(value, (list, tuple)) else value for value in (control.value for control in controls))
        if state == last_state.get("state"):
            return
        last_state["state"] = state

        rows, cols, red, green, blue, name, intensity = state
        channels = [n for n, selected in zip(CHANNEL_NAMES, (red, green, blue)) if selected]
        edited = apply_transformation(image, transformations[name], rows, cols, channels, intensity)
        numbers = (rows[1] - rows[0]) * (cols[1] - cols[0]) * len(channels)
        caption.value = f"Regione: righe {rows[0]}-{rows[1]}, colonne {cols[0]}-{cols[1]}, canali {''.join(channels) or 'nessuno'} -> {numbers:,} numeri modificati"

        fig = make_comparison_figure(image, edited, rows, cols)
        buffer = io.BytesIO()
        fig.savefig(buffer, format="png", dpi=90)
        plt.close(fig)
        picture.value = buffer.getvalue()

    for control in controls:
        control.observe(refresh, names="value")
    refresh()

    channel_row = widgets.HBox([widgets.Label("Canali", layout=widgets.Layout(width="90px"))] + channel_boxes)
    display(widgets.VBox([row_range, col_range, channel_row, transformation, strength, caption, picture]))
