import pytest
import numpy as np
from src.effects import flipper, nuker, rainbower


@pytest.fixture
def dummy_image():
    return np.zeros((60, 60, 3), dtype=np.uint8)


def test_flipper_shape_retention(dummy_image):
    result = flipper(dummy_image, h=60, w=60, block_size=10)
    assert result.shape == (60, 60, 3)


def test_nuker_overflow(dummy_image):
    result = nuker(dummy_image)
    assert result[0, 0, 0] == 6


def test_rainbower_modifies_array(dummy_image):
    result = rainbower(dummy_image, h=60, w=60, block_size=10, spread=50)
    assert result.shape == (60, 60, 3)
    assert np.any(result > 0)
