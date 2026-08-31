from PIL import ImageEnhance


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
