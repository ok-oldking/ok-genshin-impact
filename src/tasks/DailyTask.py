import re
import time

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
        for i in range(10):
            new_x = self.width_of_screen(0.51)
            new_y = self.width_of_screen(0.5)
            win32api.SetCursorPos((new_x, new_y))
            time.sleep(0.2)

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
        while True:

            self.sleep(0.01)
        self.sleep(5)

    def run(self):
        self.sleep(1)
        # self.walk()
        self.click_relative(0.15,0.31)
        return

    def battle(self):
        for i in range(4):
            self.send_key(str(i+1))
            self.sleep(0.3)
            self.send_key('e')
            self.sleep(1.5)




def sort_characters_by_priority(chars, priority):
    """
    Sorts a list of character objects based on their 'char_name' attribute,
    according to a priority list.

    Characters whose 'char_name' attribute appears in the priority list are
    placed at the front, sorted by their order within the priority list.
    Characters not in the priority list retain their original order.

    Args:
        chars: A list of character objects, where each object has a 'char_name' attribute (string).
        priority: A list of character names (strings) representing the priority order.

    Returns:
        A new list of character objects, sorted according to the priority.  The
        original `chars` list is not modified.
    """

    priority_map = {name: index for index, name in enumerate(priority)}
    sorted_chars = []

    for i, the_char in enumerate(chars):  # Use enumerate to get the original index
        char_name = the_char.name
        if char_name in priority_map:
            sorted_chars.append((priority_map[char_name], i, the_char))  # (priority_index, original_index, char_object)
        else:
            sorted_chars.append((len(priority), i, the_char))  # (lowest_priority, original_index, char_object)

    sorted_chars.sort()  # Sort the list of tuples

    return [char_object for _, _, char_object in sorted_chars]  # Extract the character objects
