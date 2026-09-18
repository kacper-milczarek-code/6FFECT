from PySide6.QtWidgets import QApplication, QLabel, QPushButton, QWidget, QFileDialog, QSlider, QButtonGroup
from PySide6.QtGui import QPixmap, QMouseEvent, QImage
from PySide6.QtCore import Qt, QEvent
from src.engine import EffectsManager
from src.ui.effect_export_ui import ExportDialogs
from src.video_exporter import VideoExporter
from src.utils import closest_window_res
import src.sound_manager as sound_manager
import src.config as cfg


class MainWindow(QWidget):

    def make_widget(self, widget_class, **kwargs):
        """Universal function for creating and configuring Qt widgets

        Kwargs:
            text (str): Set widget text via setText
            geometry (tuple[int, int, int, int]): Widget coordinates and size (x, y, width, height).
            name (str): Set object name via setObjectName().
            group (str): 'UIGroup' property used for show/hide operations.
            wgt_type (str): Widget category ('btn', 'slider', 'example_img_btn') to install the event filter.
            action (callable): Callback function connected to the clicked signal.
            value (int): Initial value for QSlider widgets.
            sld_lbl (QLabel): Label object to display the slider's current name and value.
            sld_idx (int): Index key used to fetch slider names from current_sliders.
            effect (str): Name of the effect associated with the button, passed to the action callback.
            img_path (str): File path to the image passed to the action callback, displayed by image_display.
        """
        widget = widget_class(self)

        if "text" in kwargs:
            widget.setText(kwargs["text"])
        if "geometry" in kwargs:
            widget.setGeometry(*kwargs["geometry"])
        if "name" in kwargs:
            widget.setObjectName(kwargs["name"])
        if "group" in kwargs:
            widget.setProperty("UIGroup", kwargs["group"])

        if "wgt_type" in kwargs:
            wgt_type = kwargs["wgt_type"]
            widget.setProperty("WidgetType", wgt_type)
            if wgt_type in ("btn", "slider", "example_img_btn"):
                widget.installEventFilter(self)

        if "action" in kwargs and hasattr(widget, "clicked") and isinstance(widget, QPushButton):
            action = kwargs["action"]
            if "effect" in kwargs:
                effect = kwargs["effect"]
                widget.clicked.connect(
                    lambda checked, w=widget: (self.highlight_effect_button(w), action(effect, checked)))
                widget.setCheckable(True)
                self.effects_buttons.addButton(widget)
            elif "img_path" in kwargs:
                img_path = kwargs["img_path"]
                widget.clicked.connect(lambda checked, p=img_path: action(p))
            else:
                widget.clicked.connect(kwargs["action"])
        if widget_class is QSlider:
            widget.setOrientation(Qt.Orientation.Horizontal)
            widget.setRange(1, 100)

            if "value" in kwargs:
                widget.setValue(kwargs["value"])

            if "sld_lbl" in kwargs and "sld_idx" in kwargs:
                lbl, idx = kwargs["sld_lbl"], kwargs["sld_idx"]
                widget.valueChanged.connect(lambda val, lb=lbl, i=idx: self.handle_slider_moved(val, lb, i))

        return widget

    def __init__(self):
        super().__init__()
        screen_w, screen_h = 960, 540
        ui_width, ui_height = 320, 170
        self.setWindowTitle("6FFECT")
        self.setFixedSize(screen_w + ui_width, screen_h + ui_height)
        self.setAcceptDrops(True)
        with open("src/ui/style.qss", "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())
        sound_manager.load_sounds()
        self.effects_buttons = QButtonGroup(self)
        self.effects_buttons.setExclusive(False)
        self.upload_image = None

        self.export_dialogs = ExportDialogs()
        self.effects_manager = EffectsManager()
        self.video_exporter = VideoExporter()

        self.effects_manager.start()
        self.effects_manager.display_frame_ready_signal.connect(self.display_image)
        self.effects_manager.save_frame_ready_signal.connect(self.video_exporter.add_frame)

        self.export_dialogs.export_request_signal.connect(self.handle_start_export)
        self.export_dialogs.progress_dialog.cancel_saving_signal.connect(self.handle_cancel_export)

        self.video_exporter.update_progress_bar_value.connect(self.export_dialogs.update_progress_bar_value)
        self.video_exporter.export_finished_signal.connect(self.handle_finish_export)

        self.current_ui = "menu_widgets"

        # STATIC WIDGETS
        self.image_display = self.make_widget(
            widget_class=QLabel,
            geometry=(0, 0, screen_w, screen_h),
            name="display"
        )
        self.image_display.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.ex_img_label = self.make_widget(
            widget_class=QLabel,
            text="Example images",
            geometry=(screen_w + 50, 7, 250, 30),
            name="ui_labels"
        )

        self.example_img_btn1 = self.make_widget(
            widget_class=QPushButton,
            geometry=(screen_w, 44, 320, 168),
            name="example_img1",
            wgt_type="example_img_btn",
            img_path="assets/example images/img1.png",
            action=self.prepare_image
        )

        self.example_img_btn2 = self.make_widget(
            widget_class=QPushButton,
            geometry=(screen_w, 208, 320, 168),
            name="example_img2",
            wgt_type="example_img_btn",
            img_path="assets/example images/img2.png",
            action=self.prepare_image
        )

        self.example_img_btn3 = self.make_widget(
            widget_class=QPushButton,
            geometry=(screen_w, 372, 320, 168),
            name="example_img3",
            wgt_type="example_img_btn",
            img_path="assets/example images/img3.png",
            action=self.prepare_image
        )

        # MENU WIDGETS
        self.upl_btn = self.make_widget(
            widget_class=QPushButton,
            text="UPLOAD IMAGE",
            geometry=(255, 195, 450, 150),
            name="upload",
            group="menu_widgets",
            action=self.open_file_dialog,
            wgt_type="btn"
        )

        self.name_lbl = self.make_widget(
            widget_class=QLabel,
            text="6FFECT",
            geometry=(210, 475, 1000, 300),
            group="menu_widgets",
            name="name"
        )

        self.additional_info_lbl = self.make_widget(
            widget_class=QLabel,
            text="Drop anywhere or choose an example",
            geometry=(155, 360, 650, 40),
            group="menu_widgets",
            name="add_image_info"
        )

        # MAIN WIDGETS
        self.sliders_lbl = self.make_widget(
            widget_class=QLabel,
            text="PARAMETERS: IMAGE",
            geometry=(5, screen_h + 5, 500, 30),
            group="main_widgets"
        )

        self.effects_lbl = self.make_widget(
            widget_class=QLabel,
            text="EFFECTS",
            geometry=(590, screen_h + 5, 500, 30),
            group="main_widgets"
        )

        self.settings_lbl = self.make_widget(
            widget_class=QLabel,
            text="SETTINGS",
            geometry=(1050, screen_h + 5, 500, 30),
            group="main_widgets"
        )

        self.slider1_lbl = self.make_widget(
            widget_class=QLabel,
            text=f"BRIGHTNESS: {cfg.DEFAULT_VALUES['NO MODE']['BRIGHTNESS']}",
            geometry=(205, screen_h + 44, 300, 30),
            group="main_widgets",
            wgt_type="slider_label"
        )

        self.slider2_lbl = self.make_widget(
            widget_class=QLabel,
            text=f"SATURATION: {cfg.DEFAULT_VALUES['NO MODE']['SATURATION']}",
            geometry=(205, screen_h + 84, 300, 30),
            group="main_widgets",
            wgt_type="slider_label"
        )

        self.slider3_lbl = self.make_widget(
            widget_class=QLabel,
            text=f"CONTRAST: {cfg.DEFAULT_VALUES['NO MODE']['CONTRAST']}",
            geometry=(205, screen_h + 124, 300, 30),
            group="main_widgets",
            wgt_type="slider_label"
        )

        self.slider1 = self.make_widget(
            widget_class=QSlider,
            geometry=(5, screen_h + 45, 190, 30),
            group="main_widgets",
            wgt_type="slider",
            sld_lbl=self.slider1_lbl,
            sld_idx=0,
            value=cfg.DEFAULT_VALUES["NO MODE"]["BRIGHTNESS"]
        )

        self.slider2 = self.make_widget(
            widget_class=QSlider,
            geometry=(5, screen_h + 85, 190, 30),
            group="main_widgets",
            wgt_type="slider",
            sld_lbl=self.slider2_lbl,
            sld_idx=1,
            value=cfg.DEFAULT_VALUES["NO MODE"]["SATURATION"]
        )

        self.slider3 = self.make_widget(
            widget_class=QSlider,
            geometry=(5, screen_h + 125, 190, 30),
            group="main_widgets",
            wgt_type="slider",
            sld_lbl=self.slider3_lbl,
            sld_idx=2,
            value=cfg.DEFAULT_VALUES["NO MODE"]["CONTRAST"]
        )

        self.flipper_btn = self.make_widget(
            widget_class=QPushButton,
            text="FLIPPER",
            geometry=(420, screen_h + 50, 150, 50),
            group="main_widgets",
            action=self.handle_effect_btn_click,
            wgt_type="btn",
            effect="FLIPPER"
        )

        self.fader_btn = self.make_widget(
            widget_class=QPushButton,
            text="FADER",
            geometry=(580, screen_h + 50, 150, 50),
            group="main_widgets",
            action=self.handle_effect_btn_click,
            wgt_type="btn",
            effect="FADER"
        )

        self.nuker_btn = self.make_widget(
            widget_class=QPushButton,
            text="NUKER",
            geometry=(740, screen_h + 50, 150, 50),
            group="main_widgets",
            action=self.handle_effect_btn_click,
            wgt_type="btn",
            effect="NUKER"
        )

        self.puzzler_btn = self.make_widget(
            widget_class=QPushButton,
            text="PUZZLER",
            geometry=(420, screen_h + 110, 150, 50),
            group="main_widgets",
            action=self.handle_effect_btn_click,
            wgt_type="btn",
            effect="PUZZLER"
        )

        self.liner_btn = self.make_widget(
            widget_class=QPushButton,
            text="LINER",
            geometry=(580, screen_h + 110, 150, 50),
            group="main_widgets",
            action=self.handle_effect_btn_click,
            wgt_type="btn",
            effect="LINER"
        )

        self.rainbower_btn = self.make_widget(
            widget_class=QPushButton,
            text="RAINBOWER",
            geometry=(740, screen_h + 110, 150, 50),
            group="main_widgets",
            action=self.handle_effect_btn_click,
            wgt_type="btn",
            effect="RAINBOWER"
        )
        # SETTINGS WIDGETS
        self.save_btn = self.make_widget(
            widget_class=QPushButton,
            text="SAVE VIDEO",
            geometry=(965, screen_h + 50, 150, 50),
            group="main_widgets",
            action=self.export_dialogs.launch_export_ui,
            wgt_type="btn"
        )

        self.new_img_btn = self.make_widget(
            widget_class=QPushButton,
            text="NEW IMAGE",
            geometry=(1125, screen_h + 50, 150, 50),
            group="main_widgets",
            action=self.reset_ui_to_image_chooser,
            wgt_type="btn"
        )

        self.reset_btn = self.make_widget(
            widget_class=QPushButton,
            text="RESET",
            geometry=(965, screen_h + 110, 150, 50),
            group="main_widgets",
            action=self.reset_to_default_values,
            wgt_type="btn"
        )

        self.mute_btn = self.make_widget(
            widget_class=QPushButton,
            text="MUTE SOUNDS",
            geometry=(1125, screen_h + 110, 150, 50),
            group="main_widgets",
            action=sound_manager.toggle_mute,
            wgt_type="btn",
            name="mute"
        )
        self.mute_btn.setCheckable(True)

        self.liner_switch_btn = self.make_widget(
            widget_class=QPushButton,
            text="GLITCH",
            geometry=(5, screen_h + 80, 190, 80),
            group="main_widgets",
            wgt_type="btn",
            name="liner_switch",
            action=lambda checked: self.handle_liner_switch_btn_click(checked)
        )
        self.liner_switch_btn.setCheckable(True)

        self.liner_switch_lbl = self.make_widget(
            widget_class=QLabel,
            text="ON / [OFF]",
            geometry=(205, screen_h + 100, 300, 30),
            group="main_widgets",
            wgt_type="slider_label"
        )
        self.liner_switch_btn.hide()
        self.liner_switch_lbl.hide()
        self.switch_ui_to("menu_widgets")

    def switch_ui_to(self, ui_group: str):
        """Toggle visibility of widgets based on their UIGroup property."""
        self.current_ui = ui_group

        for widget in self.findChildren(QWidget):
            group = widget.property("UIGroup")
            if not group:
                continue

            if group == ui_group:
                if widget not in (self.liner_switch_btn, self.liner_switch_lbl):
                    widget.show()
            else:
                widget.hide()

    def eventFilter(self, watched: QWidget, event, /):
        """
        Triggers sound effects on widget hover and click release events.
        """
        wgt_type = watched.property("WidgetType")
        if event.type() == QEvent.Type.Enter:
            if wgt_type in ("btn", "slider", "example_img_btn"):
                sound_manager.play(wgt_type, "hover")
        elif isinstance(event, QMouseEvent) and event.type() == QEvent.Type.MouseButtonRelease:
            if event.button() == Qt.MouseButton.LeftButton and watched.rect().contains(event.position().toPoint()):
                if wgt_type in ("btn", "example_img_btn"):
                    sound_manager.play(wgt_type, "click")
        return super().eventFilter(watched, event)

    def highlight_effect_button(self, current_button: QPushButton):
        """
        Clears checked state of previously selected button.
        Ensures that only a single button (or none) can be selected at a time.
        """
        for effect_button in self.effects_buttons.buttons():
            if effect_button.isChecked() and effect_button is not current_button:
                effect_button.setChecked(False)

    def handle_slider_moved(self, value, label, sld_index):
        """
        Processes slider movement and calls functions handling slider values.
        """
        label.setText(f"{cfg.current_sliders_parameters[sld_index]}: {value}")
        cfg.current_values[cfg.current_effect][cfg.current_sliders_parameters[sld_index]] = value
        if cfg.current_effect == "NO MODE":
            self.effects_manager.apply_no_mode_parameters()
        else:
            self.effects_manager.apply_effects_parameters(cfg.current_sliders_parameters[sld_index], value)

    def change_sliders(self):
        """
        Updates slider section corresponding with selected effect.
        """
        sliders_labels = (self.slider1_lbl, self.slider2_lbl, self.slider3_lbl)
        sliders = (self.slider1, self.slider2, self.slider3)
        [(sld_lab.hide(), sld.hide()) for sld_lab, sld in zip(sliders_labels, sliders)]
        [s.hide() for s in sliders]
        for i in range(len(cfg.current_sliders_parameters)):
            parameter = cfg.current_sliders_parameters[i]
            value = cfg.current_values[cfg.current_effect][parameter]
            slider_range = cfg.sliders_settings[cfg.current_effect][parameter]["ui_range"]
            sliders_labels[i].setText(f"{parameter}: {value}")
            sliders[i].setRange(*slider_range)
            sliders[i].setValue(value)
            if self.current_ui != "menu_widgets":
                sliders_labels[i].show()
                sliders[i].show()

    def reset_to_default_values(self):
        """
        Resets all values in cfg.current_values to default values in cfg.DEFAULT_VALUES.
        Resets effect and widget settings to default values.
        Switches ui to menu_widgets.
        """
        cfg.current_values = {m: s.copy() for m, s in cfg.DEFAULT_VALUES.items()}
        self.effects_manager.update_block_size()
        self.effects_manager.apply_no_mode_parameters()
        self.effects_manager.init_effects_loop_variables()
        self.handle_liner_switch_btn_click(False)
        self.liner_switch_btn.setChecked(False)
        self.change_sliders()

    def reset_ui_to_image_chooser(self):
        self.reset_to_default_values()
        self.switch_ui_to("menu_widgets")
        self.sliders_lbl.setText("PARAMETERS: IMAGE")
        self.effects_manager.is_paused = True
        self.image_display.clear()
        cfg.current_effect = "NO MODE"
        cfg.current_sliders_parameters = ["BRIGHTNESS", "SATURATION", "CONTRAST"]
        self.change_sliders()
        for effect_button in self.effects_buttons.buttons():
            if effect_button.isChecked():
                effect_button.setChecked(False)

    def handle_effect_btn_click(self, effect: str, checked: bool):
        if checked:
            if effect == "LINER":
                self.liner_switch_btn.show()
                self.liner_switch_lbl.show()
            else:
                self.liner_switch_btn.hide()
                self.liner_switch_lbl.hide()
            cfg.current_effect = effect
            cfg.current_sliders_parameters = [param for param in cfg.sliders_settings[cfg.current_effect].keys()]
            self.effects_manager.update_block_size()
            self.change_sliders()
            self.sliders_lbl.setText(f"PARAMETERS: {effect}")
            self.effects_manager.init_effects_loop_variables()
        else:
            cfg.current_effect = "NO MODE"
            cfg.current_sliders_parameters = [param for param in cfg.sliders_settings[cfg.current_effect].keys()]
            self.change_sliders()
            self.sliders_lbl.setText(f"PARAMETERS: IMAGE")
            self.effects_manager.emit_clean_frame = True
            self.effects_manager.pause()
            if effect == "LINER":
                self.liner_switch_btn.hide()
                self.liner_switch_lbl.hide()

    def handle_liner_switch_btn_click(self, checked: bool):
        if checked:
            self.liner_switch_lbl.setText("[ON] / OFF")
            self.effects_manager.set_liner_glitch_mode(True)
        else:
            self.liner_switch_lbl.setText("ON / [OFF]")
            self.effects_manager.set_liner_glitch_mode(False)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            self.prepare_image(file_path)

    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Choose image",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.webp);;Wszystkie pliki (*.*)"
        )
        if file_path:
            self.prepare_image(file_path)

    def prepare_image(self, img_path: str):
        """
        Prepares image for effects application.
        Converts image to 16:9 or 9:16 format.
        Triggers initialization of image and effect loop variables.
        """
        if self.current_ui == "menu_widgets":
            self.switch_ui_to("main_widgets")
        self.upload_image = QImage(img_path)
        target_resolution = closest_window_res(self.upload_image)
        if target_resolution != "correct":
            w, h = target_resolution
            self.upload_image = self.upload_image.scaled(w, h)
        self.effects_manager.load_image_variables(self.upload_image)
        self.effects_manager.init_effects_loop_variables()

    def display_image(self, image: QImage):
        """
        Adjusts the image size to the display and displays it.
        """
        if self.current_ui != "menu_widgets":
            pixmap = QPixmap.fromImage(image)
            if pixmap.height() > pixmap.width():
                new_width = int(pixmap.width() * (self.image_display.height() / pixmap.height()))
                self.image_display.setPixmap(pixmap.scaled(new_width, self.image_display.height()))
            else:
                self.image_display.setPixmap(pixmap.scaled(self.image_display.size()))

    def closeEvent(self, event):
        """
        Handles window close event.
        Ensures proper termination of EffectsManager thread.
        Prevents thread-related memory leaks.
        """
        if self.effects_manager.isRunning():
            self.effects_manager.stop()
            self.effects_manager.wait()

        event.accept()

    def handle_start_export(self, file_path: str, duration: int):
        """
        Handles save click from dialog box.
        Calculates and passes parameters to video_exporter.
        Turns on the recording flag.
        """
        fps = cfg.current_values[cfg.current_effect]["SPEED"]
        total_frames = duration * fps
        frame_size = (self.effects_manager.qimage.width(), self.effects_manager.qimage.height())

        self.video_exporter.start_recording(file_path, fps, frame_size, total_frames)

        self.effects_manager.start_export()

    def handle_finish_export(self):
        self.effects_manager.stop_export()
        self.export_dialogs.close_progress_dialog()
        self.export_dialogs.open_success_dialog()

    def handle_cancel_export(self):
        self.effects_manager.stop_export()
        self.video_exporter.cancel()
        self.export_dialogs.close_progress_dialog()
        self.export_dialogs.cancel_dialog.show()


def app_init():
    app = QApplication()
    window = MainWindow()
    window.show()
    app.exec()
