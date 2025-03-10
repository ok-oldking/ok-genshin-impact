import re
import time
from typing import List

import cv2
import numpy as np

from ok import BaseTask, find_boxes_within_boundary, find_boxes_by_name, Box, calculate_color_percentage, og
from ok import Logger

logger = Logger.get_logger(__name__)


class BaseGiTask(BaseTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def in_world(self):
        return self.find_one('top_left_paimon')

    def in_world_or_dungeon(self):
        return self.find_one('top_right_bag')

    def click(self, x: int | Box | List[Box] = -1, y=-1, move_back=False, name=None, interval=-1, move=True,
              down_time=0.01, after_sleep=0):
        super().click(x, y, move_back=move_back, name=name, move=move, down_time=0.02)



    def find_choices(self, box, horizontal=0, vertical=0, limit=1, threshold=0.2) -> List[Box]:
        result = []
        to_find = box
        count = 0
        horizontal = int(horizontal)
        vertical = int(vertical)
        start = time.time()
        while True:
            frame = self.frame
            to_find = Box(to_find.x + horizontal, to_find.y + vertical, to_find.width, to_find.height, name='choice')
            percentage_white = calculate_color_percentage(frame, white_color, to_find)
            # percentage_grey = calculate_color_percentage(frame, dark_gray_color, to_find)
            to_find.confidence = percentage_white
            # self.logger.debug(f'percentage_white:{percentage_white}')
            self.draw_boxes(boxes=to_find)
            if to_find.confidence > threshold:
                count = count + 1
                result.append(to_find)
                if count >= limit:
                    break
                if horizontal == 0 and vertical == 0:
                    break
            else:
                percentage_less_white = calculate_color_percentage(frame, less_white_color, to_find)
                # self.logger.debug(f'percentage_less_white:{percentage_less_white}')
                if percentage_less_white > threshold - 0.05 and time.time() - start < 1:
                    self.next_frame()
                    continue
                break
        return result

    def find_tree(self, threshold=0.5) -> List[Box]:
        """
        Main function to load ONNX model, perform inference, draw bounding boxes, and display the output image.

        Args:
            onnx_model (str): Path to the ONNX model.
            input_image (ndarray): Path to the input image.

        Returns:
            list: List of dictionaries containing detection information such as class_id, class_name, confidence, etc.
        """
        # Load the ONNX model
        model = og.my_app.tree_model

        # Read the input image
        # original_image: np.ndarray = cv2.imread(input_image)
        original_image: np.ndarray = self.frame
        [height, width, _] = original_image.shape

        # Prepare a square image for inference
        length = max((height, width))
        image = np.zeros((length, length, 3), np.uint8)
        image[0:height, 0:width] = original_image
        model_length = 640
        # Calculate scale factor
        scale = length / model_length

        # Preprocess the image and prepare blob for model
        blob = cv2.dnn.blobFromImage(image, scalefactor=1 / 255, size=(model_length, model_length), swapRB=True)
        model.setInput(blob)

        # Perform inference
        outputs = model.forward()

        # Prepare output array
        outputs = np.array([cv2.transpose(outputs[0])])
        rows = outputs.shape[1]

        boxes = []
        scores = []
        class_ids = []

        # Iterate through output to collect bounding boxes, confidence scores, and class IDs
        for i in range(rows):
            classes_scores = outputs[0][i][4:]
            (minScore, maxScore, minClassLoc, (x, maxClassIndex)) = cv2.minMaxLoc(classes_scores)
            if maxScore >= 0.25:
                box = [
                    outputs[0][i][0] - (0.5 * outputs[0][i][2]),
                    outputs[0][i][1] - (0.5 * outputs[0][i][3]),
                    outputs[0][i][2],
                    outputs[0][i][3],
                ]
                boxes.append(box)
                scores.append(maxScore)
                class_ids.append(maxClassIndex)

        # Apply NMS (Non-maximum suppression)
        result_boxes = cv2.dnn.NMSBoxes(boxes, scores, threshold, 0.45, 0.5)

        detections = []

        # Iterate through NMS results to draw bounding boxes and labels
        for i in range(len(result_boxes)):
            index = result_boxes[i]
            box = boxes[index]
            my_box = Box(box[0] * scale, box[1] * scale, box[2]* scale, box[3] * scale)
            my_box.name = "Tree"
            my_box.confidence = scores[index]
            detections.append(my_box)

        return sorted(detections, key=lambda detection: detection.confidence, reverse=True)



white_color = {
    'r': (245, 255),  # Red range
    'g': (245, 255),  # Green range
    'b': (245, 255)  # Blue range
}

pick_up_text_green_color = {
    'r': (162, 182),  # Red range
    'g': (245, 255),  # Green range
    'b': (59, 75)  # Blue range
}

pick_up_text_blue_color = {
    'r': (59, 79),  # Red range
    'g': (245, 255),  # Green range
    'b': (245, 255)  # Blue range
}

pick_up_text_purple_color = {
    'r': (162, 182),  # Red range
    'g': (245, 255),  # Green range
    'b': (59, 75)  # Blue range
}

less_white_color = {
    'r': (210, 250),  # Red range
    'g': (210, 250),  # Green range
    'b': (210, 250)  # Blue range
}

dark_gray_color = {
    'r': (40, 60),  # Red range
    'g': (40, 75),  # Green range
    'b': (40, 85)  # Blue range
}


