# Test case
import unittest


from config import config
from ok.test.TaskTestCase import TaskTestCase
from src.tasks.FarmRelicTask import FarmRelicTask


class TestRelic(TaskTestCase):
    task_class = FarmRelicTask

    config = config

    def test_base(self):
        # Create a BattleReport object
        self.set_image('tests/images/end_battle.png')
        # btn_ok = self.task.wait_feature('btn_ok', box='bottom', time_out=20, raise_if_not_found=True,
        #                                 settle_time=1)
        btn_ok = self.task.confirm_dialog()
        # self.task.screenshot('btn_ok')
        print(f'FarmRelicTask btn_ok {btn_ok}')
        self.assertEqual(1, len(btn_ok))

    def test_resin(self):
        # Create a BattleReport object
        self.set_image('tests/images/resin.png')
        # btn_ok = self.task.wait_feature('btn_ok', box='bottom', time_out=20, raise_if_not_found=True,
        #                                 settle_time=1)
        double_resin, resin = self.task.find_resin_left()
        # self.task.screenshot('btn_ok')
        # print(f'FarmRelicTask btn_ok {btn_ok}')
        self.assertEqual(0, double_resin)
        self.assertEqual(122, resin)

    def test_resin2(self):
        # Create a BattleReport object
        self.set_image('tests/images/end_battle.png')
        # btn_ok = self.task.wait_feature('btn_ok', box='bottom', time_out=20, raise_if_not_found=True,
        #                                 settle_time=1)
        double_resin, resin = self.task.find_resin_left()
        # self.task.screenshot('btn_ok')
        # print(f'FarmRelicTask btn_ok {btn_ok}')
        self.assertEqual(0, double_resin)
        self.assertEqual(109, resin)


if __name__ == '__main__':
    unittest.main()
