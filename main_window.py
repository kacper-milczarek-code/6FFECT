from PySide6.QtWidgets import QApplication, QLabel, QPushButton, QWidget, QFileDialog, QSlider
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QEvent
from src.sound_manager import play, load_sounds


class MainWindow(QWidget):

    def make_widget(self, widget_class, text=None, geometry=None, name=None, group=None, wgt_type=None, action=None):
        widget = widget_class(self)
        if text:
            widget.setText(text)
        if geometry:
            widget.setGeometry(*geometry)
        if name:
            widget.setObjectName(name)
        if group:
            widget.setProperty("UIGroup", group)
        if wgt_type:
            widget.setProperty("WidgetType", wgt_type)
        if action:
            widget.clicked.connect(action)
        if widget_class == QSlider:
            widget.setOrientation(Qt.Orientation.Horizontal)
        if wgt_type in ("btn", "slider", "example_img_btn"):
            widget.installEventFilter(self)
        return widget

    def __init__(self):
        super().__init__()
        screen_w, screen_h = 960, 540
        ui_width, ui_height = 320, 170
        self.setWindowTitle("6FFECT")
        self.resize(screen_w + ui_width, screen_h + ui_height)
        with open("assets/styles/style.qss", "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())
        load_sounds()

        # STATIC WIDGETS
        self.image_display = self.make_widget(
            widget_class=QLabel,
            geometry=(0, 0, screen_w, screen_h),
            name="display"
        )

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
            wgt_type="example_img_btn"
        )

        self.example_img_btn2 = self.make_widget(
            widget_class=QPushButton,
            geometry=(screen_w, 208, 320, 168),
            name="example_img2",
            wgt_type="example_img_btn"
        )

        self.example_img_btn3 = self.make_widget(
            widget_class=QPushButton,
            geometry=(screen_w, 372, 320, 168),
            name="example_img3",
            wgt_type="example_img_btn"
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

        # self.hide_ui(ui_group="menu_widgets")

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

        self.slider1 = self.make_widget(
            widget_class=QSlider,
            geometry=(5, screen_h + 45, 190, 30),
            group="main_widgets",
            wgt_type="slider"
        )

        self.slider2 = self.make_widget(
            widget_class=QSlider,
            geometry=(5, screen_h + 85, 190, 30),
            group="main_widgets",
            wgt_type="slider"
        )

        self.slider3 = self.make_widget(
            widget_class=QSlider,
            geometry=(5, screen_h + 125, 190, 30),
            group="main_widgets",
            wgt_type="slider"
        )

        self.slider1_lbl = self.make_widget(
            widget_class=QLabel,
            text="Brightness: 50",
            geometry=(205, screen_h + 44, 300, 30),
            group="main_widgets",
            wgt_type="slider_label"
        )

        self.slider2_lbl = self.make_widget(
            widget_class=QLabel,
            text="Saturation: 50",
            geometry=(205, screen_h + 84, 300, 30),
            group="main_widgets",
            wgt_type="slider_label"
        )

        self.slider3_lbl = self.make_widget(
            widget_class=QLabel,
            text="Contrast: 50",
            geometry=(205, screen_h + 124, 300, 30),
            group="main_widgets",
            wgt_type="slider_label"
        )

        self.flipper_btn = self.make_widget(
            widget_class=QPushButton,
            text="FLIPPER",
            geometry=(420, screen_h + 50, 150, 50),
            group="main_widgets",
            action=self.process_effect,
            wgt_type="btn"
        )

        self.fader_btn = self.make_widget(
            widget_class=QPushButton,
            text="FADER",
            geometry=(580, screen_h + 50, 150, 50),
            group="main_widgets",
            action=self.process_effect,
            wgt_type="btn"
        )

        self.nuker_btn = self.make_widget(
            widget_class=QPushButton,
            text="NUKER",
            geometry=(740, screen_h + 50, 150, 50),
            group="main_widgets",
            action=self.process_effect,
            wgt_type="btn"
        )

        self.puzzler_btn = self.make_widget(
            widget_class=QPushButton,
            text="PUZZLER",
            geometry=(420, screen_h + 110, 150, 50),
            group="main_widgets",
            action=self.process_effect,
            wgt_type="btn"
        )

        self.liner_btn = self.make_widget(
            widget_class=QPushButton,
            text="LINER",
            geometry=(580, screen_h + 110, 150, 50),
            group="main_widgets",
            action=self.process_effect,
            wgt_type="btn"
        )

        self.rainbower_btn = self.make_widget(
            widget_class=QPushButton,
            text="RAINBOWER",
            geometry=(740, screen_h + 110, 150, 50),
            group="main_widgets",
            action=self.process_effect,
            wgt_type="btn"
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
            text="RESET IMAGE",
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

    def eventFilter(self, watched, event, /):
        wgt_type = watched.property("WidgetType")
        if event.type() == QEvent.Type.Enter:
            if wgt_type in ("btn", "slider", "example_img_btn"):
                play(wgt_type, "hover")
        elif event.type() == QEvent.Type.MouseButtonPress:
            if event.button() == Qt.MouseButton.LeftButton:
                if wgt_type in ("btn", "example_img_btn"):
                    play(wgt_type, "click")
        return super().eventFilter(watched, event)

    def process_effect(self):
        pass

    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Wybierz obraz",
            "",
            "Obrazy (*.png *.jpg *.jpeg *.bmp *.webp);;Wszystkie pliki (*.*)"
        )
        if file_path:
            print(f"Wybrano plik: {file_path}")
            pixmap = QPixmap(file_path)
            self.image_display.setPixmap(pixmap.scaled(self.image_display.size()))


def app_init():
    app = QApplication()
    okno = MainWindow()
    okno.show()
    app.exec()


app_init()
