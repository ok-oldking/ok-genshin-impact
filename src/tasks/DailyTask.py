import re
import time
from asyncio import timeout

import win32api
import win32con
import win32gui

from ok import Logger, find_boxes_by_name, find_boxes_within_boundary
from src.tasks.BaseGiTask import BaseGiTask
from src.tasks.FarmRelicTask import FarmRelicTask

logger = Logger.get_logger(__name__)


class DailyTask(FarmRelicTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "Auto Daily Task"
        self.description = "Farm Relic and Finish Daily Task"


    def run(self):
        self.info_set('current task', 'wait login')
        self.wait_until(self.login, time_out=90, raise_if_not_found=True)

        self.ensure_main()

        self.teleport_into_domain()

        self.farm_relic_til_no_stamina()

        self.teleport_to_fontaine_catherine()
        self.go_and_craft()

        self.teleport_to_fontaine_catherine()
        self.go_to_catherine()
        self.claim_rewards()

        return

    def battle(self):
        for i in range(4):
            self.send_key(str(i+1))
            self.sleep(0.3)
            self.send_key('e')
            self.sleep(1.5)
