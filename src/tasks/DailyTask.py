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
        self.executor.interaction.block_input()
        self.sleep(5)
        self.executor.interaction.deactivate()
        self.executor.interaction.unblock_input()


        # while True:
        #
        #     self.sleep(0.01)


    def run(self):
        self.sleep(1)
        # self.walk()
        self.send_key('f')
        # self.click_relative(0.15,0.31)
        return

    def battle(self):
        for i in range(4):
            self.send_key(str(i+1))
            self.sleep(0.3)
            self.send_key('e')
            self.sleep(1.5)


