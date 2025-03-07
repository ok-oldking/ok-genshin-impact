import time

from qfluentwidgets import FluentIcon

from ok import FindFeature, Logger
from ok import TriggerTask
from src.tasks.BaseGiTask import BaseGiTask, white_color

logger = Logger.get_logger(__name__)


class AutoPickTask(TriggerTask, BaseGiTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "Auto Pick"
        self.description = "Auto Pick Flowers in Game World"
        self.icon = FluentIcon.SHOPPING_CART
        self.last_box_name = None
        self.last_pick_time = 0

    def trigger(self):
        # self.logger.debug("trigger task2")
        if self.in_world_or_dungeon():
            while button_f := self.find_one("f", vertical_variance=0.1):
                percent = self.calculate_color_percentage(white_color, button_f)
                if percent < 0.8:
                    self.log_debug(f'wait for f animation {percent}')
                    self.next_frame()
                    continue
                dialogs = self.find_dialogs(button_f)
                white_list = None
                if dialogs:
                    to_find = dialogs[0]
                    white_list = self.find_one(pick_white_list, box=to_find.copy(x_offset=-to_find.width * 0.15,
                                                                           width_offset=to_find.width * 0.3,
                                                                           y_offset=-to_find.height * 0.15,
                                                                           height_offset=to_find.height * 0.3))
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
                if not dialogs:
                    self.logger.info(f"found a f {percent} {white_list} {dialogs}")
                    self.screenshot('pick')
                    self.send_key("f")
                    self.sleep(0.005)
                    continue
                elif self.debug:
                    # logger.debug(f'draw dialogs {dialogs} {white_list}')
                    self.draw_boxes(boxes=dialogs)
                break

    def find_dialogs(self, button_f):
        return self.find_choices(button_f, horizontal=button_f.width * 2.35, limit=1,
                               threshold=0.3)

pick_white_list = ['pick_w_chest', 'pick_w_m_glass', 'pick_w_butterfly']

