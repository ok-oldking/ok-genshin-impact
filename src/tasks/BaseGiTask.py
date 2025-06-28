import math
import re
import time
from typing import List

import cv2
import numpy as np
import win32api
import win32con

from ok import BaseTask, Box, calculate_color_percentage, og, Feature, create_non_black_mask
from ok import Logger

logger = Logger.get_logger(__name__)

class BaseGiTask(BaseTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._turn_per_angle = 0

    @property
    def find_f_box(self):
        return self.box_of_screen(0.63, 0.36, 0.65, 0.77)

    @property
    def find_choices_box(self):
        return self.box_of_screen(0.66, 0.36, 0.69, 0.77)

    def login(self):
        if og.my_app.logged_in:
            return True
        if self.in_world_or_domain():
            self.log_info(f'in_world_or_domain set login to True')
            og.my_app.logged_in = True
            return True
        if self.find_one('log_out'):
            self.log_info(f'login click center')
            self.click_relative(0.5, 0.5, after_sleep=3)
            return
        if self.find_one('monthly_card'):
            self.log_info(f'monthly_card click center')
            self.click_relative(0.5, 0.5, after_sleep=3)
            return
        if self.find_one('monthly_card_diamond'):
            self.log_info(f'monthly_card click center')
            self.click_relative(0.5, 0.6, after_sleep=3)
            return

    def find_f(self):
        return self.find_one("f", vertical_variance=0.16)

    def in_world(self):
        if self.find_one('top_left_paimon'):
            og.my_app.logged_in = True
            return True

    def in_world_or_domain(self):
        if self.in_world() or self.in_domain():
            og.my_app.logged_in = True
            return True

    def in_domain(self):
        return self.find_one('top_left_dungeon')

    def click(self, x: int | Box | List[Box] = -1, y=-1, move_back=False, name=None, interval=-1, move=True,
              down_time=0.01, after_sleep=0, key="left"):
        super().click(x, y, move_back=move_back, name=name, move=move, down_time=0.03, after_sleep=after_sleep, key=key)

    def calculate_angle_between(self, box1: Box, box2: Box):
        center1_x, center1_y = box1.center()
        center2_x, center2_y = box2.center()
        delta_x = center2_x - center1_x
        delta_y = center2_y - center1_y

        angle_radians = math.atan2(delta_y, delta_x)  # Returns angle in radians, range [-pi, pi]
        angle_degrees = math.degrees(angle_radians)  # Convert radians to degrees

        return angle_degrees

    def mini_map_find(self, feature, threshold=0.6):
        return self.find_one(feature, box='box_mini_map', threshold=threshold)

    def do_turn_to_mini_map(self, feature):
        self.do_turn_angle(self.get_mini_map_turn_angle(feature))

    def get_mini_map_turn_angle(self, feature):
        target = self.mini_map_find(feature)
        if not target:
            self.log_info(f'Can not find {feature} on minimap')
            return 0
        my_angle, my_box = self.get_angle()
        if not my_box:
            self.log_info(f'Can not find myself on minimap')
            return 0
        angle_degrees = self.calculate_angle_between(my_box, target)
        to_turn = self.get_angle_between(my_angle, angle_degrees)
        self.log_info(f'angle: {my_angle}, angle_degrees: {angle_degrees}, to_turn: {to_turn}')
        return to_turn

    def get_angle_between(self, my_angle, angle):
        if my_angle > angle:
            to_turn = angle - my_angle
        else:
            to_turn = -(my_angle - angle)
        if to_turn > 180:
            to_turn -= 360
        elif to_turn < -180:
            to_turn += 360
        return to_turn

    def get_direction(self, direction_fun, current_direction, threshold=-1):
        target = direction_fun()
        if target:
            distance = target.center()[0] - self.width / 2
        else:
            return None
        if threshold < 0:
            if current_direction:
                threshold = 0.06
            else:
                threshold = 0.02
        if abs(distance) <= self.width_of_screen(threshold):
            new_direction = None
        elif distance > 0:
            new_direction = 'd'
        else:
            new_direction = 'a'

        return new_direction

    def do_walk_center(self, direction_fun, time_out=3):
        if not direction_fun:
            return
        start = time.time()
        current_direction = None
        while time.time() - start < time_out:
            new_direction = self.get_direction(direction_fun, current_direction, 0.08)
            if not new_direction:
                break
            if new_direction != current_direction:
                self.log_info(f'do_walk_center changed direction {new_direction}')
                if current_direction:
                    break
                if new_direction:
                    self.do_send_key_down(new_direction)
                    self.sleep(0.01)
                current_direction = new_direction
        self.log_info(f'do_walk_center end {current_direction}')
        if current_direction:
            self.do_send_key_up(current_direction)
            self.sleep(0.001)

    def do_walk_to_f(self, time_out=5, run=True, min_time=0, direction_fun=None, mini_map_target=None):
        self.log_info('do_walk_to_f start')
        # self.do_walk_center(direction_fun=direction_fun)
        self.do_send_key_down('w')
        if run:
            self.sleep(0.1)
            self.executor.interaction.do_mouse_down(key='right')
        start = time.time()
        found = False
        current_direction = None
        last_turn = 0
        while time.time() - start < time_out:
            if time.time() - start >= min_time and self.find_f() and (
                    not mini_map_target or not self.mini_map_find(mini_map_target, threshold=0.85)):
                self.log_info(f'found f while walking cost:{time.time() - start}')
                self.executor.interaction.do_send_key('f')
                if run:
                    self.executor.interaction.do_mouse_up(key='right')
                self.do_send_key_up('w')
                found = True
                break
            if mini_map_target and time.time() - last_turn > 0.5:
                angle_to_turn = self.get_mini_map_turn_angle(mini_map_target)
                if angle_to_turn:
                    self.do_turn_angle(angle_to_turn, middle_click=False)
            elif direction_fun:
                new_direction = self.get_direction(direction_fun, current_direction)
                if new_direction != current_direction:
                    self.log_info(f'changed direction {new_direction}')
                    if current_direction:
                        self.do_send_key_up(current_direction)
                        self.sleep(0.001)
                    if new_direction:
                        self.do_send_key_down(new_direction)
                    current_direction = new_direction
            self.next_frame()
        if current_direction:
            self.do_send_key_up(current_direction)
        if run:
            self.executor.interaction.do_mouse_up(key='right')
        self.do_send_key_up('w')

        if found:
            self.sleep(1)
        f_count = 0
        while self.find_f() and f_count < 3:
            self.log_error(f'do_walk_to_f f failed, send f again')
            self.screenshot('f_failed')
            self.executor.interaction.do_send_key('f')
            self.sleep(1)
            f_count += 1
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
        self.info_set('current task', 'claim_rewards')
        self.open_catherine()
        pick_daily_reward = self.find_pick_up_with_yellow_text('pick_daily_reward')
        if pick_daily_reward:
            self.click(pick_daily_reward, after_sleep=1)
            self.wait_feature('monthly_card_diamond', settle_time=1, box=self.box_of_screen(0.22, 0.23, 0.75, 0.68),
                              post_action=lambda: self.send_key('space', after_sleep=1), raise_if_not_found=True)
            self.back(after_sleep=1)
            self.wait_until(self.find_f, settle_time=1, raise_if_not_found=True)

    def claim_expedition(self):

        self.open_catherine()

        pick_daily_expedition = self.find_pick_up_with_yellow_text('pick_daily_expedition')

        if pick_daily_expedition:
            self.click(pick_daily_expedition)
            self.wait_click_feature('claim_all', settle_time=0.5)
            self.wait_click_feature('dispatch_again', settle_time=0.5, after_sleep=1.5)
            self.back(after_sleep=3)
            self.ensure_main()
        else:
            self.end_chat()

    def end_chat(self):
        dots = self.find_feature("chat_3_dots", box=self.find_choices_box)
        if dots:
            self.click(dots[-1])
            self.wait_until(self.in_world, settle_time=0.5,
                            post_action=lambda: self.send_key('space', after_sleep=1))

    def find_pick_up_with_yellow_text(self, feature):
        pick_daily_reward = self.find_one(feature, box=self.find_choices_box)
        if not pick_daily_reward:
            raise RuntimeError("No daily reward found")
        text_zone = pick_daily_reward.copy(x_offset=pick_daily_reward.width * 1.2,
                                           width_offset=pick_daily_reward.width * 1.2)
        yellow_percent = self.calculate_color_percentage(pick_up_text_yellow_color, text_zone)
        if self.debug:
            self.screenshot('yellow_percent')
            self.log_debug(f"{feature} yellow_percent={yellow_percent}"'')
        if yellow_percent > 0.05:
            return pick_daily_reward

    def teleport_to_fontaine_catherine(self):
        self.info_set('current task', 'teleport_to_fontaine_catherine')
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
        self.wait_catherine()

    def open_catherine(self):
        if not self.find_one('pick_daily_reward', box=self.find_choices_box):
            self.send_key('f', after_sleep=1)
            self.wait_catherine()

    def wait_catherine(self):
        self.wait_feature('pick_daily_reward', settle_time=0.5, box=self.find_choices_box,
                          post_action=lambda: self.send_key('space', after_sleep=1))

    def go_and_craft(self):
        self.info_set('current task', 'go_and_craft')
        self.executor.interaction.operate(self.do_go_to_craft, block=True)
        ok = self.wait_feature('btn_ok', box='bottom_right', settle_time=0.5,
                               post_action=lambda: self.send_key('space', after_sleep=1))
        self.click(ok, after_sleep=1)
        self.ensure_main()

    def claim_daily_book(self):
        if self.find_red_dot(box='box_top_right_book'):
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
        self.do_turn_to_mini_map('mini_map_craft')
        self.sleep(0.2)
        self.do_walk_to_f(min_time=1.5, time_out=6)

    def do_go_to_catherine(self):
        self.do_turn_to_mini_map('mini_map_catherine')
        self.do_walk_to_f(min_time=1.5, time_out=3, mini_map_target='mini_map_catherine')

    def find_tree(self, threshold=0.3) -> Box:
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
            self.draw_boxes('tree', ret)
            return ret[0]

    def open_book(self):
        self.send_key('f1', after_sleep=2)

    def send_key(self, key, after_sleep=0, down_time=0.04):
        super().send_key(key, after_sleep=after_sleep, down_time=down_time)

    def go_to_relic(self):
        self.ensure_main()
        self.open_book()
        self.click_relative(0.16, 0.42, after_sleep=0.5)
        # self.click_relative(0.47, 0.2, after_sleep=0.5)
        # self.click_relative(0.46, 0.31, after_sleep=0.5)

    def scroll_into_relic(self, n, use_resin):
        self.go_to_relic()
        if n > 4:
            # distance = self.measure_scroll()
            # self.sleep(1)
            # book_locations = self.find_feature('book_location', horizontal_variance=0.05, vertical_variance=1)
            # distance3 = book_locations[-1].y - book_locations[0].y
            # scroll_delta_per_row = -1 * round(distance3 / 3 / distance)
            row_to_scroll = n - 4
            scroll_delta_per_row = -8
            logger.debug(f"scroll_relic book_locations: scroll_delta_per_row:{scroll_delta_per_row}")
            self.scroll_relative(0.48, 0.32, row_to_scroll * scroll_delta_per_row + 1)
            self.sleep(1)
            n = 4
        book_locations = self.find_feature('book_location', horizontal_variance=0.05, vertical_variance=1)
        self.click(book_locations[n-1])
        self.wait_confirm_dialog(btn='btn_teleport')
        self.wait_world()
        self.walk_to_f()
        self.wait_feature('btn_ok', box='bottom_right', settle_time=1.5)
        stamina_texts = self.ocr(box=self.box_of_screen(0.73, 0, 0.93, 0.09), match=[number_re, stamina_re], log=True)
        if len(stamina_texts) != 2:
            self.log_error(f'Can not find stamina text: {stamina_texts}')
        if double_stamina_texts := self.find_boxes(stamina_texts, match=number_re):
            double_stamina = int(double_stamina_texts[0].name)
        else:
            double_stamina = 1
        if stamina_texts := self.find_boxes(stamina_texts, match=stamina_re):
            stamina = int(stamina_texts[0].name.split('/')[0])
        else:
            stamina = 20
        self.info_set('Resin', stamina)
        self.info_set('Double resin', double_stamina)
        if double_stamina == 0:
            if not use_resin:
                return False
            else:
                if stamina < 20:
                    return False
        self.wait_confirm_dialog()
        self.wait_confirm_dialog()
        return True

    def wait_world(self, time_out=60, settle_time=1):
        self.wait_until(self.in_world, time_out=time_out, settle_time=settle_time, raise_if_not_found=True)

    def walk_to_chest(self):
        self.executor.interaction.operate(lambda: self.do_walk_to_chest, block=True)

    def do_walk_to_chest(self):
        if self.find_key():
            self.send_key('f')
            return True
        if self.find_chest_icon():
            if not self.walk_to_box(self.find_chest_icon, end_condition=self.find_key):
                raise Exception("无法找到拾取体力!")
            self.send_key('f')
            return True
        raise Exception("找不到钥匙或者宝箱图标!")

    def find_key(self):
        return self.find_one("pick_b_key", vertical_variance=0.16)

    def find_chest_icon(self):
        return self.find_one('chest_icon', box=self.box_of_screen(0.1, 0.2, 0.9, 0.8), threshold=0.7)

    def walk_to_box(self, find_function, time_out=40, end_condition=None, y_offset=0):
        if not find_function:
            self.log_info('find_function not found, break')
            return False
        last_direction = None
        start = time.time()
        ended = False
        last_target = None
        centered = False
        last_x_distance = None
        while time.time() - start < time_out:
            self.next_frame()
            if end_condition:
                ended = end_condition()
                if ended:
                    break
            treasure_icon = find_function()
            if isinstance(treasure_icon, list):
                if len(treasure_icon) > 0:
                    treasure_icon = treasure_icon[0]
                else:
                    treasure_icon = None
            if treasure_icon:
                last_target = treasure_icon
            if last_target is None:
                next_direction = self.opposite_direction(last_direction)
                self.log_info('find_function not found, change to opposite direction')
            else:
                x, y = last_target.center()
                y = max(0, y - self.height_of_screen(y_offset))
                x_distance = x - self.width_of_screen(0.5)
                centered = centered or (last_x_distance is not None and x_distance * last_x_distance < 0)
                last_x_distance = x_distance
                if not centered:
                    if x > self.width_of_screen(0.5):
                        next_direction = 'd'
                    else:
                        next_direction = 'a'
                else:
                    if y > self.height_of_screen(0.5):
                        next_direction = 's'
                    else:
                        next_direction = 'w'
                if next_direction == 'd' or next_direction == 'a':
                    if last_direction:
                        self.send_key_up(last_direction)
                        self.sleep(0.01)
                    self.send_key_down(next_direction)
                    self.sleep(0.1)
                    self.send_key_up(next_direction)
                    self.sleep(0.2)
                    last_direction = None
                    continue

            if next_direction != last_direction:
                if last_direction:
                    self.send_key_up(last_direction)
                    self.sleep(0.01)
                last_direction = next_direction
                if next_direction:
                    self.send_key_down(next_direction)
        if last_direction:
            self.send_key_up(last_direction)
            self.sleep(0.001)
        if not end_condition:
            return last_direction is not None
        else:
            return ended

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
        self.info_set('current task', 'ensure main')
        start = time.time()
        while not self.in_world() and time.time() - start < 10:
            self.send_key('esc')
            self.sleep(2)
        if not self.in_world():
            raise Exception('Enter Main Page Failed!')

    def confirm_dialog(self, btn='btn_ok'):
        btn_ok = self.find_feature(btn, box='bottom', threshold=0.9)
        if not btn_ok:
            return
        if len(btn_ok) > 1:
            raise Exception('Found more than one OK button!')
        self.click(btn_ok)
        return btn_ok

    def wait_confirm_dialog(self, btn='btn_ok', time_out=10, box='bottom'):
        btn_ok = self.wait_feature(btn, box=box, raise_if_not_found=True, time_out=time_out, settle_time=1,
                                   threshold=0.9)
        self.click(btn_ok, after_sleep=1)

    def turn_east(self):
        angle, _ = self.get_angle()
        self.info_set('East Angle:', angle)
        angle_to_turn = self.get_angle_between(angle, 0)
        if angle_to_turn != 0:
            self.executor.interaction.operate(lambda: self.do_turn_angle(angle_to_turn * -1), block=True)

    def turn_angle(self, angle, vertical_angle=0, middle_click=True):
        self.executor.interaction.operate(lambda: self.do_turn_angle(angle, vertical_angle, middle_click), block=True)

    def turn_east_and_move_to(self, fun):
        success = self.executor.interaction.operate(lambda: self.do_turn_east_and_move_to(fun), block=True)
        if self.find_f():
            if self.debug:
                self.screenshot('f_again')
            raise RuntimeError(f'Failed to Claim the Domain Reward, maybe your Inventory is Full!')
        return success

    def do_turn_east_and_move_to(self, fun):
        angle, _ = self.get_angle()
        self.info_set('East Angle:', angle)
        angle_to_turn = self.get_angle_between(angle, 0)
        self.do_turn_angle(angle_to_turn)
        return self.do_walk_to_f(direction_fun=fun, time_out=12)

    def catch_butter_fly(self, time_out=10, catch_time=1):
        self.executor.interaction.operate(lambda: self.do_catch_butter_fly(time_out, catch_time=catch_time), block=True)

    def do_catch_butter_fly(self, time_out=10, catch_time=1):
        self.do_send_key_down('w')
        self.sleep(0.1)
        self.executor.interaction.do_mouse_down(key='right')
        start = time.time()
        start_catch = False
        while time.time() - start < time_out:
            if not start_catch and self.find_f():
                time_out = min(time.time() - start + catch_time, time_out)
                start_catch = True
                self.log_info(f'start catch butter fly: {time_out}')
            if start_catch:
                if self.check_interval(0.2):
                    self.executor.interaction.do_send_key('f')
            self.next_frame()
        self.executor.interaction.do_mouse_up(key='right')
        self.do_send_key_up('w')

    def do_turn_angle(self, angle, vertical_angle=0, middle_click=True):
        if middle_click:
            self.executor.interaction.do_middle_click(self.width_of_screen(0.5), self.height_of_screen(0.5),
                                                      down_time=0.02)
            self.sleep(0.5)
        turn_per_angle = self.get_turn_per_angle()
        x_move = round(turn_per_angle * angle)
        y_move = round(turn_per_angle * vertical_angle)
        self.info_set('Turn Angle', f'h:{angle} v:{vertical_angle}')
        self.executor.interaction.do_move_mouse_relative(x_move, y_move)
        if middle_click:
            self.sleep(0.1)
            self.do_send_key_down('w')
            self.sleep(0.1)
            self.do_send_key_up('w')
            self.sleep(0.2)
        self.info_set(f'turn_angle_after', self.get_angle()[0])

    def get_turn_per_angle(self):
        if not self._turn_per_angle:
            width, height = get_hwnd_screen_resolution(self.hwnd.hwnd)
            self._turn_per_angle = 20.8 * width / 3840
            self.log_info(f'get_hwnd_screen_resolution {width, height} turn_per_angle: {self._turn_per_angle}')
        return self._turn_per_angle

    def get_angle(self):
        arrow_template = self.get_feature_by_name('domain_map_arrow_east')
        original_mat = arrow_template.mat
        max_conf = 0
        max_angle = None
        max_target = None
        (h, w) = arrow_template.mat.shape[:2]
        self.log_debug(f'turn_east h:{h} w:{w}')
        center = (w // 2, h // 2)
        target_box = self.get_box_by_name('domain_map_arrow_east')
        target_box = target_box.scale(1)
        # if self.debug:
        #     self.screenshot('arrow_original', original_mat)
        for angle in range(0, 360):
            # Rotate the template image
            rotation_matrix = cv2.getRotationMatrix2D(center, -angle, 1.0)
            template = cv2.warpAffine(original_mat, rotation_matrix, (w, h))

            target = self.find_one(f'arrow_{angle}', box=target_box,
                                   template=template, threshold=0.01, mask_function=create_non_black_mask)
            # if self.debug and angle % 90 == 0:
            #     self.screenshot(f'arrow_rotated_{angle}', arrow_template.mat)
            if target and target.confidence > max_conf:
                max_conf = target.confidence
                max_angle = angle
                max_target = target
        self.log_debug(f'turn_east max_conf: {max_conf} {max_angle}')
        return max_angle, max_target

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

    def claim_mail(self):
        self.back()
        self.wait_feature('esc_achievements', settle_time=1)
        if mail := self.find_red_dot('box_mail'):
            self.click(mail)
            self.wait_click_feature('claim_all', box='bottom_left', settle_time=1)
        self.ensure_main()

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

    def claim_battle_pass(self):
        if self.find_red_dot('box_top_right_battle_pass'):
            self.send_key('f4')
            self.wait_feature('top_right_close_btn', settle_time=1)
            if dots := self.find_red_dot('battle_pass_quests'):
                self.click(dots, after_sleep=1)
                self.click_box('battle_pass_claim_all', after_sleep=1)
                self.ensure_main()


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

    def claim_domain(self):
        self.wait_feature('tree_close', settle_time=0.3)
        use_box = self.box_of_screen(0.27, 0.33, 0.36, 0.74)
        if use2 := self.find_one('use_2', box=use_box):
            use2.x += self.width_of_screen(0.65 - 0.32)
            self.click(use2)
        elif use1 := self.find_one('use_1', box=use_box):
            if self.config.get('Use Original Resin'):
                use1.x += self.width_of_screen(0.65 - 0.32)
                self.click(use1)
            else:
                self.back(after_sleep=1)
                self.back(after_sleep=1)
                self.confirm_dialog()
                return False
        else:
            raise RuntimeError('Can tree claim!')

        btn_ok = self.wait_feature('btn_ok', box='bottom', time_out=6, raise_if_not_found=False,
                                   settle_time=1, threshold=0.9)
        if not btn_ok:
            self.back(after_sleep=1)
            self.back(after_sleep=1)
            self.confirm_dialog()
            return False

        self.sleep(3)
        double_resin, resin = self.find_resin_left()
        self.info_set('Resin', resin)
        self.info_incr('Double Resin', double_resin)
        can_continue = double_resin > 0 or (self.config.get('Use Original Resin') and resin >= 20)
        self.log_info(f'Farm Relic Domain can_continue: {can_continue}')
        if can_continue:
            self.confirm_dialog(btn='btn_ok')
            self.sleep(5)
        else:
            self.confirm_dialog(btn='dungeon_exit')
        return can_continue

    def find_resin_left(self):
        double_resin = 1 if self.find_one('double_resin_icon', horizontal_variance=0.3) else 0
        stamina_texts = self.ocr(box=self.box_of_screen(0.7, 0.01, 0.92, 0.08), match=[stamina_re, number_re],
                                 log=True)
        if not stamina_texts:
            logger.error('Can not find resin left!')
            resin = 0
        else:
            if not stamina_texts[-1].name.split('/')[0]:
                resin = int(stamina_texts[-2].name.split('/')[0])
            else:
                resin = int(stamina_texts[-1].name.split('/')[0])

        return double_resin, resin

def get_hwnd_screen_resolution(hwnd):
    # Get the monitor where the hwnd is located
    monitor = win32api.MonitorFromWindow(hwnd, win32con.MONITOR_DEFAULTTONEAREST)

    # Get monitor info
    monitor_info = win32api.GetMonitorInfo(monitor)
    monitor_area = monitor_info['Monitor']  # Monitor dimensions

    width = monitor_area[2] - monitor_area[0]
    height = monitor_area[3] - monitor_area[1]

    return width, height


stamina_re = re.compile(r"^\d+/\d+$")
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
    'g': (194, 235),  # Green range
    'b': (15, 60)  # Blue range
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
