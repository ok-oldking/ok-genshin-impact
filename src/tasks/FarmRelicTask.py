from ok import Logger
from src.tasks.BaseCombatTask import BaseCombatTask
from src.tasks.BaseGiTask import number_re, stamina_re

logger = Logger.get_logger(__name__)


class FarmRelicTask(BaseCombatTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "Farm Relic Task"
        self.description = "Farm Relic Task"
        self.default_config.update({
            'Relic Domain To Farm': 1,
            'Combat Sequence': '1EQ2EQ3EQ4EQ',
            'Use Original Resin': False
        })
        self.config_description.update({
            'Relic Domain To Farm': 'Which Relic Domain to Farm, in the F1 Book (1-17)'
        })
        self.config_description.update({
            'Use Original Resin': 'Only use Condensed Resin if Turned Off'
        })


    def run(self):
        if self.teleport_into_domain():
            self.farm_relic_til_no_stamina()
        self.log_info(f'Farm Relic Completed!', notify=True)

    def teleport_into_domain(self):
        self.info_set('current task', 'teleport_into_domain')
        to_farm = self.config['Relic Domain To Farm']
        success = self.scroll_into_relic(to_farm, self.config.get('Use Original Resin'))
        if not success:
            self.log_info(f'No Resin to Farm Relic!', notify=True)
            self.ensure_main()
        return success

    def farm_relic_til_no_stamina(self):
        self.info_set('current task', 'farm_relic_til_no_stamina')
        while True:
            self.info_incr('Farm Relic Domain Count')
            self.wait_until(self.wait_in_domain, settle_time=1, time_out=50, raise_if_not_found=True)
            if not self.walk_to_f(time_out=7):
                raise RuntimeError('Can not find the Domain key!')
            self.auto_combat(end_check=self.domain_combat_end)
            if not self.turn_east_and_move_to(self.find_tree):
                self.log_error('Can get to the Domain Tree, please move manually, and then click continue!',
                               notify=True)
                self.screenshot('can_not_goto_tree')
                self.pause()
                self.move_to_tree()
            if not self.claim_domain():
                break
        self.wait_world()

    def move_to_tree(self):
        self.turn_east_and_move_to(self.find_tree)

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

        self.wait_feature('btn_ok', box='bottom', time_out=20, raise_if_not_found=True,
                          settle_time=1, threshold=0.9)

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
        double_resin = 1 if self.find_one('double_resin_icon') else 0

        stamina_texts = self.ocr(box=self.box_of_screen(0.72, 0.02, 0.83, 0.07), match=stamina_re, log=True)
        if not stamina_texts:
            raise Exception('Can not find resin left!')
        
        return double_resin, int(stamina_texts[0].name.split('/')[0])

    def turn_and_walk_to_tree(self):
        self.executor.interaction.operate(self.do_turn_and_walk_to_tree, block=True)

    def do_turn_and_walk_to_tree(self):
        self.do_turn_to(self.find_tree)
        if not self.do_walk_to_f(time_out=10):
            raise RuntimeError('Can not walk to the tree')

    def wait_in_domain(self):
        if self.find_one('relic_pop_up'):
            if self.debug:
                self.screenshot('relic_pop_up before')
            self.sleep(1)
            self.back(after_sleep=1)
            if self.debug:
                self.screenshot('relic_pop_up after')
            return False
        if self.in_domain():
            if self.debug:
                self.screenshot('in_domain')
            return True
