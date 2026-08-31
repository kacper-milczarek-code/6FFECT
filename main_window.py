from PySide6.QtWidgets import QApplication, QLabel, QPushButton, QWidget, QFileDialog, QSlider, QButtonGroup
from PySide6.QtGui import QPixmap, QMouseEvent, QImage
from PySide6.QtCore import Qt, QEvent
from engine import EffectsManager
from src.utils import closest_window_res
import src.sound_manager as sm
import src.config as cfg


class MainWindow(QWidget):

    def make_widget(self, widget_class, **kwargs):
        """
        Universal function for creating and configuring Qt widgets
        Kwargs:
            text (str): Set widget text via setText
            geometry (tuple[int, int, int, int]): Widget coordinates and size (x, y, width, height).
            name (str): Set object name via setObjectName().
            group (str): 'UIGroup' property used for show/hide operations.
            wgt_type (str): Widget category ('btn', 'slider', 'example_img_btn') to install the event filter.
            action (callable): Callback function connected to the clicked signal.
            value (int): Initial value for QSlider widgets.
            sld_lbl (QLabel): Label object to display the slider's current name and value.
            sld_num (int): Index key used to fetch slider names from current_sliders.
            effect (str): Name of the effect associated with the button, passed to the action callback.
            img_path (str): File path to the image passed to the action callback, displayed by image_display.
        """
        widget = widget_class(self)

        if "text" in kwargs: widget.setText(kwargs["text"])
        if "geometry" in kwargs: widget.setGeometry(*kwargs["geometry"])
        if "name" in kwargs: widget.setObjectName(kwargs["name"])
        if "group" in kwargs: widget.setProperty("UIGroup", kwargs["group"])

        if "wgt_type" in kwargs:
            wgt_type = kwargs["wgt_type"]
            widget.setProperty("WidgetType", wgt_type)
            if wgt_type in ("btn", "slider", "example_img_btn"):
                widget.installEventFilter(self)

        if "action" in kwargs and hasattr(widget, "clicked") and isinstance(widget, QPushButton):
            action = kwargs["action"]
            if "effect" in kwargs:
                effect = kwargs["effect"]
                widget.clicked.connect(lambda checked, w=widget: (self.highlight_button(w), action(effect, checked)))
                widget.setCheckable(True)
                self.effects_buttons.addButton(widget)
            elif "img_path" in kwargs:
                img_path = kwargs["img_path"]
                widget.clicked.connect(lambda checked, p=img_path: action(p))
            else:
                widget.clicked.connect(kwargs["action"])
        if widget_class == QSlider:
            widget.setOrientation(Qt.Orientation.Horizontal)
            widget.setRange(1, 100)

            if "value" in kwargs:
                widget.setValue(kwargs["value"])

            if "sld_lbl" in kwargs and "sld_num" in kwargs:
                lbl, idx = kwargs["sld_lbl"], kwargs["sld_num"]
                widget.valueChanged.connect(lambda val, lb=lbl, i=idx: self.slider_moved(val, lb, i))

        return widget

    def __init__(self):
        super().__init__()
        screen_w, screen_h = 960, 540
        ui_width, ui_height = 320, 170
        self.setWindowTitle("6FFECT")
        self.setFixedSize(screen_w + ui_width, screen_h + ui_height)
        with open("assets/styles/style.qss", "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())
        sm.load_sounds()
        self.effects_buttons = QButtonGroup(self)
        self.effects_buttons.setExclusive(False)
        self.upload_image = None
        self.effects_manager = EffectsManager()
        self.effects_manager.frame_ready_signal.connect(self.display_image)
        self.image_scaled = False

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
            geometry=(screen_w + 35, 7, 250, 30),
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
            geometry=(100, 360, 800, 30),
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
            text=f"Brightness: {cfg.DEFAULT_VALUES['NO MODE']['BRIGHTNESS']}",
            geometry=(205, screen_h + 44, 300, 30),
            group="main_widgets",
            wgt_type="slider_label"
        )

        self.slider2_lbl = self.make_widget(
            widget_class=QLabel,
            text=f"Saturation: {cfg.DEFAULT_VALUES['NO MODE']['SATURATION']}",
            geometry=(205, screen_h + 84, 300, 30),
            group="main_widgets",
            wgt_type="slider_label"
        )

        self.slider3_lbl = self.make_widget(
            widget_class=QLabel,
            text=f"Contrast: {cfg.DEFAULT_VALUES['NO MODE']['CONTRAST']}",
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
            sld_num=0,
            value=cfg.DEFAULT_VALUES["NO MODE"]["BRIGHTNESS"]
        )

        self.slider2 = self.make_widget(
            widget_class=QSlider,
            geometry=(5, screen_h + 85, 190, 30),
            group="main_widgets",
            wgt_type="slider",
            sld_lbl=self.slider2_lbl,
            sld_num=1,
            value=cfg.DEFAULT_VALUES["NO MODE"]["SATURATION"]
        )

        self.slider3 = self.make_widget(
            widget_class=QSlider,
            geometry=(5, screen_h + 125, 190, 30),
            group="main_widgets",
            wgt_type="slider",
            sld_lbl=self.slider3_lbl,
            sld_num=2,
            value=cfg.DEFAULT_VALUES["NO MODE"]["CONTRAST"]
        )

        self.flipper_btn = self.make_widget(
            widget_class=QPushButton,
            text="FLIPPER",
            geometry=(420, screen_h + 50, 150, 50),
            group="main_widgets",
            action=self.process_effect,
            wgt_type="btn",
            effect="FLIPPER"
        )

        self.fader_btn = self.make_widget(
            widget_class=QPushButton,
            text="FADER",
            geometry=(580, screen_h + 50, 150, 50),
            group="main_widgets",
            action=self.process_effect,
            wgt_type="btn",
            effect="FADER"
        )

        self.nuker_btn = self.make_widget(
            widget_class=QPushButton,
            text="NUKER",
            geometry=(740, screen_h + 50, 150, 50),
            group="main_widgets",
            action=self.process_effect,
            wgt_type="btn",
            effect="NUKER"
        )

        self.puzzler_btn = self.make_widget(
            widget_class=QPushButton,
            text="PUZZLER",
            geometry=(420, screen_h + 110, 150, 50),
            group="main_widgets",
            action=self.process_effect,
            wgt_type="btn",
            effect="PUZZLER"
        )

        self.liner_btn = self.make_widget(
            widget_class=QPushButton,
            text="LINER",
            geometry=(580, screen_h + 110, 150, 50),
            group="main_widgets",
            action=self.process_effect,
            wgt_type="btn",
            effect="LINER"
        )

        self.rainbower_btn = self.make_widget(
            widget_class=QPushButton,
            text="RAINBOWER",
            geometry=(740, screen_h + 110, 150, 50),
            group="main_widgets",
            action=self.process_effect,
            wgt_type="btn",
            effect="RAINBOWER"
        )
        # SETTINGS WIDGETS
        self.save_btn = self.make_widget(
            widget_class=QPushButton,
            text="SAVE",
            geometry=(965, screen_h + 50, 150, 50),
            group="main_widgets",
            action=self.process_effect,
            wgt_type="btn"
        )

        self.new_img_btn = self.make_widget(
            widget_class=QPushButton,
            text="NEW IMAGE",
            geometry=(1125, screen_h + 50, 150, 50),
            group="main_widgets",
            action=self.process_effect,
            wgt_type="btn"
        )

        self.reset_btn = self.make_widget(
            widget_class=QPushButton,
            text="RESET",
            geometry=(965, screen_h + 110, 150, 50),
            group="main_widgets",
            action=self.process_effect,
            wgt_type="btn"
        )

        self.mute_btn = self.make_widget(
            widget_class=QPushButton,
            text="MUTE SOUNDS",
            geometry=(1125, screen_h + 110, 150, 50),
            group="main_widgets",
            action=self.process_effect,
            wgt_type="btn"
        )
        # self.hide_ui("main_widgets")
        self.hide_ui("menu_widgets")

    def hide_ui(self, ui_group: str):
        for widget in self.findChildren(QWidget):
            if widget.property("UIGroup") == ui_group:
                widget.hide()

    def eventFilter(self, watched: QWidget, event, /):
        """
        Triggers sound effects on widget hover and click release events.
        """
        wgt_type = watched.property("WidgetType")
        if event.type() == QEvent.Type.Enter:
            if wgt_type in ("btn", "slider", "example_img_btn"):
                sm.play(wgt_type, "hover")
        elif isinstance(event, QMouseEvent) and event.type() == QEvent.Type.MouseButtonRelease:
            if event.button() == Qt.MouseButton.LeftButton and watched.rect().contains(event.position().toPoint()):
                if wgt_type in ("btn", "example_img_btn"):
                    sm.play(wgt_type, "click")
        return super().eventFilter(watched, event)

    def highlight_button(self, current_button: QPushButton):
        """
        Clears the checked state of the previously selected button.
        Ensures that only a single button (or none) can be selected at a time.
        """
        for effect_button in self.effects_buttons.buttons():
            if effect_button.isChecked() and effect_button is not current_button:
                effect_button.setChecked(False)

    def slider_moved(self, value, label, sld_index):
        label.setText(f"{cfg.current_sliders[sld_index]}: {value}")
        cfg.current_values[cfg.current_effect][cfg.current_sliders[sld_index]] = value
        if cfg.current_effect == "NO MODE":
            self.effects_manager.apply_no_mode_parameters()
        else:
            self.effects_manager.apply_effects_parameters(sld_index)

    def process_effect(self, effect, checked):
        if checked:
            cfg.current_effect = effect
            self.sliders_lbl.setText(f"PARAMETERS: {effect}")
        else:
            cfg.current_effect = "NO MODE"
            self.sliders_lbl.setText(f"PARAMETERS: IMAGE")

    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Wybierz obraz",
            "",
            "Obrazy (*.png *.jpg *.jpeg *.bmp *.webp);;Wszystkie pliki (*.*)"
        )
        if file_path:
            print(f"Wybrano plik: {file_path}")
            self.prepare_image(file_path)

    def prepare_image(self, img_path):
        """

        """
        self.upload_image = QImage(img_path)
        target_resolution = closest_window_res(self.upload_image)
        if target_resolution != "correct":
            w, h = target_resolution
            self.upload_image = self.upload_image.scaled(w, h)
        self.effects_manager.load_image_variables(self.upload_image)
        self.image_scaled = False
        pixmap = QPixmap.fromImage(self.upload_image)
        self.display_image(pixmap)
        self.effects_manager.apply_no_mode_parameters()

    def display_image(self, pixmap):
        if pixmap.height() > pixmap.width():
            new_width = int(pixmap.width() * (self.image_display.height() / pixmap.height()))
            self.image_display.setPixmap(pixmap.scaled(new_width, self.image_display.height()))
        else:
            self.image_display.setPixmap(pixmap.scaled(self.image_display.size()))


def app_init():
    app = QApplication()
    window = MainWindow()
    window.show()
    app.exec()


app_init()
