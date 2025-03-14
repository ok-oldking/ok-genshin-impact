from ok import Logger, find_boxes_by_name, find_boxes_within_boundary
from src.tasks.BaseGiTask import BaseGiTask, pick_up_text_yellow_color

logger = Logger.get_logger(__name__)


class ClaimDailyRewardTask(BaseGiTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "Claim Daily Reward"
        self.description = "Teleport to Fontaine and Claim Daily Reward and Expedition"

    def run(self):
        self.ensure_main()
        self.teleport_to_fontaine_catherine()
        self.claim_daily_book()
        self.go_to_catherine()
        self.claim_rewards()
        self.claim_expedition()
        return

