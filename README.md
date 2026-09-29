# 6FFECT

> Aby przejść do polskiej wersji, zobacz [README.pl.md](README.pl.md).

**6FFECT** is a desktop application designed to apply six custom, dynamic visual effects to any image. 
It features real-time parameter adjustment, allowing users to fine-tune image properties and effect behavior on the fly. 
The application is wrapped in a polished, sci-fi-inspired user interface, complete with custom graphics and interactive sound effects.

<p align="center">
  <img width="49%" alt="6FFECT Menu Overview" src="https://github.com/user-attachments/assets/ac532882-e6d4-48b0-a93c-25de32d0cffb" />
  <img width="49%" alt="6FFECT Interface Settings" src="https://github.com/user-attachments/assets/cf40b658-17ea-4e2d-8bc0-d2f9b7b38eb5" />
</p>

## ℹ️ About this project
6FFECT is my first project published on GitHub. I developed it to advance my Python programming skills — specifically focusing on Object-Oriented Programming (OOP), 
designing multi-module application architecture, managing multithreading, and adopting Git/GitHub workflows. The graphical user interface was built using the PySide6 framework. 
I developed the custom visual effects from scratch, utilizing NumPy for high-performance vectorized matrix operations, along with partial integration of the Pillow library.

## ✨ Key Features
- **6 Custom Effects**: FLIPPER, FADER, NUKER, PUZZLER, LINER, and RAINBOWER.
- **Real-Time Adjustments**: Tune image parameters (brightness, saturation, contrast) and effect behaviors instantly using simple sliders.
- **MP4 Video Export**: Render custom animations directly to MP4 with progress tracking.
- **Sci-Fi UI & Audio Feedback**: Sci-fi-styled Qt interface with interactive sound effects.
- **Drag & Drop**: Quick image loading with smart 16:9 / 9:16 aspect ratio fitting.

## ⚡ Visual effects
- **FLIPPER**: Divides the image into squares and rotates each square 90 degrees to the left.
- **FADER**: Applies irregular blob-like patches to the image by blacking out groups of pixels.
- **NUKER**: Brightens all image pixels causing glitch-art-style degradation due to RGB channel overflow.
- **PUZZLER**: Divides the image into squares and randomly reorders their positions.
- **LINER**: Blacks out or glitches image rows. When finished, it performs the reverse process of restoring the original rows.
- **RAINBOWER**: Divides the image into squares and tints each one with a random color channel.

## 🎬 Showcase Video
https://github.com/user-attachments/assets/d456d1c8-99a9-4497-ae2f-ad347bad72f0

## 🛠️ Created With
* **[Python](https://www.python.org/)** — Core programming language
* **[PySide6 / Qt](https://doc.qt.io/qtforpython-6/)** — GUI framework and user interface components
* **[NumPy](https://numpy.org/)** — High-performance vectorized matrix operations for custom VFX
* **[OpenCV](https://opencv.org/)** — Real-time computer vision and advanced image manipulation
* **[Pillow (PIL)](https://python-pillow.org/)** — Image loading, basic processing, and format handling
* **[Pytest](https://docs.pytest.org/)** — Automated unit and integration testing library


## 🧩 Project Structure
```text
6FFECT/
├── src/
│   ├── ui/
|   |   ├── effect_export_ui.py # Export UI dialogs
│   |   └── main_window.py      # Main PySide6 UI window, signal & event handling
|   |   └── style.qss           # QSS stylesheet for entire interface
│   ├── config.py               # Central application settings, default ranges & slider mappings
│   ├── effects.py              # Vectorized NumPy VFX algorithms & PIL image adjustments
│   ├── engine.py               # Background QThread engine for real-time frame rendering
│   ├── paths.py                # Path definitions for assets, icons, fonts, and stylesheets
│   ├── sound_manager.py        # Audio feedback controller with event throttling & mute toggle
│   ├── utils.py                # Format conversions (QImage <-> NumPy <-> PIL) & math helpers
│   └── video_exporter.py       # OpenCV MP4 video exporter
├── assets/                     # Sound effects, fonts, icons & example images
├── tests/                      # Simple unit tests for the effects and utils modules
├── main.py                     # Application entry point
├── setup.bat                   # Application setup
└── requirements.txt            # Python dependencies
```

## 📋 System Requirements
| Requirement | Details |
| :--- | :--- |
| **Operating System** | 💻 **Windows** (tested on Windows 10 / 11) |
| **Python Version** | 🐍 **Python 3.12 – 3.14** (recommended) |
| **Dependencies** | 📦 Managed via `requirements.txt` (PySide6, NumPy, OpenCV, Pillow, Pytest) |

> ⚠️ **Note:** **6FFECT** is currently designed and tested exclusively for **Windows**. Cross-platform support (macOS/Linux) is not available at this time.

## 📦 Installation Options
#### Option 1: Standalone Executable (Quickest)
1. Download `6FFECT.exe` from the **Assets** section below.
2. *(Optional)* Temporarily disable or adjust your antivirus if it blocks untrusted executables.
3. Run `6FFECT.exe` directly — no Python installation required!

#### Option 2: Setup Script (From Source)
1. Download and extract **Source code (zip)** from Assets.
2. Run `setup.bat` to automatically install dependencies and launch the app.

#### Option 3: Manual Command Line (Developer Mode)
1. Get the source code:
   * **Via Git:**
     ```bash
     git clone https://github.com/kacper-milczarek-code/6FFECT.git
     ```
   * **Or via ZIP:** Download and extract **Source code (zip)** from Assets below, then open the extracted folder in terminal.

2. Navigate to the project folder in your terminal / PowerShell:
   ```bash
   cd 6FFECT
   ```

3. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   ```
   ```bash
   .\venv\Scripts\Activate.ps1
   ```

4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Launch the application:
   ```bash
   python main.py
   ```

## 🔧 Troubleshooting Launch Issues
1. **Antivirus Delay:** If your antivirus flags the executable during the first launch, please wait a few seconds for it to finish scanning.
2. **Blocked File:** If the application is blocked or quarantined, locate it in your antivirus software settings and select *"Restore / Allow as an Exception"*.
3. **Manual Fallback:** If the standalone executable (Option 1) still fails to launch, please try the manual Python environment setup described in Option 2 or Option 3.

## 🧪 Running Tests
This project uses **pytest** for unit testing.
1. Ensure all dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```
2. Run tests from the project root directory:
   ```bash
   pytest
   ```
3. To view detailed output (verbose mode), run:
   ```bash
   pytest -v
   ```

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
