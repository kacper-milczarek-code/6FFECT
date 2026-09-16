from PySide6.QtCore import QThread, Signal, QMutex, QMutexLocker, QWaitCondition
from PySide6.QtGui import QImage
from PIL.ImageQt import toqimage
import src.utils as utils
import src.effects as effects
import src.config as cfg
import numpy as np


class ProcessEffects:
    def __init__(self):
        self.img_w = 0
        self.img_h = 0
        self.curr_block_size = None
        self.curr_np_img = None

        self.coverage = 0
        self.hole_size = 0

        self.fade = False
        self.clean_np_img = None
        self.positions = np.array([])
        self.liner_glitch_mode = False
        self.liner_strength = 10

        self.rainbower_spread = 0

    def process_flipper(self) -> np.ndarray:
        self.curr_np_img = effects.flipper(self.curr_np_img, self.img_h, self.img_w, self.curr_block_size)
        return self.curr_np_img

    def process_fader(self) -> np.ndarray:
        frame_np = effects.fader(self.curr_np_img, self.img_h, self.img_w, self.coverage, self.hole_size)
        return frame_np

    def process_nuker(self) -> np.ndarray:
        self.curr_np_img = effects.nuker(self.curr_np_img)
        return self.curr_np_img

    def process_puzzler(self) -> np.ndarray:
        frame_np = effects.puzzler(self.curr_np_img, self.img_h, self.img_w, self.curr_block_size)
        return frame_np

    def process_liner(self) -> np.ndarray:
        if self.positions.size == 0:
            self.fade = not self.fade
            self.positions = np.random.choice(np.arange(self.img_h), self.img_h, replace=False)

        self.curr_np_img = effects.liner(self.curr_np_img, self.liner_strength, self.positions,
                                         self.fade, self.clean_np_img, self.liner_glitch_mode)
        self.positions = np.delete(self.positions, slice(0, self.liner_strength))
        return self.curr_np_img

    def process_rainbower(self) -> np.ndarray:
        frame_np = effects.rainbower(self.curr_np_img, self.img_h, self.img_w,
                                     self.curr_block_size, self.rainbower_spread)
        return frame_np


