import pygetwindow as gw
import time

def get_active_window_title():
    window = gw.getActiveWindow()
    if window is not None:
        return window.title
    return None

def normalize_vscode_title(title):
    parts = title.split(' - ')
    if len(parts) > 2 and "Visual Studio Code" in parts[-1]:
        filename = parts[0].lstrip('●').strip()  # Remove the symbol and leading/trailing whitespaces
        rest = ' - '.join(parts[1:])
        normalized_title = f"{filename} - {rest}"
        return normalized_title
    return title

active_window = get_active_window_title()
while True:
    prev = active_window
    active_window = get_active_window_title()
    if prev != active_window:
        if active_window is not None:
            print(f"Active Window: {active_window}")
    time.sleep(1)  # Add a small delay to reduce CPU usage
