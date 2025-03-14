import re
import time
from typing import List

import cv2
import numpy as np

from ok import BaseTask, Box, calculate_color_percentage, og, Feature, ConfigOption
from ok import Logger

logger = Logger.get_logger(__name__)

class BaseGiTask(BaseTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def find_f_box(self):
        return self.box_of_screen(0.63, 0.36, 0.65, 0.77)

    @property
    def find_choices_box(self):
        return self.box_of_screen(0.66, 0.36, 0.69, 0.77)

    def find_f(self):
        return self.find_one("f", vertical_variance=0.14)

    def in_world(self):
        return self.find_one('top_left_paimon')

    def in_world_or_domain(self):
        return self.in_world() or self.find_one('top_left_dungeon')

    def in_domain(self):
        return self.find_one('top_left_dungeon')

    def click(self, x: int | Box | List[Box] = -1, y=-1, move_back=False, name=None, interval=-1, move=True,
              down_time=0.01, after_sleep=0):
        super().click(x, y, move_back=move_back, name=name, move=move, down_time=0.03, after_sleep=after_sleep)

    def do_walk_to_f(self, time_out=5, run=True, min_time=0, direction_fun=None):
        self.do_send_key_down('w')
        if run:
            self.sleep(0.1)
            self.executor.interaction.do_mouse_down(btn='right')
        if min_time:
            self.sleep(min_time)
        start = time.time()
        found = False
        current_direction = None
        while time.time() - start < time_out:
            if self.find_f():
                self.log_info(f'found f while walking cost:{time.time() - start}')
                self.executor.interaction.do_send_key('f')
                if run:
                    self.executor.interaction.do_mouse_up(btn='right')
                self.do_send_key_up('w')
                found = True
                break
            if direction_fun:
                target = direction_fun()
                if target:
                    distance = target.center()[0] - self.width / 2
                else:
                    distance = 0
                if abs(distance) < self.width_of_screen(0.02):
                    new_direction = None
                elif distance > 0:
                    new_direction = 'd'
                else:
                    new_direction = 'a'
                if new_direction != current_direction:
                    self.log_info(f'changed direction {new_direction}')
                    if current_direction:
                        self.do_send_key_up(current_direction)
                        self.sleep(0.1)
                    if new_direction:
                        self.do_send_key_down(new_direction)
                    current_direction = new_direction
            self.next_frame()
        if current_direction:
            self.do_send_key_up(current_direction)
        if run:
            self.executor.interaction.do_mouse_up(btn='right')
        self.do_send_key_up('w')

        if found:
            self.sleep(1)
        return found

    def do_send_key_down(self, key):
        self.executor.interaction.do_send_key_down(key)

    def do_send_key_up(self, key):
        self.executor.interaction.do_send_key_up(key)

    def walk_to_f(self, time_out=5, run=True, min_time=0):
        if self.find_f() and min_time == 0:
            self.send_key('f')
            return True
        return self.executor.interaction.operate(
            lambda: self.do_walk_to_f(time_out=time_out, run=run, min_time=min_time), block=True)

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

    def chat_catherine(self):
        self.wait_until(self.find_f, raise_if_not_found=True)
        self.send_key('f', after_sleep=2)
        self.send_key('space', after_sleep=2)

    def claim_rewards(self):
        pick_daily_reward = self.find_pick_up_with_yellow_text('pick_daily_reward')
        if pick_daily_reward:
            self.click(pick_daily_reward, after_sleep=3)
            self.back(after_sleep=3)
            f = self.wait_until(self.find_f, raise_if_not_found=True)
            self.click(f, after_sleep=2)
            self.send_key('space', after_sleep=2)

        pick_daily_expedition = self.find_pick_up_with_yellow_text('pick_daily_expedition')

        if pick_daily_expedition:
            self.click(pick_daily_expedition)
            self.wait_click_feature('claim_all', settle_time=0.5)
            self.wait_click_feature('dispatch_again', settle_time=0.5, after_sleep=1.5)
            self.back(after_sleep=3)

    def find_pick_up_with_yellow_text(self, feature):
        pick_daily_reward = self.find_one(feature, box=self.find_choices_box)
        if not pick_daily_reward:
            raise RuntimeError("No daily reward found")
        text_zone = pick_daily_reward.copy(x_offset=pick_daily_reward.width * 3,
                                           width_offset=pick_daily_reward.width * 1.2)
        yellow_percent = self.calculate_color_percentage(pick_up_text_yellow_color, text_zone)
        self.log_debug(f"{feature} yellow_percent={yellow_percent}"'')
        if yellow_percent > 0.05:
            return pick_daily_reward

    def teleport_to_fontaine_catherine(self):
        self.send_key('m')
        self.wait_feature('map_close', raise_if_not_found=True, settle_time=1)
        self.scroll_relative(0.5, 0.5, 100)
        self.sleep(0.5)
        self.click_relative(0.96, 0.95, after_sleep=1)
        self.click_relative(0.75, 0.35, after_sleep=1)
        map_pin_catherine = self.find_one('map_pin_catherine', box=self.box_of_screen(0.1, 0.1, 0.9, 0.9))
        if not map_pin_catherine:
            self.log_info("No map_pin_catherine found")
            self.click_relative(0.5, 0.5, after_sleep=1)
        else:
            self.click(map_pin_catherine, after_sleep=1)
        self.wait_click_feature('map_option_catherine', raise_if_not_found=True,
                                horizontal_variance=0.1,
                                vertical_variance=0.2, after_sleep=1, settle_time=0.5)
        self.wait_confirm_dialog(btn='btn_teleport')
        self.wait_world()
        self.sleep(1)

    def go_to_catherine(self):
        self.executor.interaction.operate(self.do_go_to_catherine, block=True)
        self.wait_feature('pick_daily_reward', settle_time=0.5,
                          post_action=lambda: self.send_key('space', after_sleep=1))

    def go_and_craft(self):
        self.executor.interaction.operate(self.do_go_to_craft, block=True)
        ok = self.wait_feature('btn_ok', box='bottom_right', settle_time=0.5,
                               post_action=lambda: self.send_key('space', after_sleep=1))
        self.click(ok, after_sleep=1)
        self.back(after_sleep=1)
        self.back(after_sleep=1)

    def claim_daily_book(self):
        self.open_book()
        if box := self.find_red_dot(box='box_commission'):
            self.click(box, after_sleep=1)
            if gift := self.find_one('daily_claim_gift', horizontal_variance=0.05, vertical_variance=0.05):
                self.click(gift, after_sleep=1)
        self.ensure_main()

    def find_red_dot(self, box):
        if self.find_one('red_dot', box=box):
            return self.get_box_by_name(box)

    def do_go_to_craft(self):
        self.sleep(0.2)
        self.executor.interaction.do_move_mouse_relative(120, 0)
        self.sleep(0.2)
        self.do_walk_to_f(min_time=1.5, time_out=6)

    def do_go_to_catherine(self):
        self.sleep(0.2)
        self.executor.interaction.do_move_mouse_relative(-700, 0)
        self.sleep(0.2)
        self.do_walk_to_f(min_time=1.5, time_out=2)

    def find_tree(self, threshold=0.5) -> Box:
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

        ret = sorted(detections, key=lambda detection: detection.confidence, reverse=True)
        if ret:
            return ret[0]

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
            self.sleep(2)
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

    def turn_east(self):
        angle = self.get_angle()
        self.info_set('East Angle:', angle)
        if angle is not None:
            self.executor.interaction.operate(lambda: self.do_turn_angle(angle * -1), block=True)

    def turn_east_and_move_to(self, fun):
        angle = self.get_angle()
        self.info_set('East Angle:', angle)
        self.executor.interaction.operate(lambda: self.do_turn_east_and_move_to(angle * -1, fun), block=True)

    def do_turn_east_and_move_to(self, angle, fun):
        self.do_turn_angle(angle)
        self.do_walk_to_f(direction_fun=fun)

    def do_turn_angle(self, angle):
        self.executor.interaction.do_middle_click(self.width_of_screen(0.5), self.height_of_screen(0.5), down_time=0.02)
        self.sleep(0.5)
        turn_per_angle = 20.8
        self.sleep(0.1)
        self.executor.interaction.do_move_mouse_relative(round(turn_per_angle * angle), 0)
        self.sleep(0.1)
        self.do_send_key_down('w')
        self.sleep(0.2)
        self.do_send_key_up('w')
        self.sleep(0.6)
        self.info_set(f'turn_angle_after', self.get_angle())

    def get_angle(self):
        arrow_template = self.get_feature_by_name('domain_map_arrow_east')
        original_mat = arrow_template.mat
        max_conf = 0
        max_angle = None
        (h, w) = arrow_template.mat.shape[:2]
        self.log_debug(f'turn_east h:{h} w:{w}')
        center = (w // 2, h // 2)
        target_box = self.get_box_by_name('domain_map_arrow_east')
        target_box = target_box.copy(x_offset=-target_box.width * 0.2, y_offset=-target_box.height * 0.2,
                                     width_offset=target_box.width * 0.4, height_offset=target_box.height * 0.4)
        if self.debug:
            self.screenshot('arrow_original', original_mat)
        for angle in range(0, 360):
            # Rotate the template image
            rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
            arrow_template.mat = cv2.warpAffine(original_mat, rotation_matrix, (w, h))
            arrow_template.mask = np.where(np.all(arrow_template.mat == [0, 0, 0], axis=2), 0, 255).astype(np.uint8)

            target = self.find_one(f'arrow_{angle}', box=target_box,
                                   template=arrow_template, threshold=0.5)
            if self.debug and angle % 90 == 0:
                self.screenshot(f'arrow_rotated_{angle}', arrow_template.mat)
            if target and target.confidence > max_conf:
                max_conf = target.confidence
                max_angle = angle
        arrow_template.mat = original_mat
        arrow_template.mask = None
        self.log_debug(f'turn_east max_conf: {max_conf} {max_angle}')
        if max_angle is not None:
            if max_angle > 180:
                return 360 - max_angle
            else:
                return max_angle * -1

    def do_move_to(self, fun):
        start = time.time()
        target = fun()
        if not target:
            raise Exception('Move Failed can not find target!')
        distance = target.center()[0] - self.width / 2
        if abs(distance) <= self.width_of_screen(0.05):
            self.log_info(f'do_move_to Do not need to move! {distance}')
            return
        if distance > 0:
            direction = 'd'
        else:
            direction = 'a'
        self.do_send_key_down(direction)
        self.log_info(f'do_move_to start moving! {distance} {direction}')
        while time.time() - start < 10:
            target = fun()
            if self.debug:
                self.draw_boxes(boxes=target)
            if target:
                distance = target.center()[0] - self.width / 2
            if abs(distance) <= self.width_of_screen(0.1):
                self.log_info(f'do_move_to move success {distance}')
                self.do_send_key_up(direction)
                return
            self.next_frame()



    def do_turn_to(self, fun):
        self.executor.interaction.do_middle_click(self.width_of_screen(0.5), self.height_of_screen(0.5), down_time=0.02)
        self.sleep(0.5)
        start = time.time()
        found_tree = False
        change_count = 0
        step = 100
        direction = 1
        abs_distance = self.width
        while time.time() - start < 20:
            d_start = time.time()
            target = fun()
            if isinstance(target, list):
                if len(target) > 0:
                    target = target[0]
            self.draw_boxes(boxes=target)
            if target:
                distance = target.center()[0] - self.width / 2
                abs_distance = abs(distance)
            else:
                distance = 1
            if target:
                self.log_debug(
                    f'trees: {target} cost:{time.time() - d_start} {target.center()[0]} {self.width} distance:{distance}')

            new_direction = -1 if distance < 0 else 1

            if target and direction != new_direction:
                direction = new_direction
                step = max(1, int(step / 2))
                change_count += 1
                self.log_debug(f'turning {direction} to {new_direction}')
            if change_count >= 4:
                self.log_info('turned a lot of trees, break')
                break
            if not target and abs_distance <= self.width_of_screen(0.005):
                logger.info('found and lost tree break')
                break
            self.executor.interaction.do_move_mouse_relative(direction * step, 0)
            self.next_frame()
        target = fun()
        if isinstance(target, list):
            target = target[0]
        if self.debug:
            self.draw_boxes(boxes=target)
        if target:
            self.log_info(f'trees: {target} {self.width / 2 - target.center()[0]}')
        else:
            self.log_info('no trees')


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

pick_up_text_yellow_color = {
    'r': (245, 255),  # Red range
    'g': (194, 214),  # Green range
    'b': (40, 60)  # Blue range
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


def create_mask(rotated_image):
    mask = np.ones(rotated_image.shape, dtype=np.uint8) * 255
    for i in range(rotated_image.shape[0]):
        for j in range(rotated_image.shape[1]):
            if rotated_image[i, j] == 0:  # Assuming black is the background color
                mask[i, j] = 0
    return mask
