import re
from typing import List

from ok import BaseTask, find_boxes_within_boundary, find_boxes_by_name, Box, calculate_color_percentage
from ok import Logger

logger = Logger.get_logger(__name__)


class BaseGiTask(BaseTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def in_world(self):
        return self.find_one('top_left_paimon')

    def in_world_or_dungeon(self):
        return self.find_one('top_right_bag')

    def find_choices(self, box, horizontal=0, vertical=0, limit=1000, threshold=0.6) -> List[Box]:
        result = []
        to_find = box
        count = 0
        horizontal = int(horizontal)
        vertical = int(vertical)
        frame = self.frame
        while True:
            to_find = Box(to_find.x + horizontal, to_find.y + vertical, to_find.width, to_find.height, name='choice')
            percentage_white = calculate_color_percentage(frame, white_color, to_find)
            # percentage_grey = calculate_color_percentage(frame, dark_gray_color, to_find)
            to_find.confidence = percentage_white
            if percentage_white < 0.03:
                to_find.confidence = 0
            if to_find.confidence > threshold:
                count = count + 1
                result.append(to_find)
                if count >= limit:
                    break
                if horizontal == 0 and vertical == 0:
                    break
            else:
                break
        return result



white_color = {
    'r': (250, 255),  # Red range
    'g': (250, 255),  # Green range
    'b': (250, 255)  # Blue range
}

dark_gray_color = {
    'r': (40, 60),  # Red range
    'g': (40, 75),  # Green range
    'b': (40, 85)  # Blue range
}


# def find_choice(frame, box, horizontal=0, vertical=0, threshold=0.6) -> Box | None:
#     result = find_choices(frame, box, horizontal, vertical, 1, threshold)
#     if len(result) > 0:
#         return result[0]
#     else:
#         return None


