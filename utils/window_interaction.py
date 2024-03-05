import win32api
import win32gui
import win32con


def _active_window(title: str) -> bool:
    hwnd = win32gui.FindWindow(None, title)
    if hwnd:
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)  # restore window if minimized
        win32gui.SetForegroundWindow(hwnd)  # bring to front
        return True
    return False


def _minimize_window(title: str) -> bool:
    hwnd = win32gui.FindWindow(None, title)
    if hwnd:
        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
        return True
    return False


def _get_window_coordinates(title: str):
    hwnd = win32gui.FindWindow(None, title)
    if hwnd:
        rect = win32gui.GetWindowRect(hwnd)
        x, y, w, h = rect
        return x, y, w, h
    return None


def point_cursor_to_chat() -> bool:
    discord_name = '#general | Bot Generator Server - Discord'

    if not _active_window(discord_name):
        return False

    return True
