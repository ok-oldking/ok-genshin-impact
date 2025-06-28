# Test case
import time
import unittest

from config import config
from ok.test.TaskTestCase import TaskTestCase
from src.tasks.AutoPickTask import AutoPickTask
from src.tasks.FarmNewAbyssTask import FarmNewAbyssTask


class TestPick(TaskTestCase):
    task_class = FarmNewAbyssTask

    config = config

    def test_resin2(self):
        # Create a BattleReport object
        self.set_image('tests/images/resin2.png')
        double_resin, resin = self.task.find_resin_left()
        print(f'double_resin, resin  {double_resin, resin}')
        time.sleep(1)
        self.assertEqual(0, double_resin)
        self.assertEqual(2, resin)

    def test_resin3(self):
        # Create a BattleReport object
        self.set_image('tests/images/resin3.png')
        double_resin, resin = self.task.find_resin_left()
        print(f'double_resin, resin  {double_resin, resin}')
        time.sleep(1)
        self.assertEqual(0, double_resin)
        self.assertEqual(42, resin)


if __name__ == '__main__':
    unittest.main()
