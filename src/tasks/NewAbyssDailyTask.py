from qfluentwidgets import FluentIcon

from ok import Logger
from src.tasks.FarmNewAbyssTask import FarmNewAbyssTask
from src.tasks.FarmRelicTask import FarmRelicTask

logger = Logger.get_logger(__name__)


class NewAbyssDailyTask(FarmNewAbyssTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "日常一条龙 - 刷幽境危战"
        self.description = "刷困难幽境危战, 需要先手动通关一次所选战场困难难度"
        self.icon = FluentIcon.CAR
        self.show_create_shortcut = True
        self.add_exit_after_config()
        self.add_first_run_alert(
            "If this task is executed while the game is in the background, your mouse will be locked temperately while the game character is moving due to game and system limitations.")

    def run(self):
        self.info_set('current task', 'wait login')
        self.wait_until(self.login, time_out=180, raise_if_not_found=True)

        self.ensure_main()

        self.go()
        self.loop_battle()

        self.teleport_to_fontaine_catherine()

        if not self.config.get('Use Original Resin'):
            self.go_and_craft()

        self.claim_daily_book()
        self.go_to_catherine()
        self.claim_rewards()
        self.claim_expedition()

        self.claim_mail()
        self.claim_battle_pass()

        self.teleport_and_catch_butterfly()

        self.log_info(f'Daily Task Completed!', notify=True)
        return
