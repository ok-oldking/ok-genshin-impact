# Test case
import unittest

from config import config
from ok.test.TaskTestCase import TaskTestCase
from src.tasks.BaseGiTask import BaseGiTask


class TestBattleBaseSerialization(TaskTestCase):
    task_class = BaseGiTask

    config = config

    def test_base(self):
        # Create a BattleReport object
        self.set_image('tests/images/main.png')
        trees = self.task.find_tree()
        self.assertEqual(len(trees), 1)


if __name__ == '__main__':
    unittest.main()
