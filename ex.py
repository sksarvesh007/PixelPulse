import pygetwindow as gw
import time

def get_active_window_title():
    window = gw.getActiveWindow()
    if window is not None:
        return window.title
    return None

active_window = get_active_window_title()
while True:
    prev = active_window
    active_window = get_active_window_title()
    if prev != active_window:
        print(active_window)
        if "Brave" in active_window:
            print(f"WEBSITE IS : {active_window.title}")
    time.sleep(1)