import hashlib
import os
import threading
from typing import List

import msgpack
from PySide6.QtCore import Signal, QObject
from pip._internal.utils.misc import ensure_dir

from ok import Config, Logger
from ok import Handler
from ok import og

logger = Logger.get_logger(__name__)


class Globals(QObject):
    refreshed_signal = Signal(object)
    refresh_signal = Signal(object)
    refresh_data_signal = Signal(list)

    def __init__(self, exit_event):
        super().__init__()
        self.my_battle_logs = None
        self.meng_battle_logs = None
        self.handler = Handler(exit_event, 'my_app')


    def after_auth(self):
        # self.custom_data = json_string_to_dict(og.auth_custom_str)
        # self.show_export_table_to_excel = self.custom_data.get('show_export_table_to_excel')
        # if self.meng_battle_logs is None:
        #     self.meng_battle_logs = self.deserialize_from_file("tm.dat")
        #     self.refresh_signal.emit(self.tong_meng_stats)
        #     self.refresh_signal.emit(self.di_meng_stats)
        #     logger.info(f'successfully loaded tm.dat {len(self.meng_battle_logs)}')
        # if self.my_battle_logs is None:
        #     self.my_battle_logs = self.deserialize_from_file("my.dat")
        #     self.refresh_signal.emit(self.my_stats)
        #     logger.info(f'successfully loaded my.dat {len(self.my_battle_logs)}')
        pass



def md5_string(input_string):
    md5_hash = hashlib.md5()
    md5_hash.update(input_string.encode('utf-8'))
    return md5_hash.hexdigest()


import json


def json_string_to_dict(json_string):
    try:
        if json_string:
            dictionary = json.loads(json_string)
            return dictionary
        else:
            return {}
    except (ValueError, TypeError):
        return {}
