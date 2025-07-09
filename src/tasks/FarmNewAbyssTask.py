import re

from ok import Logger
from src.tasks.BaseCombatTask import BaseCombatTask

logger = Logger.get_logger(__name__)


class FarmNewAbyssTask(BaseCombatTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "幽境危战"
        self.description = "刷困难幽境危战, 需要先手动通关一次所选战场困难难度"
        self.default_config.update({
            '战场': "战场一",
            'Combat Sequence': '1EQ2EQ3EQ4EQ',
            'Use Original Resin': False
        })
        self.bgs = ['战场一', '战场二', '战场三']
        self.config_type['战场'] = {'type': "drop_down", 'options': self.bgs}
        self.config_description.update({
            'Use Original Resin': 'Only use Condensed Resin if Turned Off'
        })

    def run(self):
        self.ensure_main()
        self.go()
        self.loop_battle()

    def go(self):
        self.send_key('f5')
        self.wait_click_ocr(box='top_left', match="幽境危战", settle_time=0.5, after_sleep=1, raise_if_not_found=True)
        self.wait_click_ocr(box='bottom_right', match="前往挑战", settle_time=0.5, after_sleep=1,
                            raise_if_not_found=True)
        self.wait_confirm_dialog(btn='btn_teleport')
        self.wait_world()
        self.sleep(1)
        self.send_key('f')
        texts = self.wait_ocr(box='top', match=["常规挑战", "致危挑战"], settle_time=1, time_out=30,
                              raise_if_not_found=True)
        if texts[0].name == "致危挑战":
            self.click(texts, after_sleep=1)
        texts = self.ocr(box='top_right', match=re.compile("困难"))
        if not texts:
            self.click_relative(0.59, 0.17, after_sleep=1)
            self.click_relative(0.6, 0.37, after_sleep=1)
        self.confirm_dialog(btn='btn_ok')

    def in_new_abyss(self):
        return self.find_one('new_abyss_mark')

    def q_ended(self):
        return self.in_new_abyss()

    def wait_new_abyss(self):
        self.wait_until(self.in_new_abyss, settle_time=1, time_out=30, raise_if_not_found=True)

    def loop_battle(self):
        start = True
        while True:
            self.wait_new_abyss()
            if start:
                if not self.walk_to_f(time_out=7):
                    raise RuntimeError('Can not find the Domain key!')
                start = self.wait_ocr(box="bottom_right", match="开始挑战", raise_if_not_found=True, settle_time=1)
                if self.config.get("战场") == "战场一":
                    y = 0.31
                elif self.config.get("战场") == "战场二":
                    y = 0.51
                else:
                    y = 0.67
                self.click_relative(0.11, y, after_sleep=1)
                self.click(start, after_sleep=1)
                self.wait_new_abyss()
                start = False
            self.sleep(3)
            back = self.auto_combat(end_check=self.combat_ended)
            self.click(back, after_sleep=1)
            self.wait_new_abyss()
            self.sleep(1)
            self.turn_and_walk_to_box()
            if not self.claim_domain():
                break
        self.sleep(1)
        self.send_key('esc', after_sleep=1)
        self.wait_click_ocr(box="bottom", match='退出挑战', settle_time=0.5, raise_if_not_found=True)
        self.wait_world()

    def combat_ended(self):
        return self.ocr(box="bottom", match="返回")

