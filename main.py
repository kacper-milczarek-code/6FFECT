import sys
import os
import subprocess

# Set the working directory to the app root folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

venv_python = os.path.join(BASE_DIR, "venv", "Scripts", "python.exe")

# Verify virtual environment existence
if not os.path.exists(venv_python):
    print("\n[ERROR] Virtual environment (venv) was not found or is corrupted.")
    print("Please run 'setup.bat' to initialize the required environment and dependencies.")
    print("\nPress Enter to exit...")
    input()
    sys.exit(1)

# Relaunch within the virtual environment if currently running on system Python
if os.path.abspath(sys.executable).lower() != os.path.abspath(venv_python).lower():
    print("[INFO] Switching to virtual environment...")
    raise SystemExit(subprocess.call([venv_python] + sys.argv))

# Main entry point
if __name__ == "__main__":

    # Verify Python version compatibility
    MIN_VERSION = (3, 12)
    MAX_VERSION = (3, 14)
    CURRENT_VERSION = sys.version_info[:2]

    if CURRENT_VERSION < MIN_VERSION or CURRENT_VERSION > MAX_VERSION:
        current_str = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        tested_str = f"{MIN_VERSION[0]}.{MIN_VERSION[1]}-{MAX_VERSION[0]}.{MAX_VERSION[1]}"

        print("\n" + "=" * 65)
        print(f"[WARNING] Unverified Python version detected: {current_str}")
        print(f"This application was built and tested specifically on Python {tested_str}.")
        print("Running on a different version may cause unexpected bugs or crashes.")
        print("=" * 65)

        response = input("\nDo you still want to try launching the application? (Y/N): ").strip().lower()
        if response not in ('y', 'yes'):
            print("\nLaunch aborted by user.")
            sys.exit(0)
        print("\n[INFO] Proceeding with current environment...\n")

    # Initialize application UI
    try:
        from src.ui.main_window import app_init

        app_init()
    except Exception as e:
        print("\n[LAUNCH ERROR]:")
        import traceback

        traceback.print_exc()
        print("\nPress Enter to exit...")
        input()