import re
import time

import mouse
import win32api
import win32con
import win32gui

from ok import Logger, find_boxes_by_name, find_boxes_within_boundary
from src.tasks.BaseGiTask import BaseGiTask

logger = Logger.get_logger(__name__)


class DailyTask(BaseGiTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "test"
        self.description = "test"
        self.default_config.update({
            '公共区': True,
            '购买免费礼包': True,
            '自动刷体力': True,
            '竞技场': True,
            '兵棋推演': True,
            '班组': True,
            '尘烟': True,
            '领任务': True,
            '大月卡': True,
            '邮件': True,
        })

    def mouse_move_test(self):
        self.executor.interaction.block_input()
        self.executor.interaction.activate()
        for i in range(10):
            # self.executor.interaction.move_mouse_by(100)

            move_mouse_relative(100,0)
            # win32api.SetCursorPos((new_x, new_y))
            time.sleep(0.1)
        self.executor.interaction.deactivate()
        self.executor.interaction.unblock_input()

    def alt_click(self, x, y):
        self.send_key_down('alt')
        self.sleep(0.02)
        self.click_relative(x, y, move=True)
        # self.sleep(1)
        self.send_key_up('alt')

    def mijing(self):
        self.send_key_down('f1')
        self.sleep(2)
        self.alt_click(0.16,0.41)

    def scroll_book(self):
        self.scroll_relative(0.5, 0.5, -1)

    def walk(self):
        self.send_key_down('w')
        to_walk = 5
        self.executor.interaction.block_input()
        self.sleep(5)
        self.executor.interaction.deactivate()
        self.executor.interaction.unblock_input()


        # while True:
        #
        #     self.sleep(0.01)


    def run(self):
        self.sleep(2)
        # self.walk()
        # self.send_key('f')
        # self.click_relative(0.15,0.31)
        # for i in range(3):
        #     self.log_debug('wheel')
        # mouse.wheel(1)
        self.mouse_move_test()
        # self.scroll_relative(0.5, 0.5, 1)

        self.sleep(2)


        # self.swipe_relative(0.45, 0.71, 0.45, 0.31, duration=1)

        return

    def battle(self):
        for i in range(4):
            self.send_key(str(i+1))
            self.sleep(0.3)
            self.send_key('e')
            self.sleep(1.5)


import ctypes
import time

# Define constants from Windows API
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_ABSOLUTE = 0x8000
SCREEN_WIDTH = ctypes.windll.user32.GetSystemMetrics(0)
SCREEN_HEIGHT = ctypes.windll.user32.GetSystemMetrics(1)

# Define the MOUSEINPUT structure
class MOUSEINPUT(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                 ("dy", ctypes.c_long),
                 ("mouseData", ctypes.c_ulong),
                 ("dwFlags", ctypes.c_ulong),
                 ("time", ctypes.c_ulong),
                 ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]

# Define the INPUT structure
class INPUT(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                 ("mi", MOUSEINPUT)]

# Define the SendInput function
SendInput = ctypes.windll.user32.SendInput
SendInput.argtypes = [ctypes.c_uint, ctypes.POINTER(INPUT), ctypes.c_int]
SendInput.restype = ctypes.c_uint


def move_mouse_relative(dx, dy):
    """
    Moves the mouse cursor relative to its current position using user32.SendInput.

    Args:
        dx: The number of pixels to move the mouse horizontally (positive for right, negative for left).
        dy: The number of pixels to move the mouse vertically (positive for down, negative for up).
    """

    mi = MOUSEINPUT(dx, dy, 0, MOUSEEVENTF_MOVE, 0, None)
    i = INPUT(0, mi)  # type=0 indicates a mouse event
    SendInput(1, ctypes.pointer(i), ctypes.sizeof(INPUT))


def move_mouse_absolute(x, y):
    """Moves the mouse cursor to an absolute screen position using user32.SendInput.
    Takes normalized coordinates in the range [0, 65535] for x and y.
    """
    mi = MOUSEINPUT(int(x * (65535.0 / SCREEN_WIDTH)), int(y * (65535.0 / SCREEN_HEIGHT)), 0, MOUSEEVENTF_ABSOLUTE | MOUSEEVENTF_MOVE, 0, None)
    i = INPUT(0, mi)
    SendInput(1, ctypes.pointer(i), ctypes.sizeof(INPUT))