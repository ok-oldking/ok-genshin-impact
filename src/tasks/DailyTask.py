from qfluentwidgets import FluentIcon

from ok import Logger
from src.tasks.FarmRelicTask import FarmRelicTask

logger = Logger.get_logger(__name__)


class DailyTask(FarmRelicTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "Auto Daily Task"
        self.description = "Farm Relic and Finish Daily Task"
        self.icon = FluentIcon.CAR
        self.show_create_shortcut = True
        self.add_exit_after_config()
        self.add_first_run_alert(
            "If this task is executed while the game is in the background, your mouse will be locked temperately while the game character is moving due to game and system limitations.")

    def teleport_and_catch_butterfly(self):
        self.send_key('m', after_sleep=1)
        teleport = self.find_one('map_option_waypoint', box=self.box_of_screen(0.04, 0.41, 0.17, 0.60))
        self.click_box(teleport, after_sleep=1)
        self.wait_confirm_dialog(btn='btn_teleport', box='bottom_right')
        self.wait_world(settle_time=1)
        self.turn_angle(140, middle_click=False)
        self.catch_butter_fly(time_out=1.4, catch_time=0.8)

        # sea butterfly
        self.send_key('m', after_sleep=1)
        self.click_relative(0.02, 0.59, after_sleep=1)

        teleport = self.find_one('map_option_waypoint', box=self.box_of_screen(0.72, 0.07, 0.93, 0.26))
        self.click_box(teleport, after_sleep=1)
        self.wait_confirm_dialog(btn='btn_teleport', box='bottom_right')
        self.wait_world(settle_time=1)
        self.turn_angle(92, 190, False)
        self.catch_butter_fly(6, 1)

    def run(self):
        self.info_set('current task', 'wait login')
        self.wait_until(self.login, time_out=180, raise_if_not_found=True)

        self.ensure_main()

        if self.teleport_into_domain():
            self.farm_relic_til_no_stamina()

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


