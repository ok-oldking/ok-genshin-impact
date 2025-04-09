# Test case
import unittest

from config import config
from ok.test.TaskTestCase import TaskTestCase
from src.tasks.AutoPickTask import AutoPickTask


class TestAngle(TaskTestCase):
    task_class = AutoPickTask

    config = config

    def test(self):
        # Create a BattleReport object
        self.set_image('tests/images/search_arrow.png')
        angle, box = self.task.get_angle()
        print(f'TestAngle {angle}')
        self.task.screenshot('angle', box.crop_frame(self.task.frame))
        self.assertTrue(270 < angle < 360)


if __name__ == '__main__':
    unittest.main()
