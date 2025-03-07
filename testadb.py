import ctypes
import time

def disable_mouse():
    # Disable mouse input
    print('disable_mouse')
    ctypes.windll.user32.BlockInput(True)

def enable_mouse():
    # Enable mouse input
    print('enable_mouse')
    ctypes.windll.user32.BlockInput(False)

time.sleep(2)
disable_mouse()
time.sleep(1)
enable_mouse()