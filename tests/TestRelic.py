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
        self.task.screenshot('btn_ok')
        print(f'FarmRelicTask btn_ok {btn_ok}')
        self.assertEqual(1, len(btn_ok))


if __name__ == '__main__':
    unittest.main()
