import re
from typing import List

import numpy as np

from ok import BaseTask, find_boxes_within_boundary, find_boxes_by_name, Box, calculate_color_percentage, og
from ok import Logger
from src.tasks.BaseGiTask import BaseGiTask

logger = Logger.get_logger(__name__)


class FarmRelicTask(BaseGiTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "Farm Relic Task"
        self.description = "Farm Relic Task"
        self.default_config.update({
            'Relic Dungeon To Farm': 16
        })
        self.config_description = {
            'Relic Dungeon To Farm': 'Which Relic dungeon to Farm, in the F1 Book (1-17)',
        }

    def run(self):
        return self.walk_to_f()
