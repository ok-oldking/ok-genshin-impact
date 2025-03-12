import re
import time
from typing import List

import cv2
import numpy as np

from ok import BaseTask, Box, calculate_color_percentage, og, Feature
from ok import Logger

logger = Logger.get_logger(__name__)


class BaseGiTask(BaseTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def find_f(self):
        return self.find_one("f", vertical_variance=0.14)

    def in_world(self):
        return self.find_one('top_left_paimon')

    def in_world_or_domain(self):
        return self.in_world() or self.find_one('top_left_dungeon')

    def click(self, x: int | Box | List[Box] = -1, y=-1, move_back=False, name=None, interval=-1, move=True,
              down_time=0.01, after_sleep=0):
        super().click(x, y, move_back=move_back, name=name, move=move, down_time=0.02, after_sleep=after_sleep)

    def do_walk_to_f(self, time_out=5, run=True):
        self.do_send_key_down('w')
        if run:
            self.sleep(0.1)
            self.executor.interaction.do_mouse_down(btn='right')
        if self.wait_until(self.find_f, time_out=time_out):
            self.log_info('found f while walking')
            self.executor.interaction.do_send_key('f')
            if run:
                self.executor.interaction.do_mouse_up(btn='right')
            self.do_send_key_up('w')
            found = True
        else:
            if run:
                self.executor.interaction.do_mouse_up(btn='right')
            self.do_send_key_up('w')
            found = False
        if found:
            self.sleep(1)
        return found

    def do_send_key_down(self, key):
        self.executor.interaction.do_send_key_down(key)

    def do_send_key_up(self, key):
        self.executor.interaction.do_send_key_up(key)

    def walk_to_f(self, time_out=10, run=True):
        if self.find_f():
            self.send_key('f')
            return True
        return self.executor.interaction.operate(lambda: self.do_walk_to_f(time_out=time_out, run=run), block=True)

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

    def open_book(self):
        self.send_key('f1', after_sleep=2)

    def go_to_relic(self):
        self.ensure_main()
        self.open_book()
        self.click_relative(0.16, 0.42, after_sleep=1)
        self.click_relative(0.47, 0.2, after_sleep=0.5)
        self.click_relative(0.46, 0.31, after_sleep=0.5)

    def scroll_into_relic(self, n):
        self.go_to_relic()
        if n > 4:
            distance = self.measure_scroll()
            self.sleep(1)
            book_locations = self.find_feature('book_location', horizontal_variance=0.05, vertical_variance=1)
            distance3 = book_locations[-1].y - book_locations[0].y
            scroll_delta_per_row = -1 * round(distance3 / 3 / distance)
            row_to_scroll = n - 4
            logger.debug(f"scroll_relic book_locations:{len(book_locations)} distance3:{distance3} scroll_delta_per_row:{scroll_delta_per_row}")
            self.scroll_relative(0.48, 0.32, row_to_scroll * scroll_delta_per_row + 1)
            self.sleep(1)
            n = 4
        book_locations = self.find_feature('book_location', horizontal_variance=0.05, vertical_variance=1)
        self.click(book_locations[n-1])
        self.wait_confirm_dialog(btn='btn_teleport')
        self.wait_world()
        self.walk_to_f()
        self.wait_confirm_dialog()
        self.wait_confirm_dialog()

    def wait_world(self, time_out=60):
        self.wait_until(self.in_world, time_out=time_out, raise_if_not_found=True)

    def measure_scroll(self):
        last_box = self.box_of_screen(0.39, 0.66, 0.50, 0.72)
        last_crop = last_box.crop_frame(self.frame)

        source_template = Feature(last_crop, last_box.x, last_box.y)

        self.scroll_relative(0.48, 0.32, -1)
        self.sleep(0.5)

        target = self.find_one('target_box', box=self.box_of_screen(0.38, 0.22, 0.50, 0.72), template=source_template, threshold=0.95)
        scroll_distance =  last_box.y - target.y
        self.log_info(f'measure_scroll: {scroll_distance}')
        if scroll_distance < 1:
            raise Exception('Scroll Failed')
        return scroll_distance

    def ensure_main(self):
        start = time.time()
        while not self.in_world() and time.time() - start < 10:
            self.send_key('esc')
            self.sleep(1.5)
        if not self.in_world():
            raise Exception('Enter Main Page Failed!')

    def confirm_dialog(self, btn='btn_ok'):
        btn_ok = self.find_feature(btn, box='bottom', threshold=0.9)
        if not btn_ok:
            raise Exception('Can not find OK button!')
        if len(btn_ok) > 1:
            raise Exception('Found more than one OK button!')
        self.click(btn_ok)
        return btn_ok

    def wait_confirm_dialog(self, btn='btn_ok', time_out=10):
        btn_ok = self.wait_feature(btn, box='bottom', raise_if_not_found=True, time_out=time_out, settle_time=1,
                                   threshold=0.9)
        self.click(btn_ok, after_sleep=1)


number_re = re.compile(r'^\d+$')

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


