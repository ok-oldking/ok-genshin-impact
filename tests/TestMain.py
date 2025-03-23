# Test case
import unittest

from config import config
from ok.test.TaskTestCase import TaskTestCase
from src.tasks.BaseGiTask import BaseGiTask


class TestMain(TaskTestCase):
    task_class = BaseGiTask

    config = config

    def test_base(self):
        # Create a BattleReport object
        self.set_image('tests/images/tree.png')
        tree = self.task.find_tree()
        self.assertIsNotNone(tree)


if __name__ == '__main__':
    unittest.main()
