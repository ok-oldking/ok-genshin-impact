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
        triggered = self.task.trigger()
        print(f'TestPick triggered {triggered}')
        self.assertIsNone(triggered)


if __name__ == '__main__':
    unittest.main()
