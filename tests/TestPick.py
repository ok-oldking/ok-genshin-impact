# Test case
import unittest

from config import config
from ok.test.TaskTestCase import TaskTestCase
from src.tasks.AutoPickTask import AutoPickTask


class TestPick(TaskTestCase):
    task_class = AutoPickTask

    config = config

    def test_base(self):
        # Create a BattleReport object
        self.set_image('tests/images/pick.png')
        triggered = self.task.run()
        print(f'TestPick triggered {triggered}')
        self.assertTrue(triggered)

    def test_yellow1(self):
        # Create a BattleReport object
        self.set_image('tests/images/yellow_percent.png')
        yellow = self.task.find_pick_up_with_yellow_text('pick_daily_expedition')
        print(f'yellow {yellow}')
        self.assertIsNotNone(yellow)

    def test_yellow2(self):
        # Create a BattleReport object
        self.set_image('tests/images/yellow_percent.png')
        yellow = self.task.find_pick_up_with_yellow_text('pick_daily_reward')
        print(f'yellow {yellow}')
        self.assertIsNotNone(yellow)


if __name__ == '__main__':
    unittest.main()
