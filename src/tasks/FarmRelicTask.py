import re
from typing import List

import numpy as np

from ok import BaseTask, find_boxes_within_boundary, find_boxes_by_name, Box, calculate_color_percentage, og
from ok import Logger
from src.tasks.BaseGiTask import BaseGiTask

logger = Logger.get_logger(__name__)


class BaseGiTask(BaseGiTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
