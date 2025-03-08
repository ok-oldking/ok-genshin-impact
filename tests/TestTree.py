# Test case
import unittest

from config import config
from ok.test.TaskTestCase import TaskTestCase
from src.tasks.BaseGfTask import BaseGfTask

from src.tasks import FarmRelicTask


class TestBattleBaseSerialization(TaskTestCase):
    task_class = FarmRelicTask

    config = config

    def test_base(self):
        # Create a BattleReport object
        self.set_image('tests/images/tree.png')
        self.task.ensure_main()


if __name__ == '__main__':
    unittest.main()
