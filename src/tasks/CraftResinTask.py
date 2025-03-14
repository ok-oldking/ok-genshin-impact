from ok import Logger, find_boxes_by_name, find_boxes_within_boundary
from src.tasks.BaseGiTask import BaseGiTask, pick_up_text_yellow_color

logger = Logger.get_logger(__name__)


class CraftResinTask(BaseGiTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "Craft Resin"
        self.description = "Teleport to Fontaine and Craft Condensed Resin"

    def run(self):
        self.turn_east_and_move_to(self.find_tree)
        return
        self.ensure_main()
        self.teleport_to_fontaine_catherine()
        self.go_and_craft()
        return
