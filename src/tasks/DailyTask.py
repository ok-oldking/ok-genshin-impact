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
        self.name = "Auto Daily Task"
        self.description = "Farm Relic and Finish Daily Task"
        self.default_config.update({

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

    def test_tree(self):
        start =time.time()
        self.executor.interaction.block_input()
        self.executor.interaction.activate()
        found_tree = False
        change_count = 0
        step = 100
        direction = 1
        abs_distance = self.width
        while time.time() - start < 20:
            d_start = time.time()
            trees = self.find_tree()
            self.draw_boxes(boxes=trees)
            if trees:
                distance = trees[0].center()[0] - self.width / 2
                abs_distance = abs(distance)
            else:
                distance = 1
            if trees:
                self.log_debug(f'trees: {trees[0]} cost:{time.time() - d_start} {trees[0].center()[0]} {self.width} distance:{distance}')

            new_direction = -1 if distance < 0 else 1

            if trees and direction != new_direction:
                direction = new_direction
                step = max(1, int(step / 2))
                change_count += 1
                self.log_debug(f'turning {direction} to {new_direction}')

            if change_count >= 4:
                self.log_info('turned a lot of trees, break')
                break
            if not trees and abs_distance <= self.width_of_screen(0.01):
                logger.info('found and lost tree break')
                break
            move_mouse_relative(direction * step, 0)
            self.next_frame()
        self.executor.interaction.deactivate()
        self.executor.interaction.unblock_input()
        self.sleep(2)
        trees = self.find_tree()
        self.draw_boxes(boxes=trees)
        if trees:
            self.log_info(f'trees: {trees[0]} {self.width/2 - trees[0].center()[0]}')
        else:
            self.log_info('no trees')



    def run(self):
        return self.log_info(f'Developing')
        self.sleep(2)

        self.test_tree()
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