from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent

ASSETS_DIR = ROOT_DIR / "assets"
EXAMPLE_IMAGES_DIR = ASSETS_DIR / "example_images"
THUMBNAILS_DIR = EXAMPLE_IMAGES_DIR / "thumbnails"
FONTS_DIR = ASSETS_DIR / "fonts"
ICONS_DIR = ASSETS_DIR / "icons"
SFX_DIR = ASSETS_DIR / "sfx"

SRC_DIR = ROOT_DIR / "src"
UI_DIR = SRC_DIR / "ui"
STYLE_QSS_PATH = UI_DIR / "style.qss"



