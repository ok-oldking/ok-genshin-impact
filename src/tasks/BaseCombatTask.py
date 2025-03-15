import re
import time
from typing import List

import numpy as np

from ok import BaseTask, find_boxes_within_boundary, find_boxes_by_name, Box, calculate_color_percentage, og
from ok import Logger
from src.tasks.BaseGiTask import BaseGiTask, white_color
from ok import find_color_rectangles, get_mask_in_color_range, is_pure_black

logger = Logger.get_logger(__name__)


class BaseCombatTask(BaseGiTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_config.update({
            'Combat Sequence': None,
        })
        self._in_combat = False
        self.action_index = 0
        self.last_action_start = 0
        self.config_type['Combat Sequence'] = {'type': "global"}
        self.combat_config = self.get_global_config('Auto Combat Config')

    def check_health_bar(self):
        if self._in_combat:
            min_height = self.height_of_screen(12 / 2160)
            max_height = min_height * 3
            min_width = self.width_of_screen(12 / 3840)
        else:
            min_height = self.height_of_screen(12 / 2160)
            max_height = min_height * 3
            min_width = self.width_of_screen(100 / 3840)

        boxes = find_color_rectangles(self.frame, enemy_health_bar_red_color, min_width, min_height,
                                      max_height=max_height)

        if len(boxes) > 0:
            if self.debug:
                self.draw_boxes('enemy_health_bar_red', boxes, color='blue')
            return True

        return False

    def auto_combat(self, time_out=120, end_check=None):
        start = time.time()
        if start - self.last_action_start > 15:
            self.log_info(f'reset auto combat sequence')
            self.last_action_start = time.time()
            self.action_index = 0
        combat_str = self.combat_config.get('Combat Sequence').strip()
        while True:
            elapsed = time.time() - start
            if elapsed > time_out:
                raise RuntimeError('Auto Combat timed out after {} seconds!'.format(time_out))
            if elapsed > 3 and end_check is not None and self.in_world_or_domain() and end_check():
                if self.debug:
                    self.screenshot('combat_end')
                self.info_incr('Combat Count')
                return True
            action = combat_str[self.action_index % len(combat_str)]
            if to_switch := safe_parse_int(action):  # switch command
                current_char = self.get_current_char()
                if current_char != to_switch:
                    self.send_key(to_switch)
                    self.combat_sleep(0.2)
                    continue
            elif action.upper() == 'E' or action.upper() == 'L':
                cd = self.get_cd('box_e')
                if cd < 1:
                    self.sleep(cd + 0.1)
                    if action.upper() == 'E':
                        self.send_key('e')
                    else:
                        self.send_key('e', down_time=0.8)
                    self.combat_sleep()
            elif action.upper() == 'Q':
                cd = self.get_cd('box_q')
                if cd == 0:
                    white_percent = self.calculate_color_percentage(q_white_color, 'box_q')
                    self.log_debug('q_white_color: {}'.format(white_percent))
                    if white_percent > 0.05:
                        self.send_key('q')
                        self.sleep(1.5)
                        self.wait_until(self.in_world_or_domain, time_out=5)
            elif action.upper() == 'A':
                self.click_relative(0.5, 0.5)
                self.combat_sleep()
            else:
                raise Exception('Unknown action: {}'.format(action))
            self.action_index += 1

    def get_cd(self, box_name):
        cd_text = self.ocr(box=box_name, match=cd_re)
        if not cd_text:
            return 0
        else:
            return float(cd_text[0].name)

    def combat_sleep(self, to_sleep=0):
        if to_sleep == 0:
            if self.hwnd.is_foreground():
                to_sleep = 0.2
            else:
                to_sleep = 0.2
        self.sleep(to_sleep)

    def get_current_char(self):
        char1 = self.find_one('1')
        char2 = self.find_one('2')
        char3 = self.find_one('3')
        char4 = self.find_one('4')
        chars = [char1, char2, char3, char4]
        if sum(1 for item in chars if item is None) > 1:
            raise Exception('Can only combat with a team of 4!')
        lowest_char = None
        lowest_conf = 1
        for i in range(len(chars)):
            char = chars[i]
            if not char:
                lowest_char = char
                break
            white_percent = self.calculate_color_percentage(white_color, char)
            if white_percent < lowest_conf:
                lowest_conf = white_percent
                lowest_char = i + 1
        self.log_debug(f'current char: {lowest_char} {lowest_conf}')
        return lowest_char

    def domain_combat_end(self):
        return self.ocr(box='box_dungeon_end_countdown', match=count_down_re)


def safe_parse_int(value, default=0):
    """
    Safely parses an integer from a string or other value.

    Args:
      value: The value to parse. Can be a string, integer, float, etc.
      default: The value to return if parsing fails.  Defaults to 0.

    Returns:
      The integer representation of the value if parsing is successful,
      otherwise the default value.
    """
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


count_down_re = re.compile(r"[1-9]\d{2}")

cd_re = re.compile(r"^(?:[0-9]|[1-9][0-9])\.[0-9]$")

q_white_color = {
    'r': (210, 255),  # Red range
    'g': (210, 255),  # Green range
    'b': (210, 255)  # Blue range
}

enemy_health_bar_red_color = {
    'r': (245, 255),  # Red range
    'g': (80, 100),  # Green range
    'b': (80, 100)  # Blue range
}
