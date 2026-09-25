from PySide6.QtWidgets import QDialog, QLabel, QPushButton, QSlider, QProgressBar, QWidget, QFileDialog
from PySide6.QtGui import QMouseEvent
from PySide6.QtCore import Qt, QEvent, QObject, Signal, QStandardPaths
from src.paths import STYLE_QSS_PATH

import src.config as cfg
import src.sound_manager as sound_manager


class SoundFilter(QObject):
    def eventFilter(self, watched: QObject, event) -> bool:
        """
        Triggers sound effects on widget hover and click release events.
        """
        wgt_type = watched.property("WidgetType")
        if event.type() == QEvent.Type.Enter:
            if wgt_type in ("btn", "slider"):
                sound_manager.play(wgt_type, "hover")
                return False
        elif isinstance(event, QMouseEvent) and event.type() == QEvent.Type.MouseButtonRelease:
            if isinstance(watched, QWidget) and event.button() == Qt.MouseButton.LeftButton:
                if watched.rect().contains(event.position().toPoint()):
                    if wgt_type == "btn":
                        sound_manager.play(wgt_type, "click")
                        return False
        return False


class WarningDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Warning")
        self.setFixedSize(300, 120)

        self.warning_label = QLabel("Effect not selected.", self)
        self.warning_label.setGeometry(20, 20, 260, 30)

        self.ok_button = QPushButton("OK", self)
        self.ok_button.setGeometry(210, 80, 80, 30)
        self.ok_button.clicked.connect(self.accept)


class EffectSaveDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Effect save settings")
        self.setFixedSize(300, 260)

        self.duration_label = QLabel("Duration: 3s", self)
        self.duration_label.setObjectName("duration")
        self.duration_label.setGeometry(75, 30, 150, 30)

        self.duration_slider = QSlider(self)
        self.duration_slider.setGeometry(30, 60, 240, 30)
        self.duration_slider.setOrientation(Qt.Orientation.Horizontal)
        self.duration_slider.setRange(1, 10)
        self.duration_slider.setValue(3)
        self.duration_slider.valueChanged.connect(lambda value: self.duration_label.setText(f"Duration: {value}s"))

        self.format_label = QLabel("Video format: mp4", self)
        self.format_label.setObjectName("video_format")
        self.format_label.setGeometry(55, 130, 190, 30)

        self.save_button = QPushButton("Save", self)
        self.save_button.setGeometry(120, 220, 80, 30)

        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.setGeometry(210, 220, 80, 30)
        self.cancel_button.clicked.connect(self.reject)


class SuccessfullySavedDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Success")
        self.setFixedSize(440, 140)

        self.success_label = QLabel("Effect saved successfully to specified directory: ", self)
        self.success_label.setGeometry(20, 20, 420, 60)
        self.success_label.setObjectName("success")
        self.success_label.setWordWrap(True)

        self.ok_button = QPushButton("OK", self)
        self.ok_button.setGeometry(350, 100, 80, 30)
        self.ok_button.clicked.connect(self.accept)


class SavingCanceledDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Saving canceled")
        self.setFixedSize(350, 140)

        self.success_label = QLabel("Saving the effect has been canceled.", self)
        self.success_label.setGeometry(20, 20, 350, 60)
        self.success_label.setWordWrap(True)

        self.ok_button = QPushButton("OK", self)
        self.ok_button.setGeometry(260, 100, 80, 30)
        self.ok_button.clicked.connect(self.accept)


class ProgressDialog(QDialog):
    cancel_saving_signal = Signal()

    def __init__(self):
        super().__init__()
        self.setFixedSize(400, 130)
        self.user_canceled = True

        self.label = QLabel("Saving effect in progress...", self)
        self.label.setGeometry(20, 0, 360, 30)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(15, 40, 370, 40)

        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.setGeometry(310, 90, 80, 30)
        self.cancel_button.clicked.connect(self.reject)

    def reject(self):
        if self.user_canceled:
            self.user_canceled = False
            self.cancel_saving_signal.emit()
        super().reject()

    def closeEvent(self, event):
        """Emits the cancellation signal when the dialog is closed."""
        if self.user_canceled:
            self.user_canceled = False
            self.cancel_saving_signal.emit()
        event.accept()


class ExportDialogs(QObject):
    export_request_signal = Signal(str, int)

    def __init__(self):
        super().__init__()
        self.warning = WarningDialog()
        self.effect_save = EffectSaveDialog()
        self.progress_dialog = ProgressDialog()
        self.success_dialog = SuccessfullySavedDialog()
        self.cancel_dialog = SavingCanceledDialog()
        self.sound_filter = SoundFilter()
        self.setup_styles()
        self.setup_sounds()

        self.file_path = ""

        self.effect_save.save_button.clicked.connect(lambda checked: self.open_file_save_dialog())

    def setup_styles(self):
        with open(STYLE_QSS_PATH, "r", encoding="utf-8") as file:
            style = file.read()
        self.warning.setStyleSheet(style)
        self.effect_save.setStyleSheet(style)
        self.progress_dialog.setStyleSheet(style)
        self.success_dialog.setStyleSheet(style)
        self.cancel_dialog.setStyleSheet(style)

    def setup_sounds(self):
        buttons = (self.warning.ok_button, self.effect_save.save_button, self.effect_save.cancel_button,
                   self.success_dialog.ok_button, self.cancel_dialog.ok_button, self.progress_dialog.cancel_button)
        for button in buttons:
            self.install_sound(button, "btn")
        self.install_sound(self.effect_save.duration_slider, "slider")

    def install_sound(self, widget, widget_type):
        widget.setProperty("WidgetType", widget_type)
        widget.installEventFilter(self.sound_filter)

    def launch_export_ui(self):
        if cfg.current_effect == "NO MODE":
            sound_manager.play("export", "info")
            self.warning.exec()
        else:
            self.effect_save.exec()

    def update_progress_bar_value(self, value):
        self.progress_dialog.progress_bar.setValue(value)

    def close_progress_dialog(self):
        self.progress_dialog.user_canceled = False
        self.progress_dialog.accept()

    def open_success_dialog(self):
        self.success_dialog.success_label.setText(f"Effect saved successfully to specified directory: {self.file_path}")
        self.success_dialog.exec()

    def open_file_save_dialog(self):
        default_dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DesktopLocation)

        file_path, _ = QFileDialog.getSaveFileName(
            None,
            "Save video",
            default_dir,
            "MP4 Files (*.mp4)"
        )
        if not file_path:
            return

        if not file_path.endswith(".mp4"):
            file_path += ".mp4"
        self.file_path = file_path

        self.start_export()

    def start_export(self):
        duration = self.effect_save.duration_slider.value()
        total_frames = cfg.current_values[cfg.current_effect]["SPEED"] * duration

        self.effect_save.accept()

        self.progress_dialog.user_canceled = True
        self.progress_dialog.progress_bar.setRange(0, total_frames)
        self.progress_dialog.progress_bar.setValue(0)
        self.progress_dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.progress_dialog.show()

        self.export_request_signal.emit(self.file_path, duration)
