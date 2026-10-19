import os
import sys
import time
import ctypes
import subprocess
import threading
import tkinter as tk
from pathlib import Path

APP_TITLE_PART = "TypingPro"


def base_dir():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def start_typingpro():
    base = base_dir()
    if getattr(sys, "frozen", False):
        # Launcher is built as dist\TypingProLauncher.exe while the real
        # onedir application lives at dist\TypingPro\TypingPro.exe.
        target = base / "TypingPro" / "TypingPro.exe"
        if not target.exists():
            # Also support a future installer layout where both executables
            # may be placed in the same application directory.
            target = base / "TypingPro.exe"
        if not target.exists():
            raise FileNotFoundError(
                f"TypingPro.exe not found. Checked:\n"
                f"{base / 'TypingPro' / 'TypingPro.exe'}\n"
                f"{base / 'TypingPro.exe'}"
            )
        return subprocess.Popen([str(target)], cwd=str(target.parent))

    # Development launcher: use the same Python interpreter and main.py.
    target = base / "main.py"
    return subprocess.Popen([sys.executable, str(target)], cwd=str(base))


def typingpro_window_visible():
    if sys.platform != "win32":
        return False
    found = ctypes.c_bool(False)
    EnumWindows = ctypes.windll.user32.EnumWindows
    IsWindowVisible = ctypes.windll.user32.IsWindowVisible
    GetWindowTextLengthW = ctypes.windll.user32.GetWindowTextLengthW
    GetWindowTextW = ctypes.windll.user32.GetWindowTextW
    WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)

    def callback(hwnd, _):
        if not IsWindowVisible(hwnd):
            return True
        length = GetWindowTextLengthW(hwnd)
        if length <= 0:
            return True
        buf = ctypes.create_unicode_buffer(length + 1)
        GetWindowTextW(hwnd, buf, length + 1)
        title = buf.value
        if APP_TITLE_PART in title and "Launcher" not in title:
            found.value = True
            return False
        return True

    EnumWindows(WNDENUMPROC(callback), 0)
    return bool(found.value)


def watch(root, process):
    # Keep the launcher splash alive until the real TypingPro window exists.
    # If startup fails, do not leave a stuck splash forever.
    deadline = time.time() + 60
    while time.time() < deadline:
        if process.poll() is not None:
            break
        if typingpro_window_visible():
            time.sleep(0.12)
            break
        time.sleep(0.05)
    try:
        root.after(0, root.destroy)
    except Exception:
        pass


def main():
    root = tk.Tk()
    root.title("TypingPro Launcher")
    root.overrideredirect(True)
    root.configure(bg="#ffffff")
    width, height = 620, 340
    sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry(f"{width}x{height}+{(sw-width)//2}+{(sh-height)//2}")
    root.attributes("-topmost", True)

    frame = tk.Frame(root, bg="#ffffff", highlightthickness=1, highlightbackground="#dbe7f5")
    frame.pack(fill="both", expand=True)
    tk.Label(frame, text="TP", font=("Segoe UI", 42, "bold"), fg="#1769c2", bg="#ffffff").pack(pady=(48, 5))
    tk.Label(frame, text="TypingPro", font=("Segoe UI", 30, "bold"), fg="#172033", bg="#ffffff").pack()
    tk.Label(frame, text="PRACTICE  •  TYPE  •  IMPROVE", font=("Segoe UI", 10, "bold"), fg="#64748b", bg="#ffffff").pack(pady=(8, 30))
    tk.Label(frame, text="Starting TypingPro...", font=("Segoe UI", 10), fg="#475569", bg="#ffffff").pack()

    root.update_idletasks()
    process = start_typingpro()
    threading.Thread(target=watch, args=(root, process), daemon=True).start()
    root.mainloop()


if __name__ == "__main__":
    main()
