import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtNetwork import QLocalServer, QLocalSocket
from PySide6.QtGui import QFont, QFontDatabase

from src.ui.main_window import MainWindow
from src.paths import FONTS_DIR

APP_ID = "6FFECT_Unique_App_Single_Instance_Key"


def load_application_font(app: QApplication):
    """Load and apply the custom Orbitron font globally."""
    font_path = Path(FONTS_DIR) / "Orbitron-Bold.ttf"

    if font_path.exists():
        font_id = QFontDatabase.addApplicationFont(str(font_path))
        if font_id != -1:
            families = QFontDatabase.applicationFontFamilies(font_id)
            if families:
                # Use the exact family name registered by Qt from the font file metadata
                app_font = QFont(families[0])
                app.setFont(app_font)
            else:
                print("[WARNING] Font added, but no families found.")
        else:
            print("[ERROR] QFontDatabase rejected the font file (-1).")
    else:
        print(f"[ERROR] Font file not found at: {font_path}")


def main():
    app = QApplication(sys.argv)

    # Enforce single instance logic
    socket = QLocalSocket()
    socket.connectToServer(APP_ID)

    if socket.waitForConnected(500):
        sys.exit(0)

    server = QLocalServer()
    QLocalServer.removeServer(APP_ID)
    server.listen(APP_ID)

    # Load custom font right before creating the main window
    load_application_font(app)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()