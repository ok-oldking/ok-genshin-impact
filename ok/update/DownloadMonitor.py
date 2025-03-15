import re
import threading
import time

from ok import Logger
from ok import get_folder_size, bytes_to_readable_size
from ok.gui.Communicate import communicate

logger = Logger.get_logger(__name__)


class DownloadMonitor(threading.Thread):
    def __init__(self, folder_path, target_size, exit_event):
        super().__init__()
        self.folder_path = folder_path
        self.target_size = target_size
        self.stop_event = threading.Event()
        self.exit_event = exit_event
        self.size_from_log = 0
        self.last_size = 0
        self.size_from_file = 0

    def run(self):
        while not self.stop_event.is_set() and not self.exit_event.is_set():
            self.size_from_file = get_folder_size(self.folder_path)
            if self.last_size != self.size_from_file:
                self.size_from_log = 0
                self.last_size = self.size_from_file
            self.notify()
            time.sleep(1)  # Sleep briefly to avoid busy-waiting

    def notify(self):
        total_size = self.size_from_file + self.size_from_log
        if total_size > self.target_size:
            total_size = self.target_size
        percent = total_size / self.target_size

        communicate.update_download_percent.emit(True, bytes_to_readable_size(total_size),
                                                 bytes_to_readable_size(self.target_size), percent)

    def update_running(self, running):
        if not running:
            self.stop_monitoring()

    def start_monitoring(self):
        logger.info(f'Start monitoring {self.target_size} {bytes_to_readable_size(self.target_size)}')
        communicate.log.connect(self.handle_log)
        communicate.update_running.connect(self.update_running)
        self.size_from_log = 0
        self.last_size = 0
        self.stop_event.clear()
        super().start()  # Call the parent class's start method to start the thread

    def stop_monitoring(self):
        communicate.update_download_percent.emit(False, 0, 0, 0)
        communicate.log.disconnect(self.handle_log)
        communicate.update_running.disconnect(self.update_running)
        self.stop_event.set()

    def handle_log(self, level_no, message):
        match = re.search(r"\((\d+(\.\d+)?\s*[kMGTK]B)\)", message)
        if match:
            size_str = match.group(1)
            self.size_from_log += convert_to_bytes(size_str)


def convert_to_bytes(size_str):
    match = re.match(r"(\d+(\.\d+)?)\s*(kB|MB|GB|KB)", size_str)
    if match:
        size = float(match.group(1))
        unit = match.group(3)
        if unit == "kB":
            return int(size * 1024)
        elif unit == "MB":
            return int(size * 1024 * 1024)
        elif unit == "GB":
            return int(size * 1024 * 1024 * 1024)
        return int(size)
    else:
        return 0
