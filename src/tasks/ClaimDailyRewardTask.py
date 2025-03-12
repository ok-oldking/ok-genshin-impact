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
        self.name = "Auto Daily Task"
        self.description = "Farm Relic and Finish Daily Task"
        self.default_config.update({

        })

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

    def run(self):
        return self.log_info(f'Developing', notify=True)
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
