import os
import stat
import sys

APP_NAME = "AC"
PY_SCRIPT = "tdr.py"
DESKTOP_FILE = f"{APP_NAME}.desktop"
LAUNCHER = f"{APP_NAME}_launcher.sh"

def find_venv_python():
    # Use the Python currently running this script.
    return sys.executable

def create_launcher(venv_python, script_path):
    launcher_path = os.path.expanduser(f"~/.local/bin/{LAUNCHER}")
    os.makedirs(os.path.dirname(launcher_path), exist_ok=True)

    content = f"""#!/bin/bash
"{venv_python}" "{script_path}"
"""

    with open(launcher_path, "w") as f:
        f.write(content)

    st = os.stat(launcher_path)
    os.chmod(launcher_path, st.st_mode | stat.S_IEXEC)

    return launcher_path

def create_desktop_entry(launcher_path):
    desktop_path = os.path.expanduser(f"~/.local/share/applications/{DESKTOP_FILE}")
    os.makedirs(os.path.dirname(desktop_path), exist_ok=True)

    content = f"""[Desktop Entry]
Type=Application
Name={APP_NAME}
Exec={launcher_path}
Terminal=false
Categories=Utility;
"""

    with open(desktop_path, "w") as f:
        f.write(content)

    return desktop_path

def main():
    print("Installing app...")

    script_path = os.path.abspath(PY_SCRIPT)
    if not os.path.exists(script_path):
        print(f"Error: {PY_SCRIPT} not found in this directory.")
        return

    venv_python = find_venv_python()
    print(f"Using Python interpreter: {venv_python}")

    launcher = create_launcher(venv_python, script_path)
    print(f"Created launcher: {launcher}")

    desktop = create_desktop_entry(launcher)
    print(f"Created desktop entry: {desktop}")

    print("\nInstallation complete!")
    print("Refresh your app menu if it doesn't appear immediately.")
    print("You can now search for the app named:", APP_NAME)

if __name__ == "__main__":
    main()
