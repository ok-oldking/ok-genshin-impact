import time

from qfluentwidgets import FluentIcon

from ok import FindFeature, Logger
from ok import TriggerTask
from src.tasks.BaseGiTask import BaseGiTask

logger = Logger.get_logger(__name__)


class AutoDialogTask(TriggerTask, BaseGiTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "Auto Dialog"
        self.description = "Auto Dialog in Quests"
        self.icon = FluentIcon.CHAT
        self.trigger_interval = 0.5
        self.default_config = {
            '_enabled': True,
            "Speed up Dialog Using Space Key": True,
            "Send Notification when Dialog Completed": True,
        }

    def in_dialog(self):
        return self.find_one('top_left_chat_hide', horizontal_variance=0.02)


    def trigger(self):
        entered = self.in_dialog()
        start_time = time.time()
        last_in_dialog_time = start_time
        while entered:
            f = self.find_one("f", box=self.box_of_screen(0.63, 0.45, 0.65,0.77))
            if f:
                dots = self.find_feature("chat_3_dots", box=self.box_of_screen(0.66,0.45,0.69,0.77))
                if dots:
                    found_near = False
                    for dot in dots:
                        if abs(dot.center()[1] - f.center()[1]) < f.height/2:
                            found_near = True
                            break
                    if not found_near:
                        if time.time() - start_time > 10:
                            self.log_info(f'Auto Quest Dialog Need to Choose Manually!', notify=not self.hwnd.visible)
                            return
                    else:
                        if self.debug:
                            self.screenshot('dialog')
                        last_in_dialog_time = time.time()
                        self.send_key('f')
            elif play:=self.find_one('top_left_chat_play', horizontal_variance=0.02):
                self.click(play)
            elif self.in_world_or_domain():
                self.log_info(f'Auto Quest Dialog Completed!', notify=not self.hwnd.visible and self.config.get("Send Notification when Dialog Completed"))
                # self.executor.interaction.deactivate()
                return
            elif self.find_one('dialog_black_screen'):
                last_in_dialog_time = time.time()
                self.send_key('space')
            elif self.in_dialog():
                last_in_dialog_time = time.time()
                if self.config.get('Speed up Dialog Using Space Key', False):
                    self.send_key('space')
            elif time.time() - last_in_dialog_time > 10:
                self.log_info(f'Auto Quest Dialog Need to Choose Manually!',
                              notify=not self.hwnd.visible)
                return
            self.sleep(2)




