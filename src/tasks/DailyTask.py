from ok import Logger
from src.tasks.FarmRelicTask import FarmRelicTask

logger = Logger.get_logger(__name__)


class DailyTask(FarmRelicTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "Auto Daily Task"
        self.description = "Farm Relic and Finish Daily Task"


    def run(self):
        self.claim_mail()
        self.claim_battle_pass()
        return
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
        return

    def claim_mail(self):
        self.back()
        self.wait_feature('esc_achievements', settle_time=1)
        if mail := self.find_red_dot('box_mail'):
            self.click(mail)
            self.wait_click_feature('claim_all', box='bottom_left', settle_time=1)
        self.ensure_main()

    def claim_battle_pass(self):
        if self.find_red_dot('box_top_right_battle_pass'):
            self.send_key('f4')
            self.wait_feature('top_right_close_btn', settle_time=1)
            if dots := self.find_red_dot('battle_pass_quests'):
                self.click(dots, after_sleep=1)
                self.click_box('battle_pass_claim_all', after_sleep=1)
                self.ensure_main()


    def battle(self):
        for i in range(4):
            self.send_key(str(i+1))
            self.sleep(0.3)
            self.send_key('e')
            self.sleep(1.5)
