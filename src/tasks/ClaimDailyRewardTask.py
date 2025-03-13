from ok import Logger, find_boxes_by_name, find_boxes_within_boundary
from src.tasks.BaseGiTask import BaseGiTask

logger = Logger.get_logger(__name__)


class ClaimDailyRewardTask(BaseGiTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "Claim Daily Reward"
        self.description = "Claim Daily Reward and Expedition"

    def run(self):
        # self.ensure_main()
        # self.teleport_to_fontaine_catherine()
        # self.sleep(1)
        # self.go_to_catherine()
        return

    def claim_rewards(self):
        pick_daily_reward = self.find_feature("chat_3_dots", box=self.find_choices_box)
        if not pick_daily_reward:
            raise RuntimeError("No daily reward found")


    def teleport_to_fontaine_catherine(self):
        self.send_key('m')
        self.wait_feature('map_close', raise_if_not_found=True, settle_time=1)
        self.scroll_relative(0.5, 0.5, 100)
        self.sleep(0.5)
        map_pin_catherine = self.find_one('map_pin_catherine', box=self.box_of_screen(0.1, 0.1, 0.9, 0.9))
        if not map_pin_catherine:
            self.log_info("No map_pin_catherine found")
            self.click_relative(0.5, 0.5, after_sleep=1)
        else:
            self.click(map_pin_catherine, after_sleep=1)
        map_option_catherine = self.find_one('map_option_catherine', horizontal_variance=0.03, vertical_variance=0.1)
        self.click(map_option_catherine, after_sleep=1)
        self.wait_confirm_dialog(btn='btn_teleport')
        self.wait_world()

    def go_to_catherine(self):
        self.executor.interaction.operate(self.do_go_to_catherine, block=True)

    def do_go_to_catherine(self):
        self.sleep(0.2)
        self.executor.interaction.do_move_mouse_relative(-700, 0)
        self.sleep(0.2)
        self.do_walk_to_f(min_time=1.5, time_out=2)
