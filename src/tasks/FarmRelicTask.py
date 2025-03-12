import time
from ok import Logger
from src.tasks.BaseCombatTask import BaseCombatTask
from src.tasks.BaseGiTask import number_re

logger = Logger.get_logger(__name__)


class FarmRelicTask(BaseCombatTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "Farm Relic Task"
        self.description = "Farm Relic Task"
        self.default_config.update({
            'Relic Dungeon To Farm': 16,
            'Combat Sequence': '1EQ2EQ3EQ4EQ',
            'Use Original Resin': False
        })

    def run(self):
        self.teleport_into_dungeon()
        self.farm_relic_til_no_stamina()
        self.log_info(f'Farm Relic Completed!', notify=True)

    def teleport_into_dungeon(self):
        to_farm = self.config['Relic Dungeon To Farm']
        self.scroll_into_relic(to_farm)

    def farm_relic_til_no_stamina(self):
        while True:
            self.info_incr('Farm Relic Dungeon Count')
            self.wait_until(self.in_dungeon, time_out=40, raise_if_not_found=True)
            if not self.walk_to_f(time_out=5):
                raise RuntimeError('Can not find the dungeon key!')
            self.auto_combat(end_check=self.dungeon_combat_end)
            self.turn_and_walk_to_tree()
            if not self.claim_dungeon():
                break

    def claim_dungeon(self):
        if self.find_one('dungeon_use_double'):
            double_resin = self.ocr(box='box_double_stamina', match=number_re)
            if double_resin:
                double_resin = int(double_resin[0].name)
            else:
                double_resin = 1
            resin = self.ocr(box='box_stamina', match=number_re)
            claim_btn = None
            if double_resin > 0:
                claim_btn = 'dungeon_use_double'
                double_resin -= 1
            else:
                if self.config.get('Use Original Resin'):
                    if resin >= 20:
                        claim_btn = 'dungeon_use_stamina'
            if claim_btn:
                claim_btn = self.find_one('dungeon_use_double')
                if claim_btn:
                    self.click(claim_btn)
            else:
                self.back(after_sleep=1)
                self.back(after_sleep=1)
                self.confirm_dialog()
                return False

        self.wait_feature('btn_ok', box='bottom', time_out=20, raise_if_not_found=True,
                          settle_time=1, threshold=0.9)
        lefts = self.ocr(box='box_resin_left', match=number_re)
        if not lefts:
            raise Exception('Can not find resin left!')
        if len(lefts) == 1:
            double_resin = 0
            resin = int(lefts[0].name)
        elif len(lefts) == 2:
            double_resin = int(lefts[0].name)
            resin = int(lefts[-1].name)
        self.info_set('Resin', resin)
        self.info_incr('Double Resin', double_resin)
        can_continue = double_resin > 0 or (self.config.get('Use Original Resin') and resin >= 20)
        self.log_info(f'Farm Relic Dungeon can_continue: {can_continue}')
        if can_continue:
            self.confirm_dialog(btn='btn_ok')
        else:
            self.confirm_dialog(btn='dungeon_exit')
        return can_continue

    def turn_and_walk_to_tree(self):
        self.executor.interaction.operate(self.do_turn_and_walk_to_tree, block=True)

    def do_turn_and_walk_to_tree(self):
        self.do_turn_to_tree()
        if not self.do_walk_to_f(time_out=10):
            raise RuntimeError('Can not walk to the tree')

    def do_turn_to_tree(self):
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
            trees = self.find_tree()
            self.draw_boxes(boxes=trees)
            if trees:
                distance = trees[0].center()[0] - self.width / 2
                abs_distance = abs(distance)
            else:
                distance = 1
            if trees:
                self.log_debug(
                    f'trees: {trees[0]} cost:{time.time() - d_start} {trees[0].center()[0]} {self.width} distance:{distance}')

            new_direction = -1 if distance < 0 else 1

            if trees and direction != new_direction:
                direction = new_direction
                step = max(1, int(step / 2))
                change_count += 1
                self.log_debug(f'turning {direction} to {new_direction}')
            if change_count >= 4:
                self.log_info('turned a lot of trees, break')
                break
            if not trees and abs_distance <= self.width_of_screen(0.005):
                logger.info('found and lost tree break')
                break
            self.executor.interaction.do_move_mouse_relative(direction * step, 0)
            self.next_frame()
        trees = self.find_tree()
        if self.debug:
            self.draw_boxes(boxes=trees)
        if trees:
            self.log_info(f'trees: {trees[0]} {self.width / 2 - trees[0].center()[0]}')
        else:
            self.log_info('no trees')

    def in_dungeon(self):
        if self.in_world_or_dungeon():
            return True
        if self.find_one('relic_pop_up'):
            self.back(after_sleep=1)
            return False
