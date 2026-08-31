from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QImage, QPixmap
from PIL.ImageQt import toqimage
import src.utils as utils
import src.effects as effects
import src.config as cfg


class EffectsManager(QThread):
    frame_ready_signal = Signal(QPixmap)

    def __init__(self):
        super().__init__()
        self.original_qimage = None
        self.qimage = None
        self.image_np = None
        self.image_pil = None

        self.mode_callbacks = {}

    def load_image_variables(self, image: QImage):
        self.original_qimage = image
        self.image_np = utils.qimage_to_ndarray(image)
        self.image_pil = utils.qimage_to_pil(image)

    def apply_effects_parameters(self, sld_index):
        pass
        # param_function = self.mode_callbacks[cfg.current_effect]
        # param_function(sld_index)

    def apply_no_mode_parameters(self):
        basic_effects_values = (utils.ui_to_raw(v, *cfg.NO_MODE_SLIDERS_SETTINGS) for v in
                                cfg.current_values["NO MODE"].values())
        pil_image = effects.apply_basic_effects(self.image_pil, *basic_effects_values)
        self.qimage = toqimage(pil_image)
        self.frame_ready_signal.emit(QPixmap.fromImage(self.qimage))
