from ok import Logger
from src.tasks.FarmRelicTask import FarmRelicTask

logger = Logger.get_logger(__name__)


class DailyTask(FarmRelicTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "Auto Daily Task"
        self.description = "Farm Relic and Finish Daily Task"
        self.add_exit_after_config()
        self.add_first_run_alert(
            "If this task is executed while the game is in the background, your mouse will be locked temperately while the game character is moving due to game and system limitations.")


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
        self.log_info(f'Daily Task Completed!', notify=True)
        return


