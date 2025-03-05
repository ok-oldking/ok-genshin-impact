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

    def in_dialog(self):
        return self.find_one('top_left_chat_hide', horizontal_variance=0.02)


    def trigger(self):
        # Check if the scene is an instance of DialogPlayingScene or BlackDialogScene
        # self.logger.debug("trigger task2")
        entered = self.in_dialog()
        while entered:
            f = self.find_one("f", box=self.box_of_screen(0.63, 0.45, 0.65,0.77))
            if f:
                dots = self.find_feature("chat_3_dots", box=self.box_of_screen(0.66,0.45,0.69,0.77))
                if dots:
                    if abs(dots[0].center()[1] - f.center()[1]) > f.height/2:
                        self.log_debug('found other than dialogs skip')
                    else:
                        # self.click(dots[-1])
                        self.send_key('f')
            elif play:=self.find_one('top_left_chat_play', horizontal_variance=0.02):
                self.click(play)
            elif self.in_world_or_dungeon():
                self.log_info(f'Auto Quest Dialog Completed!', notify=not self.hwnd.visible)
                break
            elif self.in_dialog():
                self.send_key('space')
            # else:
            #     self.click_relative(0.96,0.05)
            self.sleep(1)




