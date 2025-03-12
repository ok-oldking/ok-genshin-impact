import time

from qfluentwidgets import FluentIcon

from ok import FindFeature, Logger
from ok import TriggerTask
from src.tasks.BaseGiTask import BaseGiTask

logger = Logger.get_logger(__name__)


class AutoLoginTask(TriggerTask, BaseGiTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "Auto Login"
        self.description = "Auto Login Game, Claim Monthly Card"
        self.default_config = {'_enabled': True}
        self.icon = FluentIcon.BACK_TO_WINDOW
        self.trigger_interval = 2
        self.logged_in = False

    def trigger(self):
        if self.logged_in:
            return
        if self.in_world_or_domain():
            self.log_info(f'in_world_or_domain set login to True')
            self.logged_in = True
            return
        if self.find_one('log_out'):
            self.log_info(f'login click center')
            self.click_relative(0.5, 0.5, after_sleep=3)
            return
        if self.find_one('monthly_card'):
            self.log_info(f'monthly_card click center')
            self.click_relative(0.5, 0.5, after_sleep=3)
            return
        if self.find_one('monthly_card_diamond'):
            self.log_info(f'monthly_card click center')
            self.click_relative(0.5, 0.6, after_sleep=3)
            return




