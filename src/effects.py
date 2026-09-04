from PIL import Image, ImageEnhance
import numpy as np


def brightness(img, value):
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(value)
    return img


def saturation(img, value):
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(value)
    return img


def contrast(img, value):
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(value)
    return img


def apply_basic_effects(pil_img, bri_v, sat_v, con_v):
    pil_img = saturation(brightness(contrast(pil_img, con_v), bri_v), sat_v)
    return pil_img


def flipper(arr, h, w, block_size):
    arr = arr.reshape(h // block_size, block_size, w // block_size, block_size, 3)
    arr = arr.transpose(0, 2, 1, 3, 4)
    arr = arr.reshape(-1, block_size, block_size, 3)
    arr[:] = np.rot90(arr[:], 1, (1, 2))

    arr = arr.reshape(h // block_size, w // block_size, block_size, block_size, 3)
    arr = arr.transpose(0, 2, 1, 3, 4).reshape(h, w, 3)
    return arr


def fader(arr, h, w, cov, hole_size):
    coverage = np.random.uniform(cov / 100, cov / 100 + 0.2)
    scale = hole_size
    small_h, small_w = max(1, h // scale), max(1, w // scale)
    small_noise = np.random.rand(small_h, small_w) * 255

    noise_img = Image.fromarray(small_noise.astype(np.uint8))
    noise_img = noise_img.resize((w, h), Image.Resampling.BICUBIC)
    noise_arr = np.array(noise_img)

    threshold = np.percentile(noise_arr, coverage * 100)

    fade = (noise_arr > threshold).astype(np.uint8)
    fade = np.expand_dims(fade, axis=-1)
    arr_fade = arr * fade

    return arr_fade.astype(np.uint8)


def nuker(arr):
    arr = arr + 6

    return arr.astype(np.uint8)


def puzzler(arr, h, w, block_size):
    positions_count = (h // block_size) * (w // block_size)
    positions = np.random.choice(np.arange(positions_count), positions_count, replace=False)
    blocks = (arr.reshape(h // block_size, block_size, w // block_size, block_size, 3))
    blocks = blocks.transpose(0, 2, 1, 3, 4)
    blocks = blocks.reshape(-1, block_size, block_size, 3)

    shuffled = blocks[positions]

    shuffled = (shuffled.reshape(h // block_size, w // block_size, block_size, block_size, 3))

    shuffled = shuffled.transpose(0, 2, 1, 3, 4).reshape(h, w, 3)
    return shuffled


def liner(arr, strength, positions, fade, arr_normal, glitch):
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


def rainbower(arr, h, w, block_size, spread):
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