class EffectsManager(QThread):
    display_frame_ready_signal = Signal(QImage)
    save_frame_ready_signal = Signal(np.ndarray)

    def __init__(self):
        super().__init__()
        self.original_qimage = None
        self.qimage = None
        self.np_img = None
        self.image_pil = None

        self.mutex = QMutex()
        self.pause_condition = QWaitCondition()

        self.is_running = True
        self.is_paused = True
        self.closing_thread = False
        self.emit_clean_frame = False
        self.emit_frame_for_save = False

        self.process_effects = ProcessEffects()

        self.fps = None

        self.params_setters = {
            "SPEED": lambda v: setattr(self, "fps", v),
            "HOLE SIZE": lambda v: setattr(self.process_effects, "hole_size", v),
            "COVERAGE": lambda v: setattr(self.process_effects, "coverage", v),
            "SPREAD": lambda v: setattr(self.process_effects, "rainbower_spread", v)
        }
        self.effects_callables = {
            "FLIPPER": self.process_effects.process_flipper,
            "FADER": self.process_effects.process_fader,
            "NUKER": self.process_effects.process_nuker,
            "PUZZLER": self.process_effects.process_puzzler,
            "LINER": self.process_effects.process_liner,
            "RAINBOWER": self.process_effects.process_rainbower,
        }

    def load_image_variables(self, image: QImage):
        self.original_qimage = image
        self.image_pil = utils.qimage_to_pil(image)
        self.apply_no_mode_parameters()

    def init_effects_loop_variables(self):
        self.process_effects.img_w = self.qimage.width()
        self.process_effects.img_h = self.qimage.height()
        self.process_effects.curr_np_img = self.np_img.copy()
        self.process_effects.clean_np_img = self.np_img.copy()

        self.process_effects.coverage = cfg.current_values["FADER"]["COVERAGE"]
        self.process_effects.hole_size = cfg.current_values["FADER"]["HOLE SIZE"]
        self.process_effects.fade = False
        self.process_effects.positions = np.array([])
        self.process_effects.rainbower_spread = cfg.current_values["RAINBOWER"]["SPREAD"]

        if cfg.current_effect != "NO MODE":
            self.fps = cfg.current_values[cfg.current_effect]["SPEED"]
            self.resume()

    def update_block_size(self):
        block_sizes = utils.calculate_block_sizes(self.qimage.width(), self.qimage.height())
        if "BLOCK SIZE" in cfg.current_values[cfg.current_effect]:
            cfg.current_values[cfg.current_effect]["BLOCK SIZE"] = len(block_sizes)
            cfg.sliders_settings[cfg.current_effect]["BLOCK SIZE"]["ui_range"] = [1, len(block_sizes)]
            cfg.sliders_settings[cfg.current_effect]["BLOCK SIZE"]["range_values"] = block_sizes.copy()
            self.process_effects.curr_block_size = max(block_sizes)

    def run(self):
        while self.is_running:
            with QMutexLocker(self.mutex):
                while self.is_paused:
                    if self.emit_clean_frame:
                        self.display_frame_ready_signal.emit(self.qimage.copy())
                        self.emit_clean_frame = False
                    self.pause_condition.wait(self.mutex)

            if cfg.current_effect != "NO MODE":
                frame_np = self.effects_callables[cfg.current_effect]()
                if isinstance(frame_np, np.ndarray):
                    if self.emit_frame_for_save:
                        self.save_frame_ready_signal.emit(frame_np.copy())
                    self.display_frame_ready_signal.emit(utils.ndarray_to_qimage(frame_np))

            if not self.closing_thread:
                self.msleep(int(1000 / self.fps))

    def pause(self):
        """
        Switches the worker thread from frame-emitting loop to waiting loop.
        """
        with QMutexLocker(self.mutex):
            self.is_paused = True

    def resume(self):
        """
        Switches the worker thread from waiting loop to frame-emitting loop .
        """
        with QMutexLocker(self.mutex):
            self.is_running = True
            self.is_paused = False
            self.pause_condition.wakeAll()

    def stop(self):
        """
        Stops the worker thread.
        Used only when closing the application via closeEvent.
        """
        with QMutexLocker(self.mutex):
            self.closing_thread = True
            self.is_running = False
            self.is_paused = False
            self.pause_condition.wakeAll()

    def apply_effects_parameters(self, parameter: str, value: int):
        """
        Retrieves the value from the moved slider and applies it to the effect loop variables.
        For the block size parameter resets the current image frame to image from self.np_img variable.
        Works only when an effect is selected.
        """
        if parameter == "BLOCK SIZE":
            self.process_effects.curr_np_img = self.np_img.copy()
            value = cfg.sliders_settings[cfg.current_effect]["BLOCK SIZE"]["range_values"][value - 1]
            self.process_effects.curr_block_size = value
        else:
            setter = self.params_setters[parameter]
            setter(value)

    def apply_no_mode_parameters(self):
        """
        Retrieves the value from the moved slider and applies it to image parameters (brightness, saturation, contrast).
        Updates the self.qimage and self.np_img variables with the image with new parameters applied.
        Works only when no effect is selected.
        """
        basic_effects_values = (utils.ui_to_raw(v, *cfg.NO_MODE_SLIDERS_SETTINGS) for v in
                                cfg.current_values["NO MODE"].values())
        pil_image = effects.apply_basic_effects(self.image_pil, *basic_effects_values)
        self.qimage = toqimage(pil_image)
        self.np_img = utils.qimage_to_ndarray(self.qimage)
        if cfg.current_effect == "NO MODE":
            self.display_frame_ready_signal.emit(self.qimage)

    def set_liner_glitch_mode(self, mode: bool):
        self.process_effects.liner_glitch_mode = mode
        self.process_effects.fade = False
        self.process_effects.positions = np.array([])
        self.process_effects.curr_np_img = self.np_img.copy()

    def start_export(self):
        self.emit_frame_for_save = True

    def stop_export(self):
        self.emit_frame_for_save = False
