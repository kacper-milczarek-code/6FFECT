import numpy as np
import math
from PySide6.QtGui import QImage
from PIL import Image


def ui_to_raw(ui_val: int | float, raw_range: tuple, ui_range: tuple, decimals: int) -> int | float:
    """
    Convert ui_val proportionally from ui_range to raw_range.

    ui_min -> raw_min
    ui_max -> raw_max
    values between them are linearly proportional
    """
    raw_min, raw_max = raw_range
    ui_min, ui_max = ui_range

    if ui_min == ui_max:
        raise ZeroDivisionError("ui_min cannot be equal to ui_max")

    raw_val = raw_min + (ui_val - ui_min) * (raw_max - raw_min) / (ui_max - ui_min)
    if decimals == 0:
        return int(round(raw_val))
    else:
        return round(raw_val, decimals)


def qimage_to_ndarray(qimage: QImage) -> np.ndarray:
    if qimage.isNull():
        raise ValueError("The given QImage is empty.")

    image = qimage.convertToFormat(QImage.Format.Format_RGBA8888)
    ptr = image.constBits()

    array = np.frombuffer(ptr, dtype=np.uint8).reshape((image.height(), image.width(), 4))

    return array[:, :, :3].copy()


def qimage_to_pil(qimage: QImage) -> Image.Image:
    if qimage.isNull():
        raise ValueError("The given QImage is empty.")
    qimage = qimage.convertToFormat(QImage.Format.Format_RGBA8888)

    width = qimage.width()
    height = qimage.height()
    ptr = qimage.constBits()

    pil_image = Image.frombytes("RGBA", (width, height), bytes(ptr), "raw", "RGBA").convert("RGB")

    return pil_image


def ndarray_to_qimage(arr: np.ndarray) -> QImage:
    h, w, ch = arr.shape
    bytes_per_line = ch * w
    return QImage(arr.data, w, h, bytes_per_line, QImage.Format.Format_RGB888).copy()


def closest_window_res(img: QImage) -> tuple[int, int] | str:
    """
    Matches closest dimensions with a 16:9 or 9:16 aspect ratio to dimensions of the provided photo.
    """
    res_horizontal = [(1920, 1080), (1600, 900), (1280, 720), (960, 540), (640, 360), (320, 180),
                      (256, 144), (240, 135), (192, 108), (160, 90), (32, 18), (16, 9)]

    res_vertical = [(1080, 1920), (900, 1600), (720, 1280), (540, 960), (360, 640),
                    (180, 320), (144, 256), (135, 240), (108, 192), (90, 160), (18, 32), (9, 16)]

    w, h = img.width(), img.height()

    if (w, h) in res_horizontal or (w, h) in res_vertical:
        return "correct"

    elif w > h:
        return min(res_horizontal, key=lambda r: abs(r[0] - w) + abs(r[1] - h))
    else:
        return min(res_vertical, key=lambda r: abs(r[0] - w) + abs(r[1] - h))


def calculate_block_sizes(width: int, height: int) -> list[int]:
    """
    Calculates correct block sizes for dividing an image with given dimensions.
    Finds all common divisors of the width and height that are greater than or equal to 10 px.
    """
    min_val = 10
    highest_bs = math.gcd(width, height)
    block_sizes = set()

    for i in range(1, math.isqrt(highest_bs) + 1):
        if highest_bs % i == 0:
            if i >= min_val:
                block_sizes.add(i)
            size = highest_bs // i
            if size >= min_val:
                block_sizes.add(size)

    return sorted(list(block_sizes))
