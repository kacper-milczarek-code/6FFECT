import pytest
import numpy as np
from PySide6.QtGui import QImage
from src.utils import ui_to_raw, calculate_block_sizes, qimage_to_ndarray, ndarray_to_qimage


def test_ui_to_raw_linear_conversion():
    raw_range = (0.1, 5.0)
    ui_range = (1, 100)

    assert ui_to_raw(1, raw_range, ui_range, decimals=1) == 0.1
    assert ui_to_raw(100, raw_range, ui_range, decimals=1) == 5.0


def test_ui_to_raw_zero_division():
    with pytest.raises(ZeroDivisionError):
        ui_to_raw(50, (0, 10), (10, 10), decimals=0)


def test_calculate_block_sizes():
    sizes = calculate_block_sizes(1920, 1080)
    assert 10 in sizes
    assert 120 in sizes
    assert all(size >= 10 for size in sizes)
    assert all(1920 % size == 0 and 1080 % size == 0 for size in sizes)


def test_qimage_and_ndarray_conversion():
    qimg = QImage(100, 100, QImage.Format.Format_RGB888)
    qimg.fill(0xFF0000)

    arr = qimage_to_ndarray(qimg)
    assert isinstance(arr, np.ndarray)
    assert arr.shape == (100, 100, 3)

    reconstructed_qimg = ndarray_to_qimage(arr)
    assert reconstructed_qimg.width() == 100
    assert reconstructed_qimg.height() == 100
