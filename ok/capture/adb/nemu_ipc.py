import ctypes
import json
import os
import sys
import time
from functools import wraps

import cv2
import numpy as np

from ok import Logger
from ok.capture.adb.nemu_utils import retry_sleep, RETRY_TRIES

logger = Logger.get_logger(__name__)


class NemuIpcIncompatible(Exception):
    pass


class NemuIpcError(Exception):
    pass


def retry(func):
    @wraps(func)
    def retry_wrapper(self, *args, **kwargs):
        """
        Args:
            self (NemuIpcImpl):
        """
        init = None
        for _ in range(RETRY_TRIES):
            # Extend timeout on retries
            if func.__name__ == 'screenshot':
                timeout = retry_sleep(_)
                if timeout > 0:
                    kwargs['timeout'] = timeout
            try:
                if callable(init):
                    time.sleep(retry_sleep(_))
                    init()
                return func(self, *args, **kwargs)
            # Can't handle
            except NemuIpcIncompatible as e:
                logger.error(e)
                break
            # NemuIpcError
            except NemuIpcError as e:
                logger.error(e)

                def init():
                    self.reconnect()
            # Unknown, probably a trucked image
            except Exception as e:
                logger.error("nemu capture error", e)

                def init():
                    pass

        logger.critical(f'Retry {func.__name__}() failed')
        raise Exception(f'Retry {func.__name__}() failed')

    return retry_wrapper


class NemuIpcImpl:
    def __init__(self, nemu_folder: str, instance_id: int, display_id: int = 0):
        """
        Args:
            nemu_folder: Installation path of MuMu12, e.g. E:/ProgramFiles/MuMuPlayer-12.0
            instance_id: Emulator instance ID, starting from 0
            display_id: Always 0 if keep app alive was disabled
        """
        self.nemu_folder: str = nemu_folder
        self.instance_id: int = instance_id
        self.display_id: int = display_id

        ipc_dll = os.path.abspath(os.path.join(nemu_folder, './shell/sdk/external_renderer_ipc.dll'))
        logger.info(
            f'NemuIpcImpl init, '
            f'nemu_folder={nemu_folder}, '
            f'ipc_dll={ipc_dll}, '
            f'instance_id={instance_id}, '
            f'display_id={display_id}'
        )

        try:
            self.lib = ctypes.CDLL(ipc_dll)
        except OSError as e:
            logger.error(e)
            # OSError: [WinError 126] 找不到指定的模块。
            if not os.path.exists(ipc_dll):
                raise NemuIpcIncompatible(
                    f'ipc_dll={ipc_dll} does not exist, '
                    f'NemuIpc requires MuMu12 version >= 3.8.13, please check your version')
            else:
                raise NemuIpcIncompatible(
                    f'ipc_dll={ipc_dll} exists, but cannot be loaded')
        self.connect_id: int = 0
        self.width = 0
        self.height = 0

    def connect(self, on_thread=True):
        if self.connect_id > 0:
            return

        if on_thread:
            connect_id = self.run_func(
                self.lib.nemu_connect,
                self.nemu_folder, self.instance_id
            )
        else:
            connect_id = self.lib.nemu_connect(self.nemu_folder, self.instance_id)
        if connect_id == 0:
            raise NemuIpcError(
                'Connection failed, please check if nemu_folder is correct and emulator is running'
            )

        self.connect_id = connect_id
        # logger.info(f'NemuIpc connected: {self.connect_id}')

    def disconnect(self):
        if self.connect_id == 0:
            return

        self.run_func(
            self.lib.nemu_disconnect,
            self.connect_id
        )

        # logger.info(f'NemuIpc disconnected: {self.connect_id}')
        self.connect_id = 0

    def reconnect(self):
        self.disconnect()
        self.connect()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    @staticmethod
    def run_func(func, *args, on_thread=True, timeout=0.5):
        """
        Args:
            func: Sync function to call
            *args:
            on_thread: True to run func on a separated thread
            timeout:

        Raises:
            JobTimeout: If function call timeout
            NemuIpcIncompatible:
            NemuIpcError
        """
        # if on_thread:
        #     # nemu_ipc may timeout sometimes, so we run it on a separated thread
        #     job = WORKER_POOL.start_thread_soon(func, *args)
        #     result = job.get_or_kill(timeout)
        # else:

        result = func(*args)

        err = False
        if func.__name__ == '_screenshot':
            pass
        elif func.__name__ == 'nemu_connect':
            if result == 0:
                err = True
        else:
            if result > 0:
                err = True
        # Get to actual error message printed in std
        if err:
            logger.warning(f'Failed to call {func.__name__}, result={result}')

        return result

    def get_resolution(self, on_thread=True):
        """
        Get emulator resolution, `self.width` and `self.height` will be set
        """
        if self.connect_id == 0:
            self.connect()

        width_ptr = ctypes.pointer(ctypes.c_int(0))
        height_ptr = ctypes.pointer(ctypes.c_int(0))
        nullptr = ctypes.POINTER(ctypes.c_int)()

        ret = self.run_func(
            self.lib.nemu_capture_display,
            self.connect_id, self.display_id, 0, width_ptr, height_ptr, nullptr,
            on_thread=on_thread
        )
        if ret > 0:
            raise NemuIpcError('nemu_capture_display failed during get_resolution()')
        self.width = width_ptr.contents.value
        self.height = height_ptr.contents.value

    def _screenshot(self):
        if self.connect_id == 0:
            self.connect(on_thread=False)
        self.get_resolution(on_thread=False)

        width_ptr = ctypes.pointer(ctypes.c_int(self.width))
        height_ptr = ctypes.pointer(ctypes.c_int(self.height))
        length = self.width * self.height * 4
        pixels_pointer = ctypes.pointer((ctypes.c_ubyte * length)())

        ret = self.lib.nemu_capture_display(
            self.connect_id, self.display_id, length, width_ptr, height_ptr, pixels_pointer,
        )
        if ret > 0:
            raise NemuIpcError('nemu_capture_display failed during screenshot()')

        # Return pixels_pointer instead of image to avoid passing image through jobs
        return pixels_pointer

    @retry
    def screenshot(self, timeout=0.5):
        """
        Args:
            timeout: Timout in seconds to call nemu_ipc
                Will be dynamically extended by `@retry`

        Returns:
            np.ndarray: Image array in RGBA color space
                Note that image is upside down
        """
        if self.connect_id == 0:
            self.connect()

        pixels_pointer = self.run_func(self._screenshot, timeout=timeout)

        # image = np.ctypeslib.as_array(pixels_pointer, shape=(self.height, self.width, 4))
        image = np.ctypeslib.as_array(pixels_pointer.contents).reshape((self.height, self.width, 4))

        image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGB)
        cv2.flip(image, 0, dst=image)
        return image

    def convert_xy(self, x, y):
        """
        Convert classic ADB coordinates to Nemu's
        `self.height` must be updated before calling this method

        Returns:
            int, int
        """
        x, y = int(x), int(y)
        x, y = self.height - y, x
        return x, y

    @retry
    def down(self, x, y):
        """
        Contact down, continuous contact down will be considered as swipe
        """
        if self.connect_id == 0:
            self.connect()
        if self.height == 0:
            self.get_resolution()

        x, y = self.convert_xy(x, y)

        ret = self.run_func(
            self.lib.nemu_input_event_touch_down,
            self.connect_id, self.display_id, x, y
        )
        if ret > 0:
            raise NemuIpcError('nemu_input_event_touch_down failed')

    @retry
    def up(self):
        """
        Contact up
        """
        if self.connect_id == 0:
            self.connect()

        ret = self.run_func(
            self.lib.nemu_input_event_touch_up,
            self.connect_id, self.display_id
        )
        if ret > 0:
            raise NemuIpcError('nemu_input_event_touch_up failed')

    @staticmethod
    def serial_to_id(serial: str):
        """
        Predict instance ID from serial
        E.g.
            "127.0.0.1:16384" -> 0
            "127.0.0.1:16416" -> 1
            Port from 16414 to 16418 -> 1

        Returns:
            int: instance_id, or None if failed to predict
        """
        try:
            port = int(serial.split(':')[1])
        except (IndexError, ValueError):
            return None
        index, offset = divmod(port - 16384 + 16, 32)
        offset -= 16
        if 0 <= index < 32 and offset in [-2, -1, 0, 1, 2]:
            return index
        else:
            return None
