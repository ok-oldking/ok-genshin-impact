import time

from qfluentwidgets import FluentIcon

from ok import Logger
from ok import TriggerTask
from src.tasks.BaseCombatTask import BaseCombatTask
from src.tasks.BaseGiTask import BaseGiTask, white_color, pick_up_text_green_color, pick_up_text_blue_color

logger = Logger.get_logger(__name__)


class AutoCombatTask(TriggerTask, BaseCombatTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "Auto Combat"
        self.description = "Auto Combat in Game World or Domain"
        self.icon = FluentIcon.SHOPPING_CART
        self.default_config = {'_enabled': True}
        self.last_box_name = None
        self.last_pick_time = 0

    def run(self):
        if self.q_ended():
            self._in_combat = self.check_health_bar()
            if self._in_combat:
                self.auto_combat(end_check=self.end_combat_check)
            return True


    def end_combat_check(self):
        health_bar = self.check_health_bar()
        if not health_bar:
            self._in_combat = False
            return True
