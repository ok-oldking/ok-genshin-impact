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
            if not self.move_to_tree():
                self.log_error('Can get to the Domain Tree, please move manually, and then click continue!',
                               notify=True)
                self.screenshot('can_not_goto_tree')
                self.pause()
                self.move_to_tree()
            self.wait_feature('tree_close', settle_time=0.3)
            if not self.claim_domain():
                break
        self.wait_world()

    def move_to_tree(self):
        return self.turn_east_and_move_to(self.find_tree)

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
