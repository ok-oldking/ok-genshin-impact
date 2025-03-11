import time

from qfluentwidgets import FluentIcon
from torch.ao.nn.quantized.functional import threshold

from ok import FindFeature, Logger, Box
from ok import TriggerTask
from src.tasks.BaseGiTask import BaseGiTask, white_color, pick_up_text_green_color, pick_up_text_blue_color

logger = Logger.get_logger(__name__)


class AutoPickTask(TriggerTask, BaseGiTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "Auto Pick"
        self.description = "Auto Pick Up in Game World"
        self.icon = FluentIcon.SHOPPING_CART
        self.default_config = {'_enabled': True}
        self.last_box_name = None
        self.last_pick_time = 0

    def trigger(self):
        # self.logger.debug("trigger task2")
        wait_start = 0
        if self.in_world_or_dungeon():
            while button_f := self.find_f():
                percent = self.calculate_color_percentage(white_color, button_f)
                if percent < 0.75:
                    self.next_frame()
                    continue
                text_zone = button_f.copy(x_offset=button_f.width * 4, width_offset=button_f.width * 2)
                if wait_start == 0 or time.time() - wait_start < 0.2:
                    white_percent = self.calculate_color_percentage(white_color, text_zone)
                    if white_percent < 0.05:
                        green_text_percent = self.calculate_color_percentage(pick_up_text_green_color, text_zone)
                        if green_text_percent < 0.05:
                            blue_text_percent = self.calculate_color_percentage(pick_up_text_blue_color, text_zone)
                            self.log_debug(f'white_percent={white_percent}, green_text_percent={green_text_percent}, blue_text_percent={blue_text_percent}')
                            if blue_text_percent < 0.05:
                                if wait_start == 0:
                                    wait_start = time.time()
                                if self.debug:
                                    self.log_debug(f'wait for text {white_percent}')
                                    # self.screenshot('wait_text')
                                self.next_frame()
                                continue
                icon_zone = button_f.copy(x_offset=button_f.width * 2.2, width_offset=button_f.width * 0.3, y_offset=-button_f.height * 0.15, height_offset=button_f.height * 0.3,
                              name='choice')

                dialogs = self.find_black_list_dialogs(icon_zone)
                if dialogs:
                    return
                white_list = self.find_one(pick_white_list, box=icon_zone)
                if white_list:
                    if white_list.name == 'pick_w_m_glass' and white_list.name == self.last_box_name and time.time() - self.last_pick_time < 60.0:
                        self.log_debug(f'same as last box skip {white_list}')
                        self.last_box_name = white_list.name
                    else:
                        self.log_debug(f'not skipping {white_list}')
                        dialogs = None
                        self.last_box_name = white_list.name
                        self.last_pick_time = time.time()
                else:
                    # self.log_debug(f'set last_box_name to None {white_list}')
                    self.last_box_name = None
                self.logger.info(f"found a f {percent} {white_list} {dialogs}")
                if self.debug:
                    self.screenshot('pick')
                self.send_key("f")
                self.sleep(0.02)
                return True



    def find_black_list_dialogs(self, box):
        return self.find_one(['chat_3_dots', 'pick_up_b_gear', 'pick_b_key'], box=box, threshold=0.7)

pick_white_list = ['pick_w_chest', 'pick_w_m_glass', 'pick_w_butterfly']

