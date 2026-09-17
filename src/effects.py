from PIL import Image, ImageEnhance
import numpy as np


def brightness(img: Image.Image, value: float) -> Image.Image:
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(value)
    return img


def saturation(img: Image.Image, value: float) -> Image.Image:
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(value)
    return img


def contrast(img: Image.Image, value: float) -> Image.Image:
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(value)
    return img


def apply_basic_effects(pil_img: Image.Image, bri_v: float, sat_v: float, con_v: float) -> Image.Image:
    """Applies contrast, then brightness, then saturation adjustments to the image, in that order."""
    pil_img = saturation(brightness(contrast(pil_img, con_v), bri_v), sat_v)
    return pil_img


def flipper(arr: np.ndarray, h: int, w: int, block_size: int) -> np.ndarray:
    """
    Divides the image into squares with a side length of 'block_size' pixels.
    Rotates each square 90 degrees to the left.
    """
    arr = arr.reshape(h // block_size, block_size, w // block_size, block_size, 3)
    arr = arr.transpose(0, 2, 1, 3, 4)
    arr = arr.reshape(-1, block_size, block_size, 3)
    arr[:] = np.rot90(arr[:], 1, (1, 2))

    arr = arr.reshape(h // block_size, w // block_size, block_size, block_size, 3)
    arr = arr.transpose(0, 2, 1, 3, 4).reshape(h, w, 3)
    return arr


def fader(arr: np.ndarray, h: int, w: int, cov: float, hole_size: int) -> np.ndarray:
    """Applies irregular blob-like patches to the image by blacking out groups of pixels.

    Randomly selects a coverage value from a range dependent on the 'cov' parameter.
    Creates small low-resolution grayscale noise matrix sized relative to arr via 'hole_size'.
    Upscales noise to 'arr' dimensions using bicubic interpolation,
    which smooths the low-res values into irregular patches of varying intensity.
    Calculates a threshold as the percentile of noise values corresponding to coverage,
    guaranteeing ~coverage% of pixels fall below it.
    Builds a binary mask (0/1) from threshold with an extra dimension,
    so it broadcasts against arr RGB channels.
    Multiplies 'arr' by the mask: if mask is 0 pixel is blackened,
    if mask is 1 pixel remains unchanged.
    """
    coverage = np.random.uniform(cov / 100, cov / 100 + 0.2)
    small_h, small_w = max(1, h // hole_size), max(1, w // hole_size)
    small_noise = np.random.rand(small_h, small_w) * 255

    noise_img = Image.fromarray(small_noise.astype(np.uint8))
    noise_img = noise_img.resize((w, h), Image.Resampling.BICUBIC)
    noise_arr = np.array(noise_img)

    threshold = np.percentile(noise_arr, coverage * 100)

    fade = (noise_arr > threshold).astype(np.uint8)
    fade = np.expand_dims(fade, axis=-1)
    arr_fade = arr * fade
    return arr_fade.astype(np.uint8)


def nuker(arr: np.ndarray) -> np.ndarray:
    """Brightens all image pixels causing glitch-art-style degradation due to RGB channel overflow.

    Increases the value of each RGB channel by 6.
    When the value exceeds 255 the added values are calculated starting from 0.
    """
    arr = arr + 6
    return arr.astype(np.uint8)


def puzzler(arr: np.ndarray, h: int, w: int, block_size: int) -> np.ndarray:
    """Divides the image into squares and randomly reorders their positions.

    Divides the image into squares with a side length of 'block_size' pixels.
    Generates a random permutation of numbers ranging from 0 to the number of squares.
    Flattens the grid of squares into a list and reorders them according to the permutation,
    before reshaping back into the original grid layout.
    """
    positions_count = (h // block_size) * (w // block_size)
    positions = np.random.choice(np.arange(positions_count), positions_count, replace=False)

    blocks = (arr.reshape(h // block_size, block_size, w // block_size, block_size, 3))
    blocks = blocks.transpose(0, 2, 1, 3, 4)
    blocks = blocks.reshape(-1, block_size, block_size, 3)

    shuffled = blocks[positions]
    shuffled = (shuffled.reshape(h // block_size, w // block_size, block_size, block_size, 3))
    shuffled = shuffled.transpose(0, 2, 1, 3, 4).reshape(h, w, 3)
    return shuffled


def liner(
    arr: np.ndarray,
    strength: int,
    positions: np.ndarray,
    fade: bool,
    arr_normal: np.ndarray,
    glitch: bool,
) -> np.ndarray:
    """Modifies 'strength' rows of the image (1 pixel tall, full width) at row indices taken from 'positions'.

    When fade is True: applies the effect to the selected rows — blackens
    them in default mode, or shifts all RGB channels by the same random
    value in glitch mode (allowing overflow).
    When fade is False: restores the selected rows to their original values from arr_normal.
    """
    row = positions[:strength]
    if glitch:
        if fade:
            arr[row] = arr[row] + np.random.randint(255)
        else:
            arr[row] = arr_normal[row]
    else:
        if fade:
            arr[row] = arr[row] * 0
        else:
            arr[row] = arr_normal[row]
    return arr


def rainbower(arr: np.ndarray, h: int, w: int, block_size: int, spread: int) -> np.ndarray:
    """Divides the image into squares and tints each one with a random color channel.

    Divides the image into squares with a side length of 'block_size' pixels.
    For each square, randomly selects one RGB channel and a random value
    within the range defined by 'spread'.
    Flattens the grid of squares into a list, then overwrites the selected
    channel of each square with its assigned value,
    before reshaping back into the original grid layout.
    """
    rgb_count = (h // block_size) * (w // block_size)
    positions = np.arange(rgb_count)
    rgb_ids = np.random.choice(np.arange(3), rgb_count)
    rgb_values = np.random.choice(np.arange(0, spread), rgb_count)

    arr = arr.reshape(h // block_size, block_size, w // block_size, block_size, 3)
    arr = arr.transpose(0, 2, 1, 3, 4)
    arr = arr.reshape(-1, block_size, block_size, 3)

    arr[positions, :, :, rgb_ids] = rgb_values[positions, None, None]

    arr = arr.reshape(h // block_size, w // block_size, block_size, block_size, 3)
    arr = arr.transpose(0, 2, 1, 3, 4).reshape(h, w, 3)
    return arr
