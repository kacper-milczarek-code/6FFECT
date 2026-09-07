from PySide6.QtWidgets import QApplication, QDialog, QLabel, QPushButton, QSlider, QWidget
from PySide6.QtGui import QMouseEvent
from PySide6.QtCore import Qt, QEvent, QObject
import src.sound_manager as sm

app = QApplication()
sm.load_sounds()


def event_filter(self, watched: QWidget, event):
    """
    Triggers sound effects on widget hover and click release events.
    """
    wgt_type = watched.property("WidgetType")
    if event.type() == QEvent.Type.Enter:
        if wgt_type in ("btn", "slider"):
            sm.play(wgt_type, "hover")
            return False
    elif isinstance(event, QMouseEvent) and event.type() == QEvent.Type.MouseButtonRelease:
        if event.button() == Qt.MouseButton.LeftButton and watched.rect().contains(event.position().toPoint()):
            if wgt_type in ("btn", "example_img_btn"):
                sm.play(wgt_type, "click")
                return False
    return False


filter_obj = QObject()
filter_obj.eventFilter = event_filter.__get__(filter_obj, QObject)

# WARNING DIALOG
warning_dialog = QDialog()
warning_dialog.setWindowTitle("Warning")
warning_dialog.setFixedSize(300, 120)

warning_lbl = QLabel("Effect not selected", warning_dialog)
warning_lbl.setGeometry(20, 20, 260, 30)

btn_ok = QPushButton("OK", warning_dialog)
btn_ok.setGeometry(210, 80, 80, 30)
btn_ok.clicked.connect(warning_dialog.accept)

effect_save_dialog = QDialog()
effect_save_dialog.setWindowTitle("Effect save settings")
effect_save_dialog.setFixedSize(300, 260)

# EFFECT_SAVE_DIALOG
duration_lbl = QLabel("Duration: 3s", effect_save_dialog)
duration_lbl.setObjectName("duration")
duration_lbl.setGeometry(75, 30, 150, 30)

duration_sld = QSlider(effect_save_dialog)
duration_sld.setGeometry(30, 60, 240, 30)
duration_sld.setOrientation(Qt.Orientation.Horizontal)
duration_sld.setRange(1, 10)
duration_sld.setValue(3)
duration_sld.valueChanged.connect(lambda val: duration_lbl.setText(f"Duration: {val}s"))

video_format_lbl = QLabel("Video format: mp4", effect_save_dialog)
video_format_lbl.setObjectName("video_format")
video_format_lbl.setGeometry(55, 130, 190, 30)

btn_save = QPushButton("Save", effect_save_dialog)
btn_save.setGeometry(120, 220, 80, 30)
btn_save.clicked.connect(effect_save_dialog.accept)


btn_cancel = QPushButton("Cancel", effect_save_dialog)
btn_cancel.setGeometry(210, 220, 80, 30)
btn_cancel.clicked.connect(effect_save_dialog.reject)


with open("assets/styles/style.qss", "r", encoding="utf-8") as f:
    qss = f.read()
    effect_save_dialog.setStyleSheet(qss)
    warning_dialog.setStyleSheet(qss)

for widget in (btn_ok, btn_cancel, btn_save, duration_sld):
    if widget != duration_sld:
        widget.setProperty("WidgetType", "btn")
    else:
        widget.setProperty("WidgetType", "slider")
    widget.installEventFilter(filter_obj)

result = effect_save_dialog.exec()
result2 = warning_dialog.exec()
