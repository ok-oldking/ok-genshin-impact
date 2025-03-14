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

    def trigger(self):
        return self.login()
