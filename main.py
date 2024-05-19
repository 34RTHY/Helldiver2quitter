import psutil
import ctypes
import time
import keyboard
from win32gui import IsWindow, IsWindowVisible, EnumWindows, SendMessageTimeout, SendMessage
from win32con import WM_CLOSE, SMTO_ABORTIFHUNG, PROCESS_TERMINATE
from win32api import OpenProcess, CloseHandle
from win32process import GetWindowThreadProcessId

def get_window_text(hwnd):
    length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
    if length > 0:
        buffer = ctypes.create_unicode_buffer(length + 1)
        ctypes.windll.user32.GetWindowTextW(hwnd, buffer, length + 1)
        return buffer.value
    return None

def get_hwnd_by_process_name_or_title(process_name, window_title_part):
    def enum_windows_callback(hwnd, result):
        if IsWindow(hwnd) and IsWindowVisible(hwnd):
            _, pid = GetWindowThreadProcessId(hwnd)
            try:
                process = psutil.Process(pid)
                window_title = get_window_text(hwnd)
                if window_title and window_title_part.lower() in window_title.lower():
                    result.append(hwnd)
                elif process.name().lower() == process_name.lower():
                    result.append(hwnd)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return True

    hwnds = []
    EnumWindows(enum_windows_callback, hwnds)
    return hwnds[0] if hwnds else None

def is_app_responsive(hwnd):
    if hwnd == 0:
        return False  # Window not found
    _, result = SendMessageTimeout(hwnd, 0, 0, 0, SMTO_ABORTIFHUNG, 1000)
    return result != 0

def close_game(hwnd):
    SendMessage(hwnd, WM_CLOSE, 0, 0)
    time.sleep(5)  # Wait a bit to see if the game closes gracefully
    return not IsWindow(hwnd)

def force_terminate_game(process_name):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'].lower() == process_name.lower():
            process = OpenProcess(PROCESS_TERMINATE, False, proc.info['pid'])
            ctypes.windll.kernel32.TerminateProcess(process, -1)
            CloseHandle(process)
            return

def attempt_to_close_game(process_name, window_title_part):
    hwnd = get_hwnd_by_process_name_or_title(process_name, window_title_part)
    if hwnd is None:
        print(f"Process '{process_name}' window or window containing '{window_title_part}' not found. Ensure the game is running.")
        return
    if not is_app_responsive(hwnd):
        print(f"{process_name} is not responding. Attempting to close...")
        if not close_game(hwnd):
            print("Failed to close gracefully, terminating now...")
            force_terminate_game(process_name)
        else:
            print("Game closed gracefully.")
    else:
        print(f"{process_name} is responding normally.")

if __name__ == "__main__":
    # Define your game process name here
    game_process_name = "helldivers2.exe"
    window_title_part = "HELLDIVERS™ 2"

    # Set up hotkey to listen for
    keyboard.add_hotkey('ctrl+del+backspace', attempt_to_close_game, args=[game_process_name, window_title_part])

    # Block the script so it doesn't exit
    print("Press 'ctrl+del+backspace' check and close the game.")
    keyboard.wait()
