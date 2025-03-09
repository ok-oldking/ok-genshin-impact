from os import path

import cv2
from PySide6.QtCore import Signal, QObject

from ok import Config, Logger, get_path_relative_to_exe

logger = Logger.get_logger(__name__)


class Globals(QObject):

    def __init__(self, exit_event):
        super().__init__()
        self._tree_model = None

    @property
    def tree_model(self):
        if self._tree_model is None:
            self._tree_model =  cv2.dnn.readNetFromONNX(get_path_relative_to_exe(path.join('assets', 'yolo', 'big_tree.onnx')))
        return self._tree_model


if __name__ == "__main__":
    glbs = Globals(exit_event=None)
