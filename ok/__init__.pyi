# pyi file generated from ok/ok/__init__.pyx

import ctypes
import logging
import re
import threading
from dataclasses import dataclass, field
from logging.handlers import TimedRotatingFileHandler
from typing import Dict, List, Optional, Union, Tuple

import numpy as np
from PySide6.QtCore import QEvent
from PySide6.QtGui import QIcon
from qfluentwidgets import FluentIcon, MSFluentWindow

from ok.gui.Communicate import communicate
from ok.gui.util.Alert import alert_error, alert_info
from ok.gui.widget.StartLoadingDialog import StartLoadingDialog

BGRA_CHANNEL_COUNT: int
WINDOWS_BUILD_NUMBER: int


class Logger:
    """
    自定义日志记录器类。
    """
    logger: object
    name: str

    def __init__(self, name: str):
        """
        初始化 Logger 实例。

        参数:
            name (str): 记录器的名称。
        """
        ...

    def debug(self, message: object):
        """
        记录一条调试消息。

        参数:
            message (object): 调试消息。
        """
        ...

    def info(self, message: object):
        """
        记录一条信息消息。

        参数:
            message (object): 信息消息。
        """
        ...

    def warning(self, message: object):
        """
        记录一条警告消息。

        参数:
            message (object): 警告消息。
        """
        ...

    def error(self, message: object, exception: Optional[Exception] = ...):
        """
        记录一条错误消息。

        参数:
            message (object): 错误消息。
            exception (Optional[Exception]): 可选的异常对象。
        """
        ...

    def critical(self, message: object):
        """
        记录一条严重错误消息。

        参数:
            message (object): 严重错误消息。
        """
        ...

    @staticmethod
    def call_stack() -> str:
        """
        获取当前调用堆栈的字符串表示形式。

        返回:
            str: 调用堆栈的字符串表示形式。
        """
        ...

    @staticmethod
    def get_logger(name: str) -> "Logger":
        """
        获取指定名称的 Logger 实例。

        参数:
            name (str): 记录器的名称。

        返回:
            Logger: Logger 实例。
        """
        ...

    @staticmethod
    def exception_to_str(exception: Exception) -> str:
        """
        将异常对象转换为字符串表示形式。

        参数:
            exception (Exception): 异常对象。

        返回:
            str: 异常的字符串表示形式。
        """
        ...


def config_logger(config: Optional[dict] = ..., name: str = ...):
    """
    配置应用程序的日志记录器。

    参数:
        config (Optional[dict]): 可选的配置字典。
        name (str): 日志文件的名称。
    """
    ...


class SafeFileHandler(TimedRotatingFileHandler):
    """
    安全的定时旋转文件处理程序。
    """
    ...


def init_class_by_name(module_name, class_name, *args, **kwargs):
    """
    根据模块名和类名初始化类。
    """
    ...


class ExitEvent(threading.Event):
    """
    退出事件类，用于协调线程和队列的退出。
    """
    queues: set
    to_stops: set

    def bind_queue(self, queue):
        """
        绑定一个队列到退出事件。

        参数:
            queue: 要绑定的队列。
        """
        ...

    def bind_stop(self, to_stop):
        """
        绑定一个具有 stop() 方法的对象到退出事件。

        参数:
            to_stop: 要绑定的对象。
        """
        ...

    def set(self):
        """
        设置退出事件，通知所有绑定的队列和对象。
        """
        ...


@dataclass(order=True)
class ScheduledTask:
    """
    计划任务的数据类。
    """
    execute_at: float
    task: callable = field(compare=False)


class Handler:
    """
    任务处理器，用于在单独线程中处理计划任务。
    """

    def __init__(self, event: ExitEvent, name: Optional[str] = ...):
        """
        初始化 Handler 实例。

        参数:
            event (ExitEvent): 退出事件。
            name (Optional[str]): 处理器的名称。
        """
        ...

    def post(self, task, delay: float = ..., remove_existing: bool = ..., skip_if_running: bool = ...):
        """
        发布一个任务到处理器的队列。

        参数:
            task: 要执行的任务（可调用对象）。
            delay (float): 任务延迟执行的时间（秒）。
            remove_existing (bool): 是否移除队列中已存在的相同任务。
            skip_if_running (bool): 如果任务正在运行，是否跳过。

        返回:
            bool: 如果任务成功发布，返回 True。
        """
        ...

    def stop(self):
        """
        停止处理器线程。
        """
        ...


def read_json_file(file_path) -> dict | None:
    """
    读取 JSON 文件内容。

    参数:
        file_path (str): JSON 文件的路径。

    返回:
        dict | None: JSON 文件内容的字典表示，如果文件不存在或解析失败则返回 None。
    """
    ...


def write_json_file(file_path, data):
    """
    将数据写入 JSON 文件。

    参数:
        file_path (str): JSON 文件的路径。
        data: 要写入的数据。

    返回:
        bool: 写入成功返回 True。
    """
    ...


def is_admin() -> bool:
    """
    检查当前用户是否为管理员。

报告:
        bool: 如果是管理员返回 True，否则返回 False。
    """
    ...


def get_first_item(lst, default=None):
    """
    获取列表的第一个元素。

    参数:
        lst: 列表。
        default: 如果列表为空，返回的默认值。

    返回:
        列表的第一个元素或默认值。
    """
    ...


def safe_get(lst, idx, default=None):
    """
    安全地获取列表指定索引的元素。

    参数:
        lst: 列表。
        idx (int): 索引。
        default: 如果索引超出范围，返回的默认值。

    返回:
        列表指定索引的元素或默认值。
    """
    ...


def find_index_in_list(my_list, target_string, default_index: int = ...):
    """
    在列表中查找目标字符串的索引。

    参数:
        my_list: 列表。
        target_string (str): 要查找的目标字符串。
        default_index (int): 如果未找到，返回的默认索引。

    返回:
        目标字符串的索引或默认索引。
    """
    ...


def get_path_relative_to_exe(*files) -> str:
    """
    获取相对于可执行文件目录的路径。

    参数:
        *files: 要连接的文件路径或目录。

    返回:
        str: 绝对路径。
    """
    ...


def get_relative_path(*files) -> str:
    """
    获取相对于当前工作目录的路径。

    参数:
        *files: 要连接的文件路径或目录。

    返回:
        str: 绝对路径。
    """
    ...


def install_path_isascii() -> tuple[bool, str]:
    """
    检查安装路径是否只包含 ASCII 字符。

    返回:
        tuple[bool, str]: 一个元组，包含是否为 ASCII 路径和安装路径。
    """
    ...


def resource_path(relative_path):
    """
    获取资源的绝对路径，适用于开发和 PyInstaller 打包。

    参数:
        relative_path (str): 相对于资源目录的路径。

    返回:
        str: 资源的绝对路径。
    """
    ...


def ensure_dir_for_file(file_path) -> str:
    """
    确保文件所在的目录存在。

    参数:
        file_path (str): 文件的路径。

    返回:
        str: 目录的路径。
    """
    ...


def ensure_dir(directory, clear: bool = ...) -> str:
    """
    确保目录存在，如果需要则创建。

    参数:
        directory (str): 要确保存在的目录。
        clear (bool): 如果目录已存在，是否清空目录内容。

    返回:
        str: 目录的路径。
    """
    ...


def delete_if_exists(file_path):
    """
    如果文件或目录存在则删除。

    参数:
        file_path (str): 要删除的文件或目录路径。
    """
    ...


def delete_folders_starts_with(path, starts_with):
    """
    删除指定路径下以特定字符串开头的文件夹。

    参数:
        path (str): 搜索文件夹的根目录。
        starts_with (str): 文件夹名前缀。
    """
    ...


def handle_remove_error(func, path, exc_info):
    """
    处理删除文件或目录时的错误。
    """
    ...


def sanitize_filename(filename) -> str:
    """
    清理文件名中的非法字符。

    参数:
        filename (str): 原始文件名。

    返回:
        str: 清理后的文件名。
    """
    ...


def clear_folder(folder_path):
    """
    清空指定文件夹的内容。

    参数:
        folder_path (str): 要清空的文件夹路径。
    """
    ...


def find_first_existing_file(filenames, directory):
    """
    在指定目录下查找存在的第一个文件。

    参数:
        filenames (list): 文件名列表。
        directory (str): 搜索目录。

    返回:
        str | None: 存在的第一个文件的完整路径，如果未找到则返回 None。
    """
    ...


def get_path_in_package(base, file):
    """
    获取包内文件的路径。

    参数:
        base: 基准文件路径。
        file (str): 要获取路径的文件名。

    返回:
        str: 包内文件的完整路径。
    """
    ...


def dir_checksum(directory, excludes: Optional[list] = ...):
    """
    计算目录内容的 MD5 校验和。

    参数:
        directory (str): 要计算校验和的目录。
        excludes (Optional[list]): 要排除的文件名列表。

    返回:
        str: 目录内容的 MD5 校验和。
    """
    ...


def find_folder_with_file(root_folder, target_file):
    """
    在根文件夹及其子文件夹中查找包含特定文件的文件夹。

    参数:
        root_folder (str): 根文件夹。
        target_file (str): 目标文件名。

    返回:
        str | None: 包含目标文件的文件夹路径，如果未找到则返回 None。
    """
    ...


def get_folder_size(folder_path) -> int:
    """
    计算文件夹的总大小（字节）。

    参数:
        folder_path (str): 文件夹路径。

    返回:
        int: 文件夹的总大小（字节）。
    """
    ...


def run_in_new_thread(func) -> threading.Thread:
    """
    在新的线程中运行函数。

    参数:
        func: 要运行的函数。

    返回:
        threading.Thread: 新创建的线程对象。
    """
    ...


def check_mutex() -> bool:
    """
    检查是否已存在应用程序的互斥锁。

    返回:
        bool: 如果成功创建互斥锁或互斥锁已存在且已处理，则返回 True。
    """
    ...


def all_pids() -> list[int]:
    """
    获取系统中所有进程的 PID 列表。

    返回:
        list[int]: 所有进程的 PID 列表。
    """
    ...


class UNICODE_STRING(ctypes.Structure):
    """
    UNICODE_STRING 结构体。
    """
    ...


class SYSTEM_PROCESS_ID_INFORMATION(ctypes.Structure):
    """
    SYSTEM_PROCESS_ID_INFORMATION 结构体。
    """
    ...


def ratio_text_to_number(supported_ratio) -> float:
    """
    将比例文本（如 "16:9"）转换为浮点数。

    参数:
        supported_ratio (str): 比例文本。

    返回:
        float: 比例的浮点数表示。
    """
    ...


def data_to_base64(data: Union[Dict, List[Dict]]) -> str:
    """
    将字典或字典列表序列化为 base64 编码字符串。

    参数:
        data (Union[Dict, List[Dict]]): 要序列化的数据。

    返回:
        str: base64 编码字符串。
    """
    ...


def base64_to_data(base64_str: str) -> Union[Dict, List[Dict]]:
    """
    将 base64 编码字符串反序列化为字典或字典列表。

    参数:
        base64_str (str): base64 编码字符串。

    返回:
        Union[Dict, List[Dict]]: 反序列化的数据。
    """
    ...


def get_readable_file_size(file_path) -> str:
    """
    计算文件的可读大小。

    参数:
        file_path (str): 文件路径。

    返回:
        str: 可读文件大小（例如，“1.23 MB”）。
    """
    ...


def bytes_to_readable_size(size_bytes) -> str:
    """
    将字节转换为人类可读的大小。

    参数:
        size_bytes (int): 大小（字节）。

    返回:
        str: 人类可读的大小。
    """
    ...


def execute(game_cmd: str) -> bool:
    """
    执行外部命令。

    参数:
        game_cmd (str): 要执行的命令。

    返回:
        bool: 如果成功执行返回 True，否则返回 False。
    """
    ...


def get_path(input_string):
    """
    从输入字符串中提取路径部分。

    参数:
        input_string (str): 包含路径和可选参数的字符串。

    返回:
        str | None: 路径部分，如果无法提取则返回 None。
    """
    ...


class Box:
    """
    表示图像中的一个矩形区域。
    """
    x: int
    y: int
    width: int
    height: int
    confidence: float
    name: str

    def __init__(self, x, y, width: int = ..., height: int = ..., confidence: float = ..., name: Optional[object] = ...,
                 to_x: int = ..., to_y: int = ...):
        """
        初始化 Box 实例。

        参数:
            x (int): 矩形左上角的 x 坐标。
            y (int): 矩形左上角的 y 坐标。
            width (int): 矩形的宽度。
            height (int): 矩形的高度。
            confidence (float): 匹配或识别的置信度。
            name (Optional[object]): 矩形的名称或标识符。
            to_x (int): 矩形右下角的 x 坐标（如果提供，将计算宽度）。
            to_y (int): 矩形右下角的 y 坐标（如果提供，将计算高度）。
        """
        ...

    def in_boundary(self, boxes) -> list["Box"]:
        """
        查找边界框中包含的框。

        参数:
            boxes (list[Box]): 要检查的框列表。

        返回:
            list[Box]: 包含在边界框中的框列表。
        """
        ...

    def scale(self, width_ratio: float, height_ratio: Optional[float] = ...):
        """
        按给定的宽度和高度比例缩放框，保持中心点不变。

        参数:
            width_ratio (float): 宽度缩放比例。
            height_ratio (Optional[float]): 高度缩放比例，如果为 None 则使用 width_ratio。

        返回:
            Box: 新的缩放后的 Box 对象。
        """
        ...

    def closest_distance(self, other: "Box") -> float:
        """
        计算当前框与另一个框之间的最近距离。

        参数:
            other (Box): 另一个 Box 对象。

        返回:
            float: 最近距离。
        """
        ...

    def center_distance(self, other) -> float:
        """
        计算当前框与另一个框中心点之间的距离。

        参数:
            other: 另一个 Box 对象。

        返回:
            float: 中心点之间的距离。
        """
        ...

    def relative_with_variance(self, relative_x: float = ..., relative_y: float = ...):
        """
        计算框内具有随机方差的相对坐标。

        参数:
            relative_x (float): 相对 x 坐标（0.0 到 1.0）。
            relative_y (float): 相对 y 坐标（0.0 到 1.0）。

        返回:
            tuple[int, int]: 计算后的像素坐标 (x, y)。
        """
        ...

    def copy(self, x_offset: int = ..., y_offset: int = ..., width_offset: int = ..., height_offset: int = ...,
             name: Optional[object] = ...):
        """
        创建一个带有偏移量和可选新名称的 Box 副本。

        参数:
            x_offset (int): x 坐标偏移量。
            y_offset (int): y 坐标偏移量。
            width_offset (int): 宽度偏移量。
            height_offset (int): 高度偏移量。
            name (Optional[object]): 新的名称。

        返回:
            Box: 新的 Box 对象。
        """
        ...

    def crop_frame(self, frame):
        """
        根据当前框裁剪图像帧。

        参数:
            frame: 要裁剪的图像帧。

        返回:
            裁剪后的图像帧。
        """
        ...

    def center(self) -> tuple[int, int]:
        """
        计算框的中心点坐标。

        返回:
            tuple[int, int]: 中心点坐标 (x, y)。
        """
        ...

    def find_closest_box(self, direction: str, boxes: list["Box"], condition: Optional[callable] = ...):
        """
        在给定的方向上查找最接近当前框的框。

        参数:
            direction (str): 搜索方向 ('up', 'down', 'left', 'right', 'all')。
            boxes (list[Box]): 要搜索的框列表。
            condition (Optional[callable]): 可选的条件函数，用于过滤框。

        返回:
            Box | None: 最接近的 Box 对象，如果未找到则返回 None。
        """
        ...


def box_intersect(box1: Box, box2: Box) -> bool:
    """
    检查两个框是否相交。

    参数:
        box1 (Box): 第一个 Box 对象。
        box2 (Box): 第二个 Box 对象。

    返回:
        bool: 如果相交返回 True，否则返回 False。
    """
    ...


def compare_boxes(box1: Box, box2: Box) -> int:
    """
    比较两个框，用于排序。

    参数:
        box1 (Box): 第一个 Box 对象。
        box2 (Box): 第二个 Box 对象。

    返回:
        int: 比较结果。
    """
    ...


def find_highest_confidence_box(boxes: list[Box]) -> Box | None:
    """
    在框列表中查找置信度最高的框。

    参数:
        boxes (list[Box]): 框列表。

    返回:
        Box | None: 置信度最高的 Box 对象，如果列表为空则返回 None。
    """
    ...


def sort_boxes(boxes: list[Box]) -> list[Box]:
    """
    根据位置和置信度对框列表进行排序。

    参数:
        boxes (list[Box]): 要排序的框列表。

    返回:
        list[Box]: 排序后的框列表。
    """
    ...


def find_box_by_name(boxes: list[Box], names: object) -> Box | None:
    """
    在框列表中按名称查找框。

    参数:
        boxes (list[Box]): 框列表。
        names (str | re.Pattern | list[str | re.Pattern]): 要匹配的名称或正则表达式模式。

    返回:
        Box | None: 找到的第一个匹配的 Box 对象，如果未找到则返回 None。
    """
    ...


def get_bounding_box(boxes: list[Box]) -> Box:
    """
    计算框列表的最小边界框。

    参数:
        boxes (list[Box]): 框列表。

    返回:
        Box: 边界框。

    引发:
        ValueError: 如果框列表为空。
    """
    ...


def find_boxes_within_boundary(boxes: list[Box], boundary_box: Box, sort: bool = ...) -> list[Box]:
    """
    查找边界框内包含的框。

    参数:
        boxes (list[Box]): 要检查的框列表。
        boundary_box (Box): 边界框。
        sort (bool): 是否对结果进行排序。

    返回:
        list[Box]: 包含在边界框中的框列表。
    """
    ...


def average_width(boxes: list[Box]) -> int:
    """
    计算框列表的平均宽度。

    参数:
        boxes (list[Box]): 框列表。

    返回:
        int: 平均宽度，如果列表为空则返回 0。
    """
    ...


def crop_image(image: object, box: Optional[Box] = ...) -> object:
    """
    根据 Box 对象裁剪图像。

    参数:
        image (object): 要裁剪的图像。
        box (Optional[Box]): Box 对象，如果为 None 则返回原始图像。

    返回:
        object: 裁剪后的图像。
    """
    ...


def relative_box(frame_width, frame_height, x, y, to_x: float = ..., to_y: float = ..., width: float = ...,
                 height: float = ..., name: Optional[object] = ..., confidence: float = ...) -> Box:
    """
    创建相对于帧尺寸的 Box 对象。

    参数:
        frame_width (int): 帧宽度。
        frame_height (int): 帧高度。
        x (float): 相对于帧宽度的 x 坐标。
        y (float): 相对于帧高度的 y 坐标。
        to_x (float): 相对于帧宽度的右下角 x 坐标（如果提供，将计算宽度）。
        to_y (float): 相对于帧高度的右下角 y 坐标（如果提供，将计算高度）。
        width (float): 相对于帧宽度的宽度（如果 to_x 未提供）。
        height (float): 相对于帧高度的高度（如果 to_y 未提供）。
        name (Optional[object]): Box 名称。
        confidence (float): Box 置信度。

    返回:
        Box: 创建的 Box 对象。
    """
    ...


def find_boxes_by_name(boxes: list[Box], names: Union[str, re.Pattern, List[Union[str, re.Pattern]]]) -> list[Box]:
    """
    在框列表中按名称查找所有匹配的框。

    参数:
        boxes (list[Box]): 框列表。
        names (str | re.Pattern | list[str | re.Pattern]): 要匹配的名称或正则表达式模式。

    返回:
        list[Box]: 所有匹配的 Box 对象列表。
    """
    ...


# Color.py

black_color: dict
white_color: dict


def is_close_to_pure_color(image: object, max_colors: int = ..., percent: float = ...) -> bool:
    """
    检查图像是否接近纯色。

    参数:
        image (object): 输入图像。
        max_colors (int): 最大允许颜色数量。
        percent (float): 纯色像素的最小百分比。

    返回:
        bool: 如果图像接近纯色返回 True，否则返回 False。
    """
    ...


def get_mask_in_color_range(image: object, color_range: dict) -> tuple[object, int]:
    """
    根据颜色范围获取图像掩码。

    参数:
        image (object): 输入图像。
        color_range (dict): 颜色范围字典，如 {'r': (0, 100), 'g': (0, 100), 'b': (0, 100)}。

    返回:
        tuple[object, int]: 掩码图像和匹配像素数量。
    """
    ...


def get_connected_area_by_color(image: object, color_range: dict, connectivity: int = ..., gray_range: int = ...) -> \
        tuple[int, object, object, object]:
    """
    根据颜色范围获取图像中的连通区域。

    参数:
        image (object): 输入图像。
        color_range (dict): 颜色范围字典。
        connectivity (int): 连通性（4 或 8）。
        gray_range (int): 灰度范围。

    返回:
        tuple[int, object, object, object]: 连通区域数量、标签、统计信息和中心点。
    """
    ...


def color_range_to_bound(color_range: dict) -> tuple[object, object]:
    """
    将颜色范围字典转换为 NumPy 数组表示的下界和上界。

    参数:
        color_range (dict): 颜色范围字典。

    返回:
        tuple[object, object]: 下界和上界 NumPy 数组。
    """
    ...


def calculate_colorfulness(image: object, box: Optional[Box] = ...) -> float:
    """
    计算图像或图像区域的色彩丰富度。

    参数:
        image (object): 输入图像。
        box (Optional[Box]): 可选的 Box 对象，指定要计算的区域。

    返回:
        float: 色彩丰富度得分。
    """
    ...


def get_saturation(image: object, box: Optional[Box] = ...) -> float:
    """
    计算图像或图像区域的平均饱和度。

    参数:
        image (object): 输入图像。
        box (Optional[Box]): 可选的 Box 对象，指定要计算的区域。

    返回:
        float: 平均饱和度得分（0.0 到 1.0）。
    """
    ...


def find_color_rectangles(image: object, color_range: dict, min_width: int, min_height: int, max_width: int = ...,
                          max_height: int = ..., threshold: float = ..., box: Optional[Box] = ...) -> list[Box]:
    """
    在图像中查找符合颜色范围和尺寸条件的矩形区域。

    参数:
        image (object): 输入图像。
        color_range (dict): 颜色范围字典。
        min_width (int): 最小宽度。
        min_height (int): 最小高度。
        max_width (int): 最大宽度。
        max_height (int): 最大高度。
        threshold (float): 颜色匹配的像素百分比阈值。
        box (Optional[Box]): 可选的 Box 对象，指定搜索区域。

    返回:
        list[Box]: 找到的符合条件的 Box 对象列表。
    """
    ...


def is_pure_black(frame: object) -> bool:
    """
    检查图像帧是否为纯黑色。

    参数:
        frame (object): 输入图像帧。

    返回:
        bool: 如果是纯黑色返回 True，否则返回 False。
    """
    ...


def calculate_color_percentage(image: object, color_ranges: dict, box: Optional[Box] = ...) -> float:
    """
    计算图像或图像区域中指定颜色范围内的像素百分比。

    参数:
        image (object): 输入图像。
        color_ranges (dict): 颜色范围字典。
        box (Optional[Box]): 可选的 Box 对象，指定要计算的区域。

    返回:
        float: 像素百分比。
    """
    ...


def rgb_to_gray(rgb: object) -> float:
    """
    将 RGB 颜色转换为灰度值。

    参数:
        rgb (object): RGB 颜色值（元组或列表）。

    返回:
        float: 灰度值。
    """
    ...


def create_non_black_mask(image):
    """
    创建非黑色像素的二进制掩码。

    参数:
        image: 输入图像（NumPy 数组，BGR 或灰度）。

    返回:
        NumPy 数组: 二进制掩码（uint8 类型，非黑色为 255，黑色为 0）。
    """
    ...


class CommunicateHandler(logging.Handler):
    """
    将日志消息通过信号发送的日志处理程序。
    """
    ...


class App:
    """
    应用程序核心类，管理 UI、任务执行器和配置。
    """
    global_config: object
    app: object
    ok_config: object
    auth_config: object
    locale: object
    overlay: object
    start_controller: object
    loading_window: object
    overlay_window: object
    main_window: object
    exit_event: object
    icon: object
    fire_base_analytics: object
    to_translate: object
    po_translation: object
    updater: object
    config: dict
    about: str
    title: str
    version: str
    debug: bool

    def __init__(self, config: dict, task_executor: Optional["TaskExecutor"], exit_event: Optional[ExitEvent] = ...):
        """
        初始化 App 实例。

        参数:
            config (dict): 应用程序配置字典。
            task_executor (Optional[TaskExecutor]): 可选的任务执行器。
            exit_event (Optional[ExitEvent]): 可选的退出事件。
        """
        ...

    def check_auth(self, key: Optional[str] = ..., uid: str = ...) -> tuple[bool, Optional["Response"]]:
        """
        检查应用程序授权。

        参数:
            key (Optional[str]): 授权密钥。
            uid (str): 用户 ID。

        返回:
            tuple[bool, Optional[Response]]: 一个元组，包含授权是否成功和响应对象。
        """
        ...

    def trial(self) -> tuple[bool, Optional[Union["Response", str]]]:
        """
        进行试用授权。

        返回:
            tuple[bool, Optional[Union[Response, str]]]: 一个元组，包含试用是否成功和响应对象或错误消息。
        """
        ...

    def quit(self):
        """
        退出应用程序。
        """
        ...

    def tr(self, key: str) -> str:
        """
        翻译给定的字符串。

        参数:
            key (str): 要翻译的字符串键。

        返回:
            str: 翻译后的字符串。
        """
        ...

    def request(self, path: str, params: dict) -> "Response":
        """
        向服务器发送请求。

        参数:
            path (str): 请求路径。
            params (dict): 请求参数。

        返回:
            Response: 服务器响应对象。
        """
        ...

    def gen_tr_po_files(self):
        """
        生成翻译 PO 文件。
        """
        ...

    def show_message_window(self, title, message):
        """
        显示消息窗口。

        参数:
            title (str): 窗口标题。
            message (str): 窗口消息。
        """
        ...

    def show_already_running_error(self):
        """
        显示应用程序已在运行的错误消息。
        """
        ...

    def show_path_ascii_error(self, path):
        """
        显示安装路径包含非 ASCII 字符的错误消息。

        参数:
            path (str): 安装路径。
        """
        ...

    def update_overlay(self, visible, x, y, window_width, window_height, width, height, scaling):
        """
        更新覆盖层窗口的位置和大小。

        参数:
            visible (bool): 覆盖层是否可见。
            x (int): 覆盖层 x 坐标。
            y (int): 覆盖层 y 坐标。
            window_width (int): 窗口宽度。
            window_height (int): 窗口高度。
            width (int): 覆盖层宽度。
            height (int): 覆盖层高度。
            scaling (float): 屏幕缩放比例。
        """
        ...

    def show_main_window(self):
        """
        显示主窗口。
        """
        ...

    def do_show_main(self):
        """
        实际显示主窗口。
        """
        ...

    def exec(self):
        """
        启动应用程序事件循环。
        """
        ...


def get_my_id() -> str:
    """
    获取基于 MAC 地址的唯一 ID。

    返回:
        str: 唯一 ID。
    """
    ...


def get_my_id_with_cwd() -> str:
    """
    获取基于 MAC 地址和当前工作目录的唯一 ID。

    返回:
        str: 唯一 ID。
    """
    ...


k: Optional[object] = ...


class Response:
    """
    服务器响应对象。
    """
    code: int
    message: str
    data: object


def r(path: str, params: dict) -> Response:
    """
    向服务器发送请求并获取响应。

    参数:
        path (str): 请求路径。
        params (dict): 请求参数。

    返回:
        Response: 服务器响应对象。
    """
    ...


def d(data: bytes) -> bytes:
    """
    解密数据。

    参数:
        data (bytes): 要解密的数据。

    返回:
        bytes: 解密后的数据。
    """
    ...


public_key: Optional[object] = ...


def e(data: bytes) -> bytes:
    """
    加密数据。

    参数:
        data (bytes): 要加密的数据。

    返回:
        bytes: 加密后的数据。
    """
    ...


# OK.pyx

class OK:
    """
    应用程序主类，管理任务执行和设备。
    """
    executor: Optional["TaskExecutor"]
    adb: Optional[object]
    adb_device: Optional[object]
    feature_set: Optional["FeatureSet"]
    hwnd: Optional[int]
    device_manager: Optional["DeviceManager"]
    ocr: Optional["OCR"]
    overlay_window: Optional[object]
    app: Optional[App]
    screenshot: Optional[object]
    exit_event: ExitEvent
    init_error: Optional[Exception]

    def __init__(self, config: dict):
        """
        初始化 OK 实例。

        参数:
            config (dict): 应用程序配置字典。
        """
        ...

    @property
    def app(self) -> App:
        """
        获取应用程序实例。

        返回:
            App: 应用程序实例。
        """
        ...

    def start(self):
        """
        启动应用程序。
        """
        ...

    def do_init(self) -> bool:
        """
        执行应用程序初始化。

        返回:
            bool: 如果初始化成功返回 True，否则返回 False。
        """
        ...

    def wait_task(self):
        """
        等待任务执行完成。
        """
        ...

    def console_handler(self, event):
        """
        处理控制台事件。
        """
        ...

    def quit(self):
        """
        退出应用程序。
        """
        ...

    def init_device_manager(self):
        """
        初始化设备管理器。
        """
        ...


class BaseScene:
    """
    基础场景类。
    """

    def reset(self):
        """
        重置场景状态。
        """
        ...


# Task.pyx

class BaseTask(OCR):
    """
    基础任务类。
    """
    name: str
    description: str
    _enabled: bool
    config: Config
    info: object
    default_config: dict
    config_description: dict
    config_type: dict
    _paused: bool
    lock: object
    _handler: object
    running: bool
    exit_after_task: bool
    trigger_interval: bool
    last_trigger_time: float
    start_time: float
    icon: object

    def __init__(self, executor: Optional["TaskExecutor"] = ...):
        """
        初始化 BaseTask 实例。

        参数:
            executor (Optional[TaskExecutor]): 可选的任务执行器。
        """
        ...

    def create_shortcut(self):
        """
        为任务创建快捷方式。
        """
        ...

    def tr(self, message):
        """
        翻译任务消息。
        """
        ...

    def should_trigger(self) -> bool:
        """
        检查任务是否应该触发。

        返回:
            bool: 如果应该触发返回 True，否则返回 False。
        """
        ...

    def is_custom(self) -> bool:
        """
        检查任务是否为自定义任务。

        返回:
            bool: 如果是自定义任务返回 True，否则返回 False。
        """
        ...

    def add_first_run_alert(self, first_run_alert):
        """
        添加首次运行提示。
        """
        ...

    def add_exit_after_config(self):
        """
        添加任务完成后退出的配置选项。
        """
        ...

    def get_status(self) -> str:
        """
        获取任务的当前状态。

        返回:
            str: 任务状态字符串。
        """
        ...

    def enable(self):
        """
        启用任务。
        """
        ...

    @property
    def handler(self) -> Handler:
        """
        获取任务的处理程序。

        返回:
            Handler: 任务的处理程序。
        """
        ...

    def pause(self):
        """
        暂停任务。
        """
        ...

    def unpause(self):
        """
        取消暂停任务。
        """
        ...

    @property
    def paused(self) -> bool:
        """
        检查任务是否已暂停。

        返回:
            bool: 如果已暂停返回 True，否则返回 False。
        """
        ...

    def log_info(self, message, notify: bool = ...):
        """
        记录信息日志。
        """
        ...

    def log_debug(self, message, notify: bool = ...):
        """
        记录调试日志。
        """
        ...

    def log_error(self, message, exception: Optional[Exception] = ..., notify: bool = ...):
        """
        记录错误日志。
        """
        ...

    def notification(self, message, title: Optional[str] = ..., error: bool = ..., tray: bool = ...,
                     show_tab: Optional[str] = ...):
        """
        发送应用程序通知。
        """
        ...

    @property
    def enabled(self) -> bool:
        """
        检查任务是否已启用。

        返回:
            bool: 如果已启用返回 True，否则返回 False。
        """
        ...

    def info_clear(self):
        """
        清空任务信息。
        """
        ...

    def info_incr(self, key, inc: int = ...):
        """
        递增任务信息中的计数。
        """
        ...

    def info_add_to_list(self, key, item):
        """
        将项目添加到任务信息中的列表。
        """
        ...

    def info_set(self, key, value):
        """
        设置任务信息中的键值对。
        """
        ...

    def info_get(self, *args, **kwargs):
        """
        获取任务信息中的值。
        """
        ...

    def info_add(self, key, count: int = ...):
        """
        将计数添加到任务信息中的键。
        """
        ...

    def load_config(self):
        """
        加载任务配置。
        """
        ...

    def validate(self, key, value) -> tuple[bool, Optional[str]]:
        """
        验证配置键值对。
        """
        ...

    def validate_config(self, key, value):
        """
        验证任务配置。
        """
        ...

    def disable(self):
        """
        禁用任务。
        """
        ...

    @property
    def hwnd_title(self) -> str:
        """
        获取窗口句柄标题。

        返回:
            str: 窗口句柄标题。
        """
        ...

    def run(self):
        """
        执行任务逻辑。
        """
        ...

    def trigger(self) -> bool:
        """
        检查任务是否应该触发。

        返回:
            bool: 如果应该触发返回 True，否则返回 False。
        """
        ...

    def on_destroy(self):
        """
        任务销毁时执行的清理操作。
        """
        ...

    def on_create(self):
        """
        任务创建时执行的初始化操作。
        """
        ...

    def set_executor(self, executor):
        """
        设置任务的执行器。
        """
        ...

    def find_boxes(self, boxes, match: Optional[object] = ..., boundary: Optional[object] = ...) -> list[Box]:
        """
        在框列表中查找匹配和边界框内的框。

        参数:
            boxes (list[Box]): 框列表。
            match (Optional[object]): 可选的匹配条件。
            boundary (Optional[object]): 可选的边界框。

        返回:
            list[Box]: 过滤后的框列表。
        """
        ...


class TaskDisabledException(Exception):
    """
    任务禁用异常。
    """
    ...


class CannotFindException(Exception):
    """
    未找到异常。
    """
    ...


class FinishedException(Exception):
    """
    完成异常。
    """
    ...


class WaitFailedException(Exception):
    """
    等待失败异常。
    """
    ...


class TaskExecutor:
    """
    任务执行器，管理任务的执行和图像捕获。
    """
    _frame: object
    paused: bool
    pause_start: float
    pause_end_time: float
    _last_frame_time: float
    wait_until_timeout: float
    device_manager: object
    feature_set: object
    wait_until_settle_time: float
    wait_scene_timeout: float
    exit_event: object
    debug_mode: bool
    debug: bool
    global_config: object
    _ocr_lib: dict
    ocr_target_height: int
    current_task: object
    config_folder: str
    trigger_task_index: int
    trigger_tasks: list
    onetime_tasks: list
    thread: object
    locale: object
    scene: object
    text_fix: dict
    ocr_po_translation: object
    config: object
    basic_options: object
    lock: object

    def __init__(self, device_manager: "DeviceManager", wait_until_timeout: float = ...,
                 wait_until_settle_time: float = ..., exit_event: Optional[ExitEvent] = ...,
                 feature_set: Optional["FeatureSet"] = ..., ocr_lib: Optional[dict] = ...,
                 config_folder: Optional[str] = ..., debug: bool = ..., global_config: Optional[GlobalConfig] = ...,
                 ocr_target_height: int = ..., config: Optional[dict] = ...):
        """
        初始化 TaskExecutor 实例。

        参数:
            device_manager (DeviceManager): 设备管理器。
            wait_until_timeout (float): 等待条件超时时间（秒）。
            wait_until_settle_time (float): 等待条件稳定时间（秒）。
            exit_event (Optional[ExitEvent]): 可选的退出事件。
            feature_set (Optional[FeatureSet]): 可选的特征集。
            ocr_lib (Optional[dict]): 可选的 OCR 库配置。
            config_folder (Optional[str]): 配置文件夹路径。
            debug (bool): 是否处于调试模式。
            global_config (Optional[GlobalConfig]): 可选的全局配置。
            ocr_target_height (int): OCR 图像目标高度。
            config (Optional[dict]): 可选的应用程序配置。
        """
        ...

    def load_tr(self):
        """
        加载 OCR 翻译。
        """
        ...

    @property
    def interaction(self) -> "BaseInteraction":
        """
        获取交互对象。

        返回:
            BaseInteraction: 交互对象。
        """
        ...

    @property
    def method(self) -> "BaseCaptureMethod":
        """
        获取图像捕获方法。

        返回:
            BaseCaptureMethod: 图像捕获方法。
        """
        ...

    def ocr_lib(self, name: str = ...):
        """
        获取指定名称的 OCR 库实例。

        参数:
            name (str): OCR 库名称。

        返回:
            OCR 库实例。
        """
        ...

    def nullable_frame(self):
        """
        获取当前图像帧，可能为 None。

        返回:
            np.ndarray | None: 当前图像帧。
        """
        ...

    def check_frame_and_resolution(self, supported_ratio, min_size, time_out: float = ...) -> tuple[bool, str]:
        """
        检查图像帧和分辨率是否符合要求。

        参数:
            supported_ratio (str): 支持的比例字符串。
            min_size (tuple[int, int]): 最小尺寸 (宽度, 高度)。
            time_out (float): 检查超时时间（秒）。

        返回:
            tuple[bool, str]: 一个元组，包含是否支持分辨率和实际分辨率字符串。
        """
        ...

    def can_capture(self) -> bool:
        """
        检查是否可以捕获图像。

        返回:
            bool: 如果可以捕获返回 True，否则返回 False。
        """
        ...

    def next_frame(self):
        """
        获取下一帧图像。

        返回:
            np.ndarray: 下一帧图像。

        引发:
            FinishedException: 如果退出事件已设置。
        """
        ...

    def is_executor_thread(self) -> bool:
        """
        检查当前线程是否为执行器线程。

        返回:
            bool: 如果是执行器线程返回 True，否则返回 False。
        """
        ...

    def connected(self) -> bool:
        """
        检查捕获方法是否已连接。

        返回:
            bool: 如果已连接返回 True，否则返回 False。
        """
        ...

    @property
    def frame(self) -> np.ndarray:
        """
        获取当前图像帧。

        返回:
            np.ndarray: 当前图像帧。

        引发:
            FinishedException: 如果退出事件已设置。
        """
        ...

    def check_enabled(self, check_pause: bool = ...):
        """
        检查当前任务是否已启用。

        参数:
            check_pause (bool): 是否检查暂停状态。

        引发:
            TaskDisabledException: 如果任务已禁用。
        """
        ...

    def sleep(self, timeout: float):
        """
        休眠指定时间，同时检查退出事件。

        参数:
            timeout (float): 休眠时间（秒）。
        """
        ...

    def pause(self, task: Optional[BaseTask] = ...):
        """
        暂停执行器或当前任务。

        参数:
            task (Optional[BaseTask]): 要暂停的任务。

        返回:
            bool: 如果成功暂停返回 True。
        """
        ...

    def stop_current_task(self):
        """
        停止当前正在执行的任务。
        """
        ...

    def start(self):
        """
        启动任务执行器线程。
        """
        ...

    def wait_condition(self, condition: callable, time_out: float = ..., pre_action: Optional[callable] = ...,
                       post_action: Optional[callable] = ..., settle_time: float = ..., raise_if_not_found: bool = ...):
        """
        等待条件满足。

        参数:
            condition (callable): 要等待的条件函数。
            time_out (float): 等待超时时间（秒）。
            pre_action (Optional[callable]): 在检查条件之前执行的动作。
            post_action (Optional[callable]): 在检查条件之后执行的动作。
            settle_time (float): 等待条件稳定时间（秒）。
            raise_if_not_found (bool): 如果超时未找到是否引发异常。

        返回:
            条件函数的结果。

        引发:
            WaitFailedException: 如果 raise_if_not_found 为 True 且超时未找到。
        """
        ...

    def reset_scene(self, check_enabled: bool = ...):
        """
        重置当前场景和图像帧。

        参数:
            check_enabled (bool): 是否检查当前任务是否启用。
        """
        ...

    def next_task(self) -> tuple[Optional[BaseTask], bool, bool]:
        """
        获取下一个要执行的任务。

        返回:
            tuple[Optional[BaseTask], bool, bool]: 一个元组，包含任务对象、是否循环和是否为触发任务。
        """
        ...

    def active_trigger_task_count(self) -> int:
        """
        获取当前活动的触发任务数量。

        返回:
            int: 活动触发任务数量。
        """
        ...

    def trigger_sleep(self):
        """
        触发任务间的休眠。
        """
        ...

    def execute(self):
        """
        执行任务循环。
        """
        ...

    def stop(self):
        """
        停止任务执行器。
        """
        ...

    def wait_until_done(self):
        """
        等待任务执行器线程结束。
        """
        ...

    def get_all_tasks(self) -> list[BaseTask]:
        """
        获取所有任务。

        返回:
            list[BaseTask]: 所有任务列表。
        """
        ...

    def get_task_by_class_name(self, class_name: str) -> Optional[BaseTask]:
        """
        根据类名获取任务。

        参数:
            class_name (str): 任务类名。

        返回:
            Optional[BaseTask]: 任务对象，如果未找到则返回 None。
        """
        ...

    def get_task_by_class(self, cls) -> Optional[BaseTask]:
        """
        根据类获取任务。

        参数:
            cls: 任务类。

        返回:
            Optional[BaseTask]: 任务对象，如果未找到则返回 None。
        """
        ...


def list_or_obj_to_str(val) -> Optional[str]:
    """
    将列表或对象转换为字符串。
    """
    ...


def create_shortcut(exe_path: Optional[str] = ..., shortcut_name_post: Optional[str] = ...,
                    description: Optional[str] = ..., target_path: Optional[str] = ...,
                    arguments: Optional[str] = ...) -> str | bool:
    """
    为可执行文件创建快捷方式。

    参数:
        exe_path (Optional[str]): 可执行文件路径。
        shortcut_name_post (Optional[str]): 快捷方式名称后缀。
        description (Optional[str]): 快捷方式描述。
        target_path (Optional[str]): 快捷方式目标路径。
        arguments (Optional[str]): 快捷方式参数。

    返回:
        str | bool: 快捷方式路径或创建失败返回 False。
    """
    ...


def prevent_sleeping(yes: bool = ...):
    """
    阻止系统进入睡眠状态。

    参数:
        yes (bool): 是否阻止睡眠。
    """
    ...


class ExecutorOperation:
    """
    执行器操作基类，提供与执行器交互的方法。
    """
    last_click_time: float
    _executor: TaskExecutor
    logger: object

    def __init__(self, executor: TaskExecutor):
        """
        初始化 ExecutorOperation 实例。

        参数:
            executor (TaskExecutor): 任务执行器。
        """
        ...

    def exit_is_set(self) -> bool:
        """
        检查退出事件是否已设置。

        返回:
            bool: 如果已设置返回 True，否则返回 False。
        """
        ...

    def box_in_horizontal_center(self, box: Box, off_percent: float = ...) -> bool:
        """
        检查框是否在水平中心。

        参数:
            box (Box): 要检查的框。
            off_percent (float): 允许的偏移百分比。

        返回:
            bool: 如果在水平中心返回 True，否则返回 False。
        """
        ...

    @property
    def executor(self) -> TaskExecutor:
        """
        获取任务执行器。

        返回:
            TaskExecutor: 任务执行器。
        """
        ...

    @property
    def debug(self) -> bool:
        """
        检查是否处于调试模式。

        返回:
            bool: 如果是调试模式返回 True，否则返回 False。
        """
        ...

    def is_scene(self, the_scene) -> bool:
        """
        检查当前场景是否为指定类型。

        参数:
            the_scene: 场景类型。

        返回:
            bool: 如果是指定类型返回 True，否则返回 False。
        """
        ...

    def reset_scene(self):
        """
        重置当前场景。
        """
        ...

    def click(self, x: Union[int, Box, List[Box]] = ..., y: int = ..., move_back: bool = ..., name: Optional[str] = ...,
              interval: float = ..., move: bool = ..., down_time: float = ..., after_sleep: float = ...,
              key: str = ...) -> bool:
        """
        模拟鼠标点击。

        参数:
            x (Union[int, Box, List[Box]]): x 坐标或 Box 对象或 Box 列表。
            y (int): y 坐标。
            move_back (bool): 点击后是否将鼠标移回原位。
            name (Optional[str]): 点击的名称。
            interval (float): 点击间隔时间（秒）。
            move (bool): 是否移动鼠标到点击位置。
            down_time (float): 按下时间（秒）。
            after_sleep (float): 点击后休眠时间（秒）。
            key (str): 鼠标键 ('left', 'middle', 'right')。

        返回:
            bool: 如果成功点击返回 True，否则返回 False。
        """
        ...

    def back(self, *args, **kwargs):
        """
        模拟返回操作。
        """
        ...

    def middle_click(self, *args, **kwargs):
        """
        模拟鼠标中键点击。
        """
        ...

    def right_click(self, *args, **kwargs):
        """
        模拟鼠标右键点击。
        """
        ...

    def check_interval(self, interval: float) -> bool:
        """
        检查是否满足点击间隔。

        参数:
            interval (float): 点击间隔时间（秒）。

        返回:
            bool: 如果满足间隔返回 True，否则返回 False。
        """
        ...

    def is_adb(self) -> bool:
        """
        检查当前设备是否为 ADB 设备。

        返回:
            bool: 如果是 ADB 设备返回 True，否则返回 False。
        """
        ...

    def mouse_down(self, x: int = ..., y: int = ..., name: Optional[str] = ..., key: str = ...):
        """
        模拟鼠标按下。

        参数:
            x (int): x 坐标。
            y (int): y 坐标。
            name (Optional[str]): 按下的名称。
            key (str): 鼠标键 ('left', 'middle', 'right')。
        """
        ...

    def mouse_up(self, name: Optional[str] = ..., key: str = ...):
        """
        模拟鼠标释放。

        参数:
            name (Optional[str]): 释放的名称。
            key (str): 鼠标键 ('left', 'middle', 'right')。
        """
        ...

    def swipe_relative(self, from_x: float, from_y: float, to_x: float, to_y: float, duration: float = ...,
                       settle_time: float = ...):
        """
        模拟相对位置的滑动。

        参数:
            from_x (float): 起始相对 x 坐标。
            from_y (float): 起始相对 y 坐标。
            to_x (float): 结束相对 x 坐标。
            to_y (float): 结束相对 y 坐标。
            duration (float): 滑动持续时间（秒）。
            settle_time (float): 滑动结束后的稳定时间（秒）。
        """
        ...

    def input_text(self, text: str):
        """
        输入文本。

        参数:
            text (str): 要输入的文本。
        """
        ...

    @property
    def hwnd(self):
        """
        获取窗口句柄。

        返回:
            窗口句柄对象。
        """
        ...

    def scroll_relative(self, x: float, y: float, count: int):
        """
        模拟相对位置的滚动。

        参数:
            x (float): 滚动中心相对 x 坐标。
            y (float): 滚动中心相对 y 坐标。
            count (int): 滚动量。
        """
        ...

    def scroll(self, x: int, y: int, count: int):
        """
        模拟滚动。

        参数:
            x (int): 滚动中心 x 坐标。
            y (int): 滚动中心 y 坐标。
            count (int): 滚动量。
        """
        ...

    def swipe(self, from_x: int, from_y: int, to_x: int, to_y: int, duration: float = ..., after_sleep: float = ...,
              settle_time: float = ...):
        """
        模拟滑动。

        参数:
            from_x (int): 起始 x 坐标。
            from_y (int): 起始 y 坐标。
            to_x (int): 结束 x 坐标。
            to_y (int): 结束 y 坐标。
            duration (float): 滑动持续时间（秒）。
            after_sleep (float): 滑动后休眠时间（秒）。
            settle_time (float): 滑动结束后的稳定时间（秒）。
        """
        ...

    def screenshot(self, name: Optional[str] = ..., frame: Optional[object] = ..., show_box: bool = ...,
                   frame_box: Optional[Box] = ...):
        """
        截取屏幕截图。

        参数:
            name (Optional[str]): 截图名称。
            frame (Optional[object]): 要截取的图像帧，如果为 None 则使用当前帧。
            show_box (bool): 是否在截图中显示 Box。
            frame_box (Optional[Box]): 要在截图中显示的 Box。
        """
        ...

    def click_box_if_name_match(self, boxes: list[Box], names: Union[str, list], relative_x: float = ...,
                                relative_y: float = ...):
        """
        如果 Box 名称匹配，则点击 Box。

        参数:
            boxes (list[Box]): Box 列表。
            names (str | list): 要匹配的名称或名称列表。
            relative_x (float): 相对于 Box 宽度的点击位置。
            relative_y (float): 相对于 Box 高度的点击位置。
        """
        ...

    def box_of_screen(self, x, y, to_x: float = ..., to_y: float = ..., width: float = ..., height: float = ...,
                      name: Optional[str] = ..., hcenter: bool = ..., confidence: float = ...) -> Box:
        """
        创建表示屏幕区域的 Box 对象。

        参数:
            x (float): 相对于屏幕宽度的 x 坐标。
            y (float): 相对于屏幕高度的 y 坐标。
            to_x (float): 相对于屏幕宽度的右下角 x 坐标（如果提供，将计算宽度）。
            to_y (float): 相对于屏幕高度的右下角 y 坐标（如果提供，将计算高度）。
            width (float): 相对于屏幕宽度的宽度（如果 to_x 未提供）。
            height (float): 相对于屏幕高度的高度（如果 to_y 未提供）。
            name (Optional[str]): Box 名称。
            hcenter (bool): 是否水平居中。
            confidence (float): Box 置信度。

        返回:
            Box: 创建的 Box 对象。
        """
        ...

    def out_of_ratio(self) -> bool:
        """
        检查当前屏幕比例是否超出支持范围。

        返回:
            bool: 如果超出返回 True，否则返回 False。
        """
        ...

    def ensure_in_front(self):
        """
        确保当前窗口在前台。
        """
        ...

    def box_of_screen_scaled(self, original_screen_width, original_screen_height, x_original, y_original,
                             to_x: int = ..., to_y: int = ..., width_original: int = ..., height_original: int = ...,
                             name: Optional[str] = ..., hcenter: bool = ..., confidence: float = ...) -> Box:
        """
        创建缩放后的表示屏幕区域的 Box 对象。

        参数:
            original_screen_width (int): 原始屏幕宽度。
            original_screen_height (int): 原始屏幕高度。
            x_original (int): 原始 x 坐标。
            y_original (int): 原始 y 坐标。
            to_x (int): 原始右下角 x 坐标（如果提供，将计算宽度）。
            to_y (int): 原始右下角 y 坐标（如果提供，将计算高度）。
            width_original (int): 原始宽度（如果 to_x 未提供）。
            height_original (int): 原始高度（如果 to_y 未提供）。
            name (Optional[str]): Box 名称。
            hcenter (bool): 是否水平居中。
            confidence (float): Box 置信度。

        返回:
            Box: 创建的 Box 对象。
        """
        ...

    def height_of_screen(self, percent: float) -> int:
        """
        计算屏幕高度的百分比像素值。

        参数:
            percent (float): 百分比（0.0 到 1.0）。

        返回:
            int: 像素值。
        """
        ...

    @property
    def screen_width(self) -> int:
        """
        获取屏幕宽度。

        返回:
            int: 屏幕宽度。
        """
        ...

    @property
    def screen_height(self) -> int:
        """
        获取屏幕高度。

        返回:
            int: 屏幕高度。
        """
        ...

    def width_of_screen(self, percent: float) -> int:
        """
        计算屏幕宽度的百分比像素值。

        参数:
            percent (float): 百分比（0.0 到 1.0）。

        返回:
            int: 像素值。
        """
        ...

    def click_relative(self, x: float, y: float, move_back: bool = ..., hcenter: bool = ..., move: bool = ...,
                       after_sleep: float = ..., name: Optional[str] = ..., interval: float = ...,
                       down_time: float = ..., key: str = ...):
        """
        模拟相对位置的鼠标点击。

        参数:
            x (float): 相对于屏幕宽度的 x 坐标。
            y (float): 相对于屏幕高度的 y 坐标。
            move_back (bool): 点击后是否将鼠标移回原位。
            hcenter (bool): 是否水平居中。
            move (bool): 是否移动鼠标到点击位置。
            after_sleep (float): 点击后休眠时间（秒）。
            name (Optional[str]): 点击的名称。
            interval (float): 点击间隔时间（秒）。
            down_time (float): 按下时间（秒）。
            key (str): 鼠标键 ('left', 'middle', 'right')。
        """
        ...

    def middle_click_relative(self, x: float, y: float, move_back: bool = ..., down_time: float = ...):
        """
        模拟相对位置的鼠标中键点击。

        参数:
            x (float): 相对于屏幕宽度的 x 坐标。
            y (float): 相对于屏幕高度的 y 坐标。
            move_back (bool): 点击后是否将鼠标移回原位。
            down_time (float): 按下时间（秒）。
        """
        ...

    @property
    def height(self) -> int:
        """
        获取当前捕获方法的高度。

        返回:
            int: 高度。
        """
        ...

    @property
    def width(self) -> int:
        """
        获取当前捕获方法的宽度。

        返回:
            int: 宽度。
        """
        ...

    def move_relative(self, x: float, y: float):
        """
        模拟相对位置的鼠标移动。

        参数:
            x (float): 相对于屏幕宽度的 x 坐标。
            y (float): 相对于屏幕高度的 y 坐标。
        """
        ...

    def move(self, x: int, y: int):
        """
        模拟鼠标移动。

        参数:
            x (int): x 坐标。
            y (int): y 坐标。
        """
        ...

    def click_box(self, box: Optional[Union[Box, List[Box], str]] = ..., relative_x: float = ...,
                  relative_y: float = ..., raise_if_not_found: bool = ..., move_back: bool = ...,
                  down_time: float = ..., after_sleep: float = ...):
        """
        点击 Box 的相对位置。

        参数:
            box (Optional[Union[Box, List[Box], str]]): Box 对象、Box 列表或 Box 名称。
            relative_x (float): 相对于 Box 宽度的点击位置。
            relative_y (float): 相对于 Box 高度的点击位置。
            raise_if_not_found (bool): 如果未找到 Box 是否引发异常。
            move_back (bool): 点击后是否将鼠标移回原位。
            down_time (float): 按下时间（秒）。
            after_sleep (float): 点击后休眠时间（秒）。

        引发:
            Exception: 如果 raise_if_not_found 为 True 且未找到 Box。
        """
        ...

    def wait_scene(self, scene_type: Optional[object] = ..., time_out: float = ...,
                   pre_action: Optional[callable] = ..., post_action: Optional[callable] = ...):
        """
        等待场景类型满足。

        参数:
            scene_type (Optional[object]): 场景类型。
            time_out (float): 等待超时时间（秒）。
            pre_action (Optional[callable]): 在检查条件之前执行的动作。
            post_action (Optional[callable]): 在检查条件之后执行的动作。
        """
        ...

    def sleep(self, timeout: float) -> bool:
        """
        休眠指定时间。

        参数:
            timeout (float): 休眠时间（秒）。

        返回:
            bool: 始终返回 True。
        """
        ...

    def send_key(self, key, down_time: float = ..., interval: float = ..., after_sleep: float = ...) -> bool:
        """
        发送按键事件。

        参数:
            key: 按键。
            down_time (float): 按下时间（秒）。
            interval (float): 按键间隔时间（秒）。
            after_sleep (float): 按键后休眠时间（秒）。

        返回:
            bool: 如果成功发送返回 True，否则返回 False。
        """
        ...

    def get_global_config(self, option):
        """
        获取全局配置选项的值。

        参数:
            option: 配置选项。
        """
        ...

    def get_global_config_desc(self, option):
        """
        获取全局配置选项的描述。
        """
        ...

    def send_key_down(self, key):
        """
        模拟按下按键。

        参数:
            key: 按键。
        """
        ...

    def send_key_up(self, key):
        """
        模拟释放按键。

        参数:
            key: 按键。
        """
        ...

    def wait_until(self, condition: callable, time_out: float = ..., pre_action: Optional[callable] = ...,
                   post_action: Optional[callable] = ..., settle_time: float = ..., raise_if_not_found: bool = ...):
        """
        等待条件满足。

        参数:
            condition (callable): 要等待的条件函数。
            time_out (float): 等待超时时间（秒）。
            pre_action (Optional[callable]): 在检查条件之前执行的动作。
            post_action (Optional[callable]): 在检查条件之后执行的动作。
            settle_time (float): 等待条件稳定时间（秒）。
            raise_if_not_found (bool): 如果超时未找到是否引发异常。

        返回:
            条件函数的结果。

        引发:
            WaitFailedException: 如果 raise_if_not_found 为 True 且超时未找到。
        """
        ...

    def wait_click_box(self, condition: callable, time_out: float = ..., pre_action: Optional[callable] = ...,
                       post_action: Optional[callable] = ..., raise_if_not_found: bool = ...):
        """
        等待 Box 满足条件并点击。

        参数:
            condition (callable): 返回 Box 对象的条件函数。
            time_out (float): 等待超时时间（秒）。
            pre_action (Optional[callable]): 在检查条件之前执行的动作。
            post_action (Optional[callable]): 在检查条件之后执行的动作。
            raise_if_not_found (bool): 如果超时未找到 Box 是否引发异常。
        """
        ...

    def next_frame(self):
        """
        获取下一帧图像。
        """
        ...

    def adb_ui_dump(self):
        """
        执行 ADB UI Dump。
        """
        ...

    @property
    def frame(self) -> np.ndarray:
        """
        获取当前图像帧。

        返回:
            np.ndarray: 当前图像帧。
        """
        ...

    @staticmethod
    def draw_boxes(feature_name: Optional[str] = ..., boxes: Optional[list[Box] | Box] = ..., color: str = ...):
        """
        绘制 Box。
        """
        ...

    def clear_box(self):
        """
        清除绘制的 Box。
        """
        ...

    def calculate_color_percentage(self, color: dict, box: Union[Box, str]) -> float:
        """
        计算 Box 区域内指定颜色的像素百分比。

        参数:
            color (dict): 颜色范围字典。
            box (Union[Box, str]): Box 对象或 Box 名称。

        返回:
            float: 像素百分比。
        """
        ...

    def adb_shell(self, *args, **kwargs):
        """
        执行 ADB Shell 命令。
        """
        ...


class TriggerTask(BaseTask):
    """
    触发任务类。
    """

    def __init__(self, *args, **kwargs):
        """
        初始化 TriggerTask 实例。
        """
        ...

    def on_create(self):
        """
        触发任务创建时执行的初始化操作。
        """
        ...

    def get_status(self) -> str:
        """
        获取触发任务的当前状态。

        返回:
            str: 触发任务状态字符串。
        """
        ...

    def enable(self):
        """
        启用触发任务。
        """
        ...

    def disable(self):
        """
        禁用触发任务。
        """
        ...


class FindFeature(ExecutorOperation):
    """
    查找特征操作类。
    """

    def __init__(self, executor: TaskExecutor):
        """
        初始化 FindFeature 实例。

        参数:
            executor (TaskExecutor): 任务执行器。
        """
        ...

    def find_feature(self, feature_name: Optional[str] = ..., horizontal_variance: float = ...,
                     vertical_variance: float = ..., threshold: float = ..., use_gray_scale: bool = ..., x: float = ...,
                     y: float = ..., to_x: float = ..., to_y: float = ..., width: float = ..., height: float = ...,
                     box: Optional[Union[Box, str]] = ..., canny_lower: int = ..., canny_higher: int = ...,
                     frame_processor: Optional[callable] = ..., template: Optional[np.ndarray] = ...,
                     match_method: int = ..., screenshot: bool = ..., mask_function: Optional[callable] = ...,
                     frame: Optional[np.ndarray] = ...) -> List[Box]:
        """
        查找图像中的特征。

        参数:
            feature_name (Optional[str]): 特征名称。
            horizontal_variance (float): 水平方差。
            vertical_variance (float): 垂直方差。
            threshold (float): 置信度阈值。
            use_gray_scale (bool): 是否使用灰度图像。
            x (float): 相对于帧宽度的 x 坐标。
            y (float): 相对于帧高度的 y 坐标。
            to_x (float): 相对于帧宽度的右下角 x 坐标。
            to_y (float): 相对于帧高度的右下角 y 坐标。
            width (float): 相对于帧宽度的宽度。
            height (float): 相对于帧高度的高度。
            box (Optional[Union[Box, str]]): 可选的搜索区域 Box 或 Box 名称。
            canny_lower (int): Canny 边缘检测下限阈值。
            canny_higher (int): Canny 边缘检测上限阈值。
            frame_processor (Optional[callable]): 可选的帧处理器函数。
            template (Optional[np.ndarray]): 可选的模板图像。
            match_method (int): 模板匹配方法。
            screenshot (bool): 是否截取截图。
            mask_function (Optional[callable]): 可选的掩码函数。
            frame (Optional[np.ndarray]): 可选的图像帧。

        返回:
            List[Box]: 找到的 Box 对象列表。
        """
        ...

    def get_feature_by_name(self, name: str) -> object:
        """
        根据名称获取特征对象。

        参数:
            name (str): 特征名称。

        返回:
            特征对象。

        引发:
            ValueError: 如果未找到特征。
        """
        ...

    def get_box_by_name(self, name: str) -> Box:
        """
        根据名称获取 Box 对象。

        参数:
            name (str): Box 名称。

        返回:
            Box: Box 对象。

        引发:
            ValueError: 如果未找到 Box。
        """
        ...

    def find_feature_and_set(self, features: Union[str, list], horizontal_variance: float = ...,
                             vertical_variance: float = ..., threshold: float = ...) -> bool:
        """
        查找特征并将其设置为对象的属性。

        参数:
            features (str | list): 要查找的特征名称或名称列表。
            horizontal_variance (float): 水平方差。
            vertical_variance (float): 垂直方差。
            threshold (float): 置信度阈值。

        返回:
            bool: 如果所有特征都找到返回 True，否则返回 False。
        """
        ...

    def wait_feature(self, feature, horizontal_variance: float = ..., vertical_variance: float = ...,
                     threshold: float = ..., time_out: float = ..., pre_action: Optional[callable] = ...,
                     post_action: Optional[callable] = ..., use_gray_scale: bool = ...,
                     box: Optional[Union[Box, str]] = ..., raise_if_not_found: bool = ..., canny_lower: int = ...,
                     canny_higher: int = ..., settle_time: float = ..., frame_processor: Optional[callable] = ...):
        """
        等待特征出现。

        参数:
            feature: 要等待的特征。
            horizontal_variance (float): 水平方差。
            vertical_variance (float): 垂直方差。
            threshold (float): 置信度阈值。
            time_out (float): 等待超时时间（秒）。
            pre_action (Optional[callable]): 在检查条件之前执行的动作。
            post_action (Optional[callable]): 在检查条件之后执行的动作。
            use_gray_scale (bool): 是否使用灰度图像。
            box (Optional[Union[Box, str]]): 可选的搜索区域 Box 或 Box 名称。
            raise_if_not_found (bool): 如果超时未找到是否引发异常。
            canny_lower (int): Canny 边缘检测下限阈值。
            canny_higher (int): Canny 边缘检测上限阈值。
            settle_time (float): 等待条件稳定时间（秒）。
            frame_processor (Optional[callable]): 可选的帧处理器函数。
        """
        ...

    def wait_click_feature(self, feature, horizontal_variance: float = ..., vertical_variance: float = ...,
                           threshold: float = ..., relative_x: float = ..., relative_y: float = ...,
                           time_out: float = ..., pre_action: Optional[callable] = ...,
                           post_action: Optional[callable] = ..., box: Optional[Union[Box, str]] = ...,
                           raise_if_not_found: bool = ..., use_gray_scale: bool = ..., canny_lower: int = ...,
                           canny_higher: int = ..., click_after_delay: float = ..., settle_time: float = ...,
                           after_sleep: float = ...) -> bool:
        """
        等待特征出现并点击。

        参数:
            feature: 要等待的特征。
            horizontal_variance (float): 水平方差。
            vertical_variance (float): 垂直方差。
            threshold (float): 置信度阈值。
            relative_x (float): 相对于 Box 宽度的点击位置。
            relative_y (float): 相对于 Box 高度的点击位置。
            time_out (float): 等待超时时间（秒）。
            pre_action (Optional[callable]): 在检查条件之前执行的动作。
            post_action (Optional[callable]): 在检查条件之后执行的动作。
            box (Optional[Union[Box, str]]): 可选的搜索区域 Box 或 Box 名称。
            raise_if_not_found (bool): 如果超时未找到是否引发异常。
            use_gray_scale (bool): 是否使用灰度图像。
            canny_lower (int): Canny 边缘检测下限阈值。
            canny_higher (int): Canny 边缘检测上限阈值。
            click_after_delay (float): 找到后延迟点击的时间（秒）。
            settle_time (float): 等待条件稳定时间（秒）。
            after_sleep (float): 点击后休眠时间（秒）。

        返回:
            bool: 如果找到并点击返回 True，否则返回 False。
        """
        ...

    def find_one(self, feature_name: Optional[str] = ..., horizontal_variance: float = ...,
                 vertical_variance: float = ..., threshold: float = ..., use_gray_scale: bool = ...,
                 box: Optional[Union[Box, str]] = ..., canny_lower: int = ..., canny_higher: int = ...,
                 frame_processor: Optional[callable] = ..., template: Optional[np.ndarray] = ...,
                 mask_function: Optional[callable] = ..., frame: Optional[np.ndarray] = ..., match_method: int = ...,
                 screenshot: bool = ...) -> Optional[Box]:
        """
        查找图像中的一个特征。

        参数:
            feature_name (Optional[str]): 特征名称。
            horizontal_variance (float): 水平方差。
            vertical_variance (float): 垂直方差。
            threshold (float): 置信度阈值。
            use_gray_scale (bool): 是否使用灰度图像。
            box (Optional[Union[Box, str]]): 可选的搜索区域 Box 或 Box 名称。
            canny_lower (int): Canny 边缘检测下限阈值。
            canny_higher (int): Canny 边缘检测上限阈值。
            frame_processor (Optional[callable]): 可选的帧处理器函数。
            template (Optional[np.ndarray]): 可选的模板图像。
            mask_function (Optional[callable]): 可选的掩码函数。
            frame (Optional[np.ndarray]): 可选的图像帧。
            match_method (int): 模板匹配方法。
            screenshot (bool): 是否截取截图。

        返回:
            Optional[Box]: 找到的 Box 对象，如果未找到则返回 None。
        """
        ...

    def on_feature(self, boxes: list[Box]):
        """
        在找到特征时执行的操作。
        """
        ...

    def feature_exists(self, feature_name: str) -> bool:
        """
        检查特征是否存在。

        参数:
            feature_name (str): 特征名称。

        返回:
            bool: 如果存在返回 True，否则返回 False。
        """
        ...

    def find_best_match_in_box(self, box: Box, to_find: list[str], threshold: float, use_gray_scale: bool = ...,
                               canny_lower: int = ..., canny_higher: int = ...,
                               frame_processor: Optional[callable] = ..., mask_function: Optional[callable] = ...) -> \
            Optional[Box]:
        """
        在指定 Box 区域内查找最佳匹配的特征。

        参数:
            box (Box): 搜索区域 Box。
            to_find (list[str]): 要查找的特征名称列表。
            threshold (float): 置信度阈值。
            use_gray_scale (bool): 是否使用灰度图像。
            canny_lower (int): Canny 边缘检测下限阈值。
            canny_higher (int): Canny 边缘检测上限阈值。
            frame_processor (Optional[callable]): 可选的帧处理器函数。
            mask_function (Optional[callable]): 可选的掩码函数。

        返回:
            Optional[Box]: 最佳匹配的 Box 对象，如果未找到则返回 None。
        """
        ...

    def find_first_match_in_box(self, box: Box, to_find: list[str], threshold: float, use_gray_scale: bool = ...,
                                canny_lower: int = ..., canny_higher: int = ...,
                                frame_processor: Optional[callable] = ..., mask_function: Optional[callable] = ...) -> \
            Optional[Box]:
        """
        在指定 Box 区域内查找第一个匹配的特征。

        参数:
            box (Box): 搜索区域 Box。
            to_find (list[str]): 要查找的特征名称列表。
            threshold (float): 置信度阈值。
            use_gray_scale (bool): 是否使用灰度图像。
            canny_lower (int): Canny 边缘检测下限阈值。
            canny_higher (int): Canny 边缘检测上限阈值。
            frame_processor (Optional[callable]): 可选的帧处理器函数。
            mask_function (Optional[callable]): 可选的掩码函数。

        返回:
            Optional[Box]: 第一个匹配的 Box 对象，如果未找到则返回 None。
        """
        ...


class OCR(FindFeature):
    """
    光学字符识别 (OCR) 类，用于检测和识别图像中的文本。
    """
    ocr_default_threshold: float
    log_debug: bool

    def __init__(self, executor: TaskExecutor):
        """
        初始化 OCR 实例。

        参数:
            executor (TaskExecutor): 任务执行器。
        """
        ...

    def get_threshold(self, lib: str, threshold: float) -> float:
        """
        获取指定 OCR 库的阈值。

        参数:
            lib (str): OCR 库名称。
            threshold (float): 可选的阈值。

        返回:
            float: 最终使用的阈值。
        """
        ...

    def ocr(self, x: float = ..., y: float = ..., to_x: float = ..., to_y: float = ...,
            match: Optional[Union[str, List[str], re.Pattern, List[re.Pattern]]] = ..., width: int = ...,
            height: int = ..., box: Optional[Union[Box, str]] = ..., name: Optional[str] = ..., threshold: float = ...,
            frame: Optional[np.ndarray] = ..., target_height: int = ..., use_grayscale: bool = ..., log: bool = ...,
            frame_processor: Optional[callable] = ..., lib: str = ...) -> list[Box]:
        """
        对图像区域执行 OCR。

        参数:
            x (float): 区域左上角的相对 x 坐标。
            y (float): 区域左上角的相对 y 坐标。
            to_x (float): 区域右下角的相对 x 坐标。
            to_y (float): 区域右下角的相对 y 坐标。
            match (str | List[str] | Pattern[str] | List[Pattern[str]] | None): 用于匹配识别文本的字符串、字符串列表、正则表达式模式或模式列表。
            width (int): 区域宽度（像素）。
            height (int): 区域高度（像素）。
            box (Box | str): 定义区域的 Box 对象或其名称。
            name (str): 区域名称。
            threshold (float): OCR 结果的置信度阈值。
            frame (np.ndarray): 要执行 OCR 的图像帧。
            target_height (int): 调整图像大小以进行 OCR 的目标高度。
            use_grayscale (bool): 在 OCR 前是否将图像转换为灰度。
            log (bool): 是否记录 OCR 结果。
            frame_processor (Optional[callable]): 可选的帧处理器函数。
            lib (str): 要使用的 OCR 库名称。

        返回:
            list[Box]: 表示检测到文本区域的 Box 对象列表，按 y 坐标排序。如果未检测到文本或未找到匹配项，则返回空列表。

        引发:
            Exception: 如果未提供图像帧。
        """
        ...

    def ocr_fun(self, lib: str):
        """
        获取指定 OCR 库的 OCR 函数。

        参数:
            lib (str): OCR 库名称。

        返回:
            OCR 函数。
        """
        ...

    def fix_match_regex(self, match):
        """
        修复匹配正则表达式，应用翻译。
        """
        ...

    def fix_texts(self, detected_boxes: list[Box]):
        """
        修复识别的文本，应用翻译和文本修复。
        """
        ...

    def add_text_fix(self, fix: dict):
        """
        添加文本修复规则到 text_fix 字典。
        """
        ...

    def rapid_ocr(self, box: object, image: object, match: object, scale_factor: float, threshold: float, lib: str) -> \
            tuple[list[Box], list[Box]]:
        """
        使用 RapidOCR 执行 OCR。

        参数:
            box (object): Box 对象。
            image (object): 图像。
            match (object): 匹配条件。
            scale_factor (float): 缩放因子。
            threshold (float): 置信度阈值。
            lib (str): OCR 库名称。

        返回:
            tuple[list[Box], list[Box]]: 检测到的 Box 列表和所有 OCR Box 列表。
        """
        ...

    def duguang_ocr(self, box: object, image: object, match: object, scale_factor: float, threshold: float, lib: str) -> \
            tuple[list[Box], list[Box]]:
        """
        使用 Duguang OCR 执行 OCR。

        参数:
            box (object): Box 对象。
            image (object): 图像。
            match (object): 匹配条件。
            scale_factor (float): 缩放因子。
            threshold (float): 置信度阈值。
            lib (str): OCR 库名称。

        返回:
            tuple[list[Box], list[Box]]: 检测到的 Box 列表和所有 OCR Box 列表。
        """
        ...

    def paddle_ocr(self, box: object, image: object, match: object, scale_factor: float, threshold: float, lib: str) -> \
            tuple[list[Box], list[Box]]:
        """
        使用 PaddleOCR 执行 OCR。

        参数:
            box (object): Box 对象。
            image (object): 图像。
            match (object): 匹配条件。
            scale_factor (float): 缩放因子。
            threshold (float): 置信度阈值。
            lib (str): OCR 库名称。

        返回:
            tuple[list[Box], list[Box]]: 检测到的 Box 列表和所有 OCR Box 列表。
        """
        ...

    def get_box(self, box: object, confidence: float, height: int, pos, scale_factor: float, text, threshold: float,
                width: int) -> Optional[Box]:
        """
        根据 OCR 结果创建 Box 对象。
        """
        ...

    def wait_click_ocr(self, x: float = ..., y: float = ..., to_x: float = ..., to_y: float = ..., width: int = ...,
                       height: int = ..., box: Optional[Union[Box, str]] = ..., name: Optional[str] = ...,
                       match: Optional[Union[str, List[str], re.Pattern, List[re.Pattern]]] = ...,
                       threshold: float = ..., frame: Optional[np.ndarray] = ..., target_height: int = ...,
                       time_out: int = ..., raise_if_not_found: bool = ..., recheck_time: float = ...,
                       after_sleep: float = ..., post_action: Optional[callable] = ..., log: bool = ...,
                       settle_time: float = ..., lib: str = ...) -> Optional[list[Box]]:
        """
        等待 OCR 结果满足条件并点击。

        参数:
            x (float): 区域左上角的相对 x 坐标。
            y (float): 区域左上角的相对 y 坐标。
            to_x (float): 区域右下角的相对 x 坐标。
            to_y (float): 区域右下角的相对 y 坐标。
            width (int): 区域宽度（像素）。
            height (int): 区域高度（像素）。
            box (Box | str): 定义区域的 Box 对象或其名称。
            name (str): 区域名称。
            match (str | List[str] | Pattern[str] | List[Pattern[str]] | None): 用于匹配识别文本的字符串、字符串列表、正则表达式模式或模式列表。
            threshold (float): OCR 结果的置信度阈值。
            frame (np.ndarray): 要执行 OCR 的图像帧。
            target_height (int): 调整图像大小以进行 OCR 的目标高度。
            time_out (int): 等待超时时间（秒）。
            raise_if_not_found (bool): 如果超时未找到是否引发异常。
            recheck_time (float): 重新检查时间（秒）。
            after_sleep (float): 点击后休眠时间（秒）。
            post_action (Optional[callable]): 在检查条件之后执行的动作。
            log (bool): 是否记录 OCR 结果。
            settle_time (float): 等待条件稳定时间（秒）。
            lib (str): 要使用的 OCR 库名称。

        返回:
            Optional[list[Box]]: 找到并点击的 Box 对象列表，如果未找到则返回 None。
        """
        ...

    def wait_ocr(self, x: float = ..., y: float = ..., to_x: float = ..., to_y: float = ..., width: int = ...,
                 height: int = ..., name: Optional[str] = ..., box: Optional[Union[Box, str]] = ...,
                 match: Optional[Union[str, List[str], re.Pattern, List[re.Pattern]]] = ..., threshold: float = ...,
                 frame: Optional[np.ndarray] = ..., target_height: int = ..., time_out: int = ...,
                 post_action: Optional[callable] = ..., raise_if_not_found: bool = ..., log: bool = ...,
                 settle_time: float = ..., lib: str = ...) -> Optional[list[Box]]:
        """
        等待 OCR 结果满足条件。

        参数:
            x (float): 区域左上角的相对 x 坐标。
            y (float): 区域左上角的相对 y 坐标。
            to_x (float): 区域右下角的相对 x 坐标。
            to_y (float): 区域右下角的相对 y 坐标。
            width (int): 区域宽度（像素）。
            height (int): 区域高度（像素）。
            name (str): 区域名称。
            box (Box | str): 定义区域的 Box 对象或其名称。
            match (str | List[str] | Pattern[str] | List[Pattern[str]] | None): 用于匹配识别文本的字符串、字符串列表、正则表达式模式或模式列表。
            threshold (float): OCR 结果的置信度阈值。
            frame (np.ndarray): 要执行 OCR 的图像帧。
            target_height (int): 调整图像大小以进行 OCR 的目标高度。
            time_out (int): 等待超时时间（秒）。
            post_action (Optional[callable]): 在检查条件之后执行的动作。
            raise_if_not_found (bool): 如果超时未找到是否引发异常。
            log (bool): 是否记录 OCR 结果。
            settle_time (float): 等待条件稳定时间（秒）。
            lib (str): 要使用的 OCR 库名称。

        返回:
            Optional[list[Box]]: 找到的 Box 对象列表，如果未找到则返回 None。
        """
        ...


def resize_image(image: object, frame_height: int, target_height: int) -> tuple[object, float]:
    """
    调整图像大小，使其高度接近目标高度。

    参数:
        image (object): 输入图像。
        frame_height (int): 原始帧高度。
        target_height (int): 目标高度。

    返回:
        tuple[object, float]: 调整大小后的图像和缩放因子。
    """
    ...


def scale_box(box: object, scale_factor: float):
    """
    按给定的缩放因子缩放 Box 坐标。

    参数:
        box (object): 要缩放的 Box 对象。
        scale_factor (float): 缩放因子。
    """
    ...


def join_list_elements(input_object) -> str:
    """
    将列表元素连接成一个字符串。
    """
    ...


# Capture.pyx

PW_CLIENT_ONLY: int
PW_RENDERFULLCONTENT: int
PBYTE: ctypes.POINTER[ctypes.c_ubyte]
WGC_NO_BORDER_MIN_BUILD: int
WGC_MIN_BUILD: int


class CaptureException(Exception):
    """
    捕获异常。
    """
    ...


class BaseCaptureMethod:
    """
    基础图像捕获方法类。
    """
    name: str = ...
    description: str = ...
    _size: Tuple
    exit_event: object

    def __init__(self):
        """
        初始化 BaseCaptureMethod 实例。
        """
        ...

    def close(self):
        """
        关闭捕获方法。
        """
        ...

    @property
    def width(self) -> int:
        """
        获取捕获宽度。

        返回:
            int: 宽度。
        """
        ...

    @property
    def height(self) -> int:
        """
        获取捕获高度。

        返回:
            int: 高度。
        """
        ...

    def get_name(self) -> str:
        """
        获取捕获方法名称。

        返回:
            str: 名称。
        """
        ...

    def measure_if_0(self):
        """
        如果尺寸为 0 则测量尺寸。
        """
        ...

    def get_frame(self) -> Optional[object]:
        """
        获取图像帧。

        返回:
            Optional[object]: 图像帧，如果获取失败或退出事件已设置则返回 None。

        引发:
            CaptureException: 如果捕获过程中发生异常。
        """
        ...

    def do_get_frame(self):
        """
        执行实际的帧捕获。
        """
        ...

    def draw_rectangle(self):
        """
        绘制矩形（用于调试）。
        """
        ...

    def clickable(self):
        """
        检查捕获方法是否可点击。
        """
        ...

    def connected(self) -> bool:
        """
        检查捕获方法是否已连接。

        返回:
            bool: 如果已连接返回 True，否则返回 False。
        """
        ...


class BaseWindowsCaptureMethod(BaseCaptureMethod):
    """
    基础 Windows 捕获方法类。
    """
    _hwnd_window: object
    _hwnd_window_internal: "HwndWindow" = None  # Type hint for the backing field

    def __init__(self, hwnd_window: "HwndWindow"):
        """
        初始化 BaseWindowsCaptureMethod 实例。

        参数:
            hwnd_window (HwndWindow): 窗口句柄对象。
        """
        ...

    @property
    def hwnd_window(self) -> "HwndWindow":
        """
        获取窗口句柄对象。

        返回:
            HwndWindow: 窗口句柄对象。
        """
        ...

    @hwnd_window.setter
    def hwnd_window(self, value: "HwndWindow"):
        """
        设置窗口句柄对象。

        参数:
            hwnd_window (HwndWindow): 窗口句柄对象。
        """
        ...

    def connected(self) -> bool:
        """
        检查 Windows 捕获方法是否已连接。

        返回:
            bool: 如果已连接返回 True，否则返回 False。
        """
        ...

    def get_abs_cords(self, x: int, y: int) -> tuple[int, int]:
        """
        获取绝对屏幕坐标。

        参数:
            x (int): 相对于窗口的 x 坐标。
            y (int): 相对于窗口的 y 坐标。

        返回:
            tuple[int, int]: 绝对屏幕坐标 (x, y)。
        """
        ...

    def clickable(self) -> bool:
        """
        检查 Windows 捕获方法是否可点击。

        返回:
            bool: 如果可点击返回 True，否则返回 False。
        """
        ...


def get_crop_point(frame_width: int, frame_height: int, target_width: int, target_height: int) -> tuple[int, int]:
    """
    获取裁剪图像的起始点。

    参数:
        frame_width (int): 图像帧宽度。
        frame_height (int): 图像帧高度。
        target_width (int): 目标宽度。
        target_height (int): 目标高度。

    返回:
        tuple[int, int]: 裁剪起始点 (x, y)。
    """
    ...


render_full: bool


class WindowsGraphicsCaptureMethod(BaseWindowsCaptureMethod):
    """
    Windows Graphics Capture 捕获方法。
    """
    name: str = ...
    description: str = ...

    last_frame: object
    last_frame_time: float
    frame_pool: object
    item: object
    session: object
    cputex: object
    rtdevice: object
    dxdevice: object
    immediatedc: object
    evtoken: object
    last_size: object

    def __init__(self, hwnd_window: "HwndWindow"):
        """
        初始化 WindowsGraphicsCaptureMethod 实例。

        参数:
            hwnd_window (HwndWindow): 窗口句柄对象。
        """
        ...

    def frame_arrived_callback(self, x, y):
        """
        帧到达回调函数。
        """
        ...

    def convert_dx_frame(self, frame) -> Optional[object]:
        """
        将 DX 帧转换为 NumPy 数组。
        """
        ...

    @property
    def hwnd_window(self) -> "HwndWindow":
        """
        获取窗口句柄对象。

        返回:
            HwndWindow: 窗口句柄对象。
        """
        ...

    @hwnd_window.setter
    def hwnd_window(self, hwnd_window: "HwndWindow"):
        """
        设置窗口句柄对象。

        参数:
            hwnd_window (HwndWindow): 窗口句柄对象。
        """
        ...

    def connected(self) -> bool:
        """
        检查 Windows Graphics Capture 方法是否已连接。

        返回:
            bool: 如果已连接返回 True，否则返回 False。
        """
        ...

    def start_or_stop(self, capture_cursor: bool = ...) -> bool:
        """
        启动或停止 Windows Graphics Capture。

        参数:
            capture_cursor (bool): 是否捕获鼠标光标。

        返回:
            bool: 如果启动成功返回 True，否则返回 False。
        """
        ...

    def create_device(self):
        """
        创建 Direct3D 设备。
        """
        ...

    def close(self):
        """
        关闭 Windows Graphics Capture。
        """
        ...

    def do_get_frame(self) -> Optional[object]:
        """
        执行 Windows Graphics Capture 捕获。

        返回:
            Optional[object]: 图像帧，如果获取失败或退出事件已设置则返回 None。
        """
        ...

    def reset_framepool(self, size, reset_device: bool = ...):
        """
        重置帧池。
        """
        ...

    def crop_image(self, frame):
        """
        裁剪图像以移除窗口边框和标题栏。
        """
        ...

    def crop_image_border_title(self, image, border: int, title_height: int):
        """
        裁剪图像的边框和标题栏。
        """
        ...


def windows_graphics_available() -> bool:
    """
    检查 Windows Graphics Capture 是否可用。

    返回:
        bool: 如果可用返回 True，否则返回 False。
    """
    ...


def is_blank(image) -> bool:
    """
    检查图像是否为空白。

    参数:
        image: 输入图像。

    返回:
        bool: 如果为空白返回 True，否则返回 False。
    """
    ...


class BitBltCaptureMethod(BaseWindowsCaptureMethod):
    """
    BitBlt 捕获方法。
    """
    name: str = ...
    short_description: str = ...
    description: str = ...

    dc_object: object
    bitmap: object
    window_dc: object
    compatible_dc: object
    last_hwnd: int
    last_width: int
    last_height: int

    def __init__(self, hwnd_window: "HwndWindow"):
        """
        初始化 BitBltCaptureMethod 实例。

        参数:
            hwnd_window (HwndWindow): 窗口句柄对象。
        """
        ...

    def do_get_frame(self) -> Optional[object]:
        """
        执行 BitBlt 捕获。

        返回:
            Optional[object]: 图像帧，如果获取失败则返回 None。
        """
        ...

    def get_name(self) -> str:
        """
        获取捕获方法名称（包含渲染模式）。

        返回:
            str: 名称。
        """
        ...

    def test_exclusive_full_screen(self) -> bool:
        """
        测试是否能捕获独占全屏窗口。

        返回:
            bool: 如果能捕获返回 True，否则返回 False。
        """
        ...

    def test_is_not_pure_color(self) -> bool:
        """
        测试捕获的图像是否非纯色。

        返回:
            bool: 如果非纯色返回 True，否则返回 False。
        """
        ...

    def bit_blt_capture_frame(self, border: int, title_height: int, _render_full_content: bool = ...) -> Optional[
        object]:
        """
        执行 BitBlt 捕获图像帧。

        参数:
            border (int): 边框宽度。
            title_height (int): 标题栏高度。
            _render_full_content (bool): 是否渲染完整内容。

        返回:
            Optional[object]: 图像帧，如果捕获失败则返回 None。
        """
        ...


class HwndWindow:
    """
    表示一个窗口句柄对象。
    """
    app_exit_event: object
    stop_event: object
    mute_option: object
    thread: object
    device_manager: object
    title: str
    exe_full_path: str
    hwnd_class: str
    _hwnd_title: str
    hwnd: int
    player_id: int
    window_width: int
    window_height: int
    x: int
    y: int
    width: int
    height: int
    frame_width: int
    frame_height: int
    real_width: int
    real_height: int
    real_x_offset: int
    real_y_offset: int
    visible: bool
    exists: bool
    pos_valid: bool
    to_handle_mute: bool
    scaling: float
    frame_aspect_ratio: float
    monitors_bounds: list
    exe_names: list
    visible_monitors: list

    def __init__(self, exit_event: ExitEvent, title: str, exe_name: Optional[Union[str, list]] = ...,
                 frame_width: int = ..., frame_height: int = ..., player_id: int = ..., hwnd_class: Optional[str] = ...,
                 global_config: Optional[GlobalConfig] = ..., device_manager: Optional["DeviceManager"] = ...):
        """
        初始化 HwndWindow 实例。

        参数:
            exit_event (ExitEvent): 应用程序退出事件。
            title (str): 窗口标题。
            exe_name (Optional[Union[str, list]]): 可执行文件名称或名称列表。
            frame_width (int): 帧宽度。
            frame_height (int): 帧高度。
            player_id (int): 玩家 ID。
            hwnd_class (Optional[str]): 窗口类名。
            global_config (Optional[GlobalConfig]): 可选的全局配置。
            device_manager (Optional[DeviceManager]): 可选的设备管理器。
        """
        ...

    def validate_mute_config(self, key, value) -> tuple[bool, Optional[str]]:
        """
        验证静音配置。
        """
        ...

    def stop(self):
        """
        停止窗口句柄对象的更新线程。
        """
        ...

    def bring_to_front(self):
        """
        将窗口带到前台。
        """
        ...

    def try_resize_to(self, resize_to) -> bool:
        """
        尝试将窗口调整到指定尺寸。

        参数:
            resize_to (list[tuple[int, int]]): 要尝试的尺寸列表。

        返回:
            bool: 如果调整成功返回 True，否则返回 False。
        """
        ...

    def update_window(self, title: str, exe_name: Optional[Union[str, list]], frame_width: int, frame_height: int,
                      player_id: int = ..., hwnd_class: Optional[str] = ...):
        """
        更新窗口信息。

        参数:
            title (str): 窗口标题。
            exe_name (Optional[Union[str, list]]): 可执行文件名称或名称列表。
            frame_width (int): 帧宽度。
            frame_height (int): 帧高度。
            player_id (int): 玩家 ID。
            hwnd_class (Optional[str]): 窗口类名。
        """
        ...

    def update_frame_size(self, width: int, height: int):
        """
        更新帧尺寸。

        参数:
            width (int): 帧宽度。
            height (int): 帧高度。
        """
        ...

    def update_window_size(self):
        """
        更新窗口尺寸线程。
        """
        ...

    def get_abs_cords(self, x: int, y: int) -> tuple[int, int]:
        """
        获取绝对屏幕坐标。

        参数:
            x (int): 相对于窗口的 x 坐标。
            y (int): 相对于窗口的 y 坐标。

        返回:
            tuple[int, int]: 绝对屏幕坐标 (x, y)。
        """
        ...

    def do_update_window_size(self):
        """
        执行窗口尺寸更新。
        """
        ...

    def is_foreground(self) -> bool:
        """
        检查窗口是否在前台。

        返回:
            bool: 如果在前台返回 True，否则返回 False。
        """
        ...

    def handle_mute(self, mute: Optional[bool] = ...):
        """
        处理静音状态。
        """
        ...

    def frame_ratio(self, size: int) -> int:
        """
        根据帧比例计算尺寸。

        参数:
            size (int): 原始尺寸。

        返回:
            int: 计算后的尺寸。
        """
        ...

    @property
    def hwnd_title(self) -> str:
        """
        获取窗口标题。

        返回:
            str: 窗口标题。
        """
        ...


def check_pos(x: int, y: int, width: int, height: int, monitors_bounds: list[tuple[int, int, int, int]]) -> bool:
    """
    检查窗口位置是否有效。

    参数:
        x (int): 窗口 x 坐标。
        y (int): 窗口 y 坐标。
        width (int): 窗口宽度。
        height (int): 窗口高度。
        monitors_bounds (list[tuple[int, int, int, int]]): 显示器边界列表。

    返回:
        bool: 如果位置有效返回 True，否则返回 False。
    """
    ...


def get_monitors_bounds() -> list[tuple[int, int, int, int]]:
    """
    获取所有显示器的边界。

    返回:
        list[tuple[int, int, int, int]]: 显示器边界列表。
    """
    ...


def is_window_in_screen_bounds(window_left: int, window_top: int, window_width: int, window_height: int,
                               monitors_bounds: list[tuple[int, int, int, int]]) -> bool:
    """
    检查窗口是否在屏幕范围内。

    参数:
        window_left (int): 窗口左侧坐标。
        window_top (int): 窗口顶部坐标。
        window_width (int): 窗口宽度。
        window_height (int): 窗口高度。
        monitors_bounds (list[tuple[int, int, int, int]]): 显示器边界列表。

    返回:
        bool: 如果在屏幕范围内返回 True，否则返回 False。
    """
    ...


def find_hwnd(title: Optional[str], exe_names: Optional[Union[str, list]], frame_width: int, frame_height: int,
              player_id: int = ..., class_name: Optional[str] = ..., selected_hwnd: int = ...) -> tuple[
    Optional[str], int, Optional[str], int, int, int, int]:
    """
    查找窗口句柄。

    参数:
        title (Optional[str]): 窗口标题。
        exe_names (Optional[Union[str, list]]): 可执行文件名称或名称列表。
        frame_width (int): 帧宽度。
        frame_height (int): 帧高度。
        player_id (int): 玩家 ID。
        class_name (Optional[str]): 窗口类名。
        selected_hwnd (int): 选中的窗口句柄。

    返回:
        tuple[Optional[str], int, Optional[str], int, int, int, int]: 窗口标题、句柄、可执行文件路径、真实 x 偏移、真实 y 偏移、真实宽度和真实高度。
    """
    ...


def get_mute_state(hwnd: int) -> int:
    """
    获取窗口的静音状态。

    参数:
        hwnd (int): 窗口句柄。

    返回:
        int: 静音状态（0 为非静音，1 为静音）。
    """
    ...


def set_mute_state(hwnd: int, mute: int):
    """
    设置窗口的静音状态。

    参数:
        hwnd (int): 窗口句柄。
        mute (int): 静音状态（0 为非静音，1 为静音）。
    """
    ...


def get_player_id_from_cmdline(cmdline) -> int:
    """
    从命令行参数中提取玩家 ID。

    参数:
        cmdline (list): 命令行参数列表。

    返回:
        int: 玩家 ID，如果未找到则返回 0。
    """
    ...


def enum_child_windows(biggest, frame_aspect_ratio):
    """
    枚举子窗口并查找与帧比例匹配的子窗口。
    """
    ...


def get_exe_by_hwnd(hwnd: int) -> tuple[Optional[str], Optional[str], Optional[list]]:
    """
    根据窗口句柄获取可执行文件信息。

    参数:
        hwnd (int): 窗口句柄。

    返回:
        tuple[Optional[str], Optional[str], Optional[list]]: 可执行文件名称、路径和命令行参数列表。
    """
    ...


# string_compare.pyx

def compare_strings_safe(str1: str, str2: str) -> bool:
    """
    安全地比较两个字符串（忽略大小写）。

    参数:
        str1 (str): 第一个字符串。
        str2 (str): 第二个字符串。

    返回:
        bool: 如果字符串相等返回 True，否则返回 False。
    """
    ...


# globals.py

class OkGlobals:
    """
    全局变量类。
    """
    app: Optional[App] = ...
    executor: Optional[TaskExecutor] = ...
    device_manager: Optional["DeviceManager"] = ...
    handler: Optional[Handler] = ...
    auth_uid: Optional[str] = ...
    auth_rd: Optional[int] = ...
    auth_expire: int = ...
    trial_expire: int = ...
    my_app: Optional[object] = ...
    dpi_scaling: float = ...
    ok: Optional["OK"] = ...
    config: Optional[dict] = ...
    task_manager: Optional[object] = ...
    app_path: str = ...
    use_dml: bool = ...
    global_config: Optional[GlobalConfig] = ...

    def __init__(self):
        """
        初始化 OkGlobals 实例。
        """
        ...

    def set_use_dml(self):
        """
        设置是否使用 DirectML。
        """
        ...

    def get_trial_expire_util_str(self) -> str:
        """
        获取试用过期时间的字符串表示。

        返回:
            str: 试用过期时间的字符串。
        """
        ...

    def get_expire_util_str(self) -> str:
        """
        获取授权过期时间的字符串表示。

        返回:
            str: 授权过期时间的字符串。
        """
        ...

    def set_dpi_scaling(self, window):
        """
        设置 DPI 缩放比例。
        """
        ...


og: OkGlobals = ...


# Config.py

class Config(dict):
    """
    配置类，用于管理应用程序配置。
    """
    config_folder: str = ...

    def __init__(self, name, default: dict, folder: Optional[str] = ..., validator: Optional[callable] = ...):
        """
        初始化 Config 对象。

        参数:
            name (str): 配置文件名称。
            default (dict): 默认配置值。
            folder (Optional[str]): 存储配置文件的文件夹。
            validator (Optional[callable]): 可选的验证函数。
        """
        ...

    def save_file(self):
        """
        将当前配置保存到文件。
        """
        ...

    def get_default(self, key):
        """
        获取默认配置值。

        参数:
            key: 配置键。
        """
        ...

    def reset_to_default(self):
        """
        将配置重置为默认值。
        """
        ...

    def pop(self, key, default: Optional[object] = ...):
        """
        从配置中移除并返回一个值。

        参数:
            key: 要移除的键。
            default (Optional[object]): 如果键不存在，返回的默认值。

        返回:
            移除的值。
        """
        ...

    def popitem(self):
        """
        移除并返回配置中的最后一个键值对。
        """
        ...

    def clear(self):
        """
        清除所有配置值。
        """
        ...

    def has_user_config(self) -> bool:
        """
        检查是否存在用户配置。

        返回:
            bool: 如果存在用户配置返回 True，否则返回 False。
        """
        ...

    def validate(self, key, value) -> bool:
        """
        验证配置键值对。

        参数:
            key: 要验证的键。
            value: 要验证的值。

        返回:
            bool: 如果有效返回 True，否则返回 False。
        """
        ...

    def verify_config(self, current: dict, default_config: dict) -> bool:
        """
        验证配置与默认配置是否一致。

        参数:
            current (dict): 当前配置。
            default_config (dict): 默认配置。

        返回:
            bool: 如果配置被修改返回 True，否则返回 False。
        """
        ...


# analytics

class Analytics:
    """
    应用程序分析类。
    """

    def __init__(self, app_config: dict, exit_event: ExitEvent):
        """
        初始化 Analytics 实例。

        参数:
            app_config (dict): 应用程序配置。
            exit_event (ExitEvent): 退出事件。
        """
        ...

    @property
    def user_properties(self):
        """
        获取用户属性。
        """
        ...

    @property
    def client_id(self):
        """
        获取客户端 ID。
        """
        ...

    def send_alive(self):
        """
        发送存活报告。
        """
        ...

    def get_unique_client_id(self):
        """
        获取唯一的客户端 ID。
        """
        ...


def get_bios_serial_number() -> Optional[str]:
    """
    获取 BIOS 序列号。

    返回:
        Optional[str]: BIOS 序列号，如果获取失败则返回 None。
    """
    ...


def random_number() -> int:
    """
    生成一个随机整数。

    返回:
        int: 随机整数。
    """
    ...


def get_screen_resolution() -> str:
    """
    获取屏幕分辨率。

    返回:
        str: 屏幕分辨率字符串。
    """
    ...


def hash_dict_keys_values(my_dict: dict) -> str:
    """
    对字典的键值对计算 MD5 校验和。

    参数:
        my_dict (dict): 输入字典。

    返回:
        str: MD5 校验和。
    """
    ...


# ConfigOptions

class ConfigOption:
    """
    配置选项类。
    """

    def __init__(self, name: str, default: Optional[dict] = ..., description: str = ...,
                 config_description: Optional[dict] = ..., config_type: Optional[dict] = ...,
                 validator: Optional[callable] = ..., icon: Optional[FluentIcon] = ...):
        """
        初始化 ConfigOption 实例。

        参数:
            name (str): 选项名称。
            default (Optional[dict]): 默认配置。
            description (str): 描述。
            config_description (Optional[dict]): 配置描述。
            config_type (Optional[dict]): 配置类型。
            validator (Optional[callable]): 验证函数。
            icon (Optional[FluentIcon]): 图标。
        """
        ...


basic_options: ConfigOption


class GlobalConfig:
    """
    全局配置类。
    """

    def __init__(self, config_options):
        """
        初始化 GlobalConfig 实例。
        """
        ...

    def get_config(self, option: Union[str, ConfigOption]):
        """
        获取配置对象。

        参数:
            option (str | ConfigOption): 配置选项名称或 ConfigOption 对象。
        """
        ...

    def get_config_desc(self, key):
        """
        获取配置描述。
        """
        ...

    def get_all_visible_configs(self) -> list[tuple[str, Config, ConfigOption]]:
        """
        获取所有可见配置。

        返回:
            list[tuple[str, Config, ConfigOption]]: 可见配置列表。
        """
        ...


class InfoDict(dict):
    """
    信息字典类。
    """
    ...


# FeatureSet

class FeatureSet:
    """
    特征集类，管理图像特征。
    """
    width: int
    height: int
    default_threshold: float
    default_horizontal_variance: float
    default_vertical_variance: float
    coco_json: str
    debug: bool
    load_success: bool
    feature_dict: dict
    box_dict: dict
    lock: object

    def __init__(self, debug: bool, coco_json: str, default_horizontal_variance: float,
                 default_vertical_variance: float, default_threshold: float = ...):
        """
        初始化 FeatureSet 实例。

        参数:
            debug (bool): 是否处于调试模式。
            coco_json (str): COCO 数据集 JSON 文件路径。
            default_horizontal_variance (float): 默认水平方差。
            default_vertical_variance (float): 默认垂直方差。
            default_threshold (float): 默认置信度阈值。
        """
        ...

    def feature_exists(self, feature_name: str) -> bool:
        """
        检查特征是否存在。

        参数:
            feature_name (str): 特征名称。

        返回:
            bool: 如果存在返回 True，否则返回 False。
        """
        ...

    def empty(self) -> bool:
        """
        检查特征集是否为空。

        返回:
            bool: 如果为空返回 True，否则返回 False。
        """
        ...

    def check_size(self, frame: object) -> bool:
        """
        检查图像帧尺寸并处理数据。

        参数:
            frame (object): 图像帧。

        返回:
            bool: 如果加载成功返回 True，否则返回 False。
        """
        ...

    def process_data(self) -> bool:
        """
        处理 COCO 数据集中的图像和标注。

        返回:
            bool: 如果处理成功返回 True，否则返回 False。
        """
        ...

    def get_box_by_name(self, mat, category_name) -> Optional[object]:
        """
        根据名称获取 Box 对象。

        参数:
            mat: 图像数据。
            category_name (str): Box 名称。

        返回:
            Optional[object]: Box 对象，如果未找到则返回 None。
        """
        ...

    def save_images(self, target_folder: str):
        """
        将所有特征图像保存到指定文件夹。

        参数:
            target_folder (str): 要保存图像的文件夹路径。
        """
        ...

    def get_feature_by_name(self, mat, name) -> Optional[object]:
        """
        根据名称获取特征对象。

        参数:
            mat: 图像数据。
            name (str): 特征名称。

        返回:
            Optional[object]: 特征对象，如果未找到则返回 None。
        """
        ...

    def find_one_feature(self, mat: np.ndarray, category_name, horizontal_variance: float = ...,
                         vertical_variance: float = ..., threshold: float = ..., use_gray_scale: bool = ...,
                         x: int = ..., y: int = ..., to_x: int = ..., to_y: int = ..., width: int = ...,
                         height: int = ..., box: Optional[Union[Box, str]] = ..., canny_lower: int = ...,
                         canny_higher: int = ..., frame_processor: Optional[callable] = ...,
                         template: Optional[np.ndarray] = ..., match_method: int = ..., screenshot: bool = ...,
                         mask_function: Optional[callable] = ...) -> List[Box]:
        """
        查找图像中的一个特征。

        参数:
            mat (np.ndarray): 要查找特征的图像。
            category_name (str): 要查找特征的类别名称。
            horizontal_variance (float): 水平方差。
            vertical_variance (float): 垂直方差。
            threshold (float): 置信度阈值。
            use_gray_scale (bool): 是否使用灰度图像。
            x (int): x 坐标。
            y (int): y 坐标。
            to_x (int): 右下角 x 坐标。
            to_y (int): 右下角 y 坐标。
            width (int): 宽度。
            height (int): 高度。
            box (Optional[Union[Box, str]]): 可选的搜索区域 Box 或 Box 名称。
            canny_lower (int): Canny 边缘检测下限阈值。
            canny_higher (int): Canny 边缘检测上限阈值。
            frame_processor (Optional[callable]): 可选的帧处理器函数。
            template (Optional[np.ndarray]): 可选的模板图像。
            match_method (int): 模板匹配方法。
            screenshot (bool): 是否截取截图。
            mask_function (Optional[callable]): 可选的掩码函数。

        返回:
            List[Box]: 找到的 Box 对象列表。
        """
        ...

    def find_feature(self, mat: np.ndarray, category_name: Union[str, list], horizontal_variance: float = ...,
                     vertical_variance: float = ..., threshold: float = ..., use_gray_scale: bool = ..., x: int = ...,
                     y: int = ..., to_x: int = ..., to_y: int = ..., width: int = ..., height: int = ...,
                     box: Optional[Union[Box, str]] = ..., canny_lower: int = ..., canny_higher: int = ...,
                     frame_processor: Optional[callable] = ..., template: Optional[np.ndarray] = ...,
                     match_method: int = ..., screenshot: bool = ..., mask_function: Optional[callable] = ...,
                     frame: Optional[np.ndarray] = ...) -> List[Box]:
        """
        查找图像中的特征。

        参数:
            mat (np.ndarray): 要查找特征的图像。
            category_name (str | list): 要查找特征的类别名称或名称列表。
            horizontal_variance (float): 水平方差。
            vertical_variance (float): 垂直方差。
            threshold (float): 置信度阈值。
            use_gray_scale (bool): 是否使用灰度图像。
            x (int): x 坐标。
            y (int): y 坐标。
            to_x (int): 右下角 x 坐标。
            to_y (int): 右下角 y 坐标。
            width (int): 宽度。
            height (int): 高度。
            box (Optional[Union[Box, str]]): 可选的搜索区域 Box 或 Box 名称。
            canny_lower (int): Canny 边缘检测下限阈值。
            canny_higher (int): Canny 边缘检测上限阈值。
            frame_processor (Optional[callable]): 可选的帧处理器函数。
            template (Optional[np.ndarray]): 可选的模板图像。
            match_method (int): 模板匹配方法。
            screenshot (bool): 是否截取截图。
            mask_function (Optional[callable]): 可选的掩码函数。
            frame (Optional[np.ndarray]): 可选的图像帧。

        返回:
            List[Box]: 找到的 Box 对象列表。
        """
        ...


class BaseInteraction:
    """
    基础交互类。
    """

    def __init__(self, capture: BaseCaptureMethod):
        """
        初始化 BaseInteraction 实例。

        参数:
            capture (BaseCaptureMethod): 捕获方法。
        """
        ...

    def should_capture(self) -> bool:
        """
        检查是否应该捕获。

        返回:
            bool: 如果应该捕获返回 True，否则返回 False。
        """
        ...

    def send_key(self, key, down_time: float = ...):
        """
        发送按键事件。

        参数:
            key: 按键。
            down_time (float): 按下时间（秒）。
        """
        ...

    def send_key_down(self, key):
        """
        模拟按下按键。

        参数:
            key: 按键。
        """
        ...

    def send_key_up(self, key):
        """
        模拟释放按键。

        参数:
            key: 按键。
        """
        ...

    def move(self, x: int, y: int):
        """
        模拟鼠标移动。

        参数:
            x (int): x 坐标。
            y (int): y 坐标。
        """
        ...

    def swipe(self, from_x: int, from_y: int, to_x: int, to_y: int, duration: int, settle_time: float = ...):
        """
        模拟滑动。

        参数:
            from_x (int): 起始 x 坐标。
            from_y (int): 起始 y 坐标。
            to_x (int): 结束 x 坐标。
            to_y (int): 结束 y 坐标。
            duration (int): 持续时间。
            settle_time (float): 稳定时间（秒）。
        """
        ...

    def click(self, x: int = ..., y: int = ..., move_back: bool = ..., name: Optional[str] = ..., move: bool = ...,
              down_time: float = ..., key: str = ...):
        """
        模拟鼠标点击。

        参数:
            x (int): x 坐标。
            y (int): y 坐标。
            move_back (bool): 点击后是否将鼠标移回原位。
            name (Optional[str]): 点击的名称。
            move (bool): 是否移动鼠标到点击位置。
            down_time (float): 按下时间（秒）。
            key (str): 鼠标键。
        """
        ...

    def on_run(self):
        """
        运行时执行的操作。
        """
        ...

    def input_text(self, text: str):
        """
        输入文本。

        参数:
            text (str): 要输入的文本。
        """
        ...

    def back(self, after_sleep: float = ...):
        """
        模拟返回操作。

        参数:
            after_sleep (float): 操作后休眠时间（秒）。
        """
        ...

    def scroll(self, x: int, y: int, scroll_amount: int):
        """
        模拟滚动。

        参数:
            x (int): 滚动中心 x 坐标。
            y (int): 滚动中心 y 坐标。
            scroll_amount (int): 滚动量。
        """
        ...


class PyDirectInteraction(BaseInteraction):
    """
    使用 pydirectinput 进行交互。
    """

    def __init__(self, capture: BaseCaptureMethod, hwnd_window: HwndWindow):
        """
        初始化 PyDirectInteraction 实例。

        参数:
            capture (BaseCaptureMethod): 捕获方法。
            hwnd_window (HwndWindow): 窗口句柄对象。
        """
        ...

    def clickable(self) -> bool:
        """
        检查是否可点击。

        返回:
            bool: 如果可点击返回 True，否则返回 False。
        """
        ...

    def send_key(self, key, down_time: float = ...):
        """
        发送按键事件。

        参数:
            key: 按键。
            down_time (float): 按下时间（秒）。
        """
        ...

    def send_key_down(self, key):
        """
        模拟按下按键。

        参数:
            key: 按键。
        """
        ...

    def send_key_up(self, key):
        """
        模拟释放按键。

        参数:
            key: 按键。
        """
        ...

    def move(self, x: int, y: int):
        """
        模拟鼠标移动。

        参数:
            x (int): x 坐标。
            y (int): y 坐标。
        """
        ...

    def swipe(self, x1: int, y1: int, x2: int, y2: int, duration: float, after_sleep: float = ...,
              settle_time: float = ...):
        """
        模拟滑动。

        参数:
            x1 (int): 起始 x 坐标。
            y1 (int): 起始 y 坐标。
            x2 (int): 结束 x 坐标。
            y2 (int): 结束 y 坐标。
            duration (float): 持续时间（秒）。
            after_sleep (float): 滑动后休眠时间（秒）。
            settle_time (float): 稳定时间（秒）。
        """
        ...

    def click(self, x: int = ..., y: int = ..., move_back: bool = ..., name: Optional[str] = ..., move: bool = ...,
              down_time: float = ..., key: str = ...):
        """
        模拟鼠标点击。

        参数:
            x (int): x 坐标。
            y (int): y 坐标。
            move_back (bool): 点击后是否将鼠标移回原位。
            name (Optional[str]): 点击的名称。
            move (bool): 是否移动鼠标到点击位置。
            down_time (float): 按下时间（秒）。
            key (str): 鼠标键。
        """
        ...

    def mouse_down(self, x: int = ..., y: int = ..., name: Optional[str] = ..., key: str = ...):
        """
        模拟鼠标按下。

        参数:
            x (int): x 坐标。
            y (int): y 坐标。
            name (Optional[str]): 按下的名称。
            key (str): 鼠标键。
        """
        ...

    def get_mouse_button(self, key: str):
        """
        获取鼠标按键常量。

        参数:
            key (str): 鼠标键。
        """
        ...

    def mouse_up(self, key: str = ...):
        """
        模拟鼠标释放。

        参数:
            key (str): 鼠标键。
        """
        ...

    def should_capture(self) -> bool:
        """
        检查是否应该捕获。

        返回:
            bool: 如果应该捕获返回 True，否则返回 False。
        """
        ...

    def on_run(self):
        """
        运行时执行的操作。
        """
        ...


# can interact with background windows, some games support it, like wuthering waves
class PostMessageInteraction(BaseInteraction):
    """
    使用 PostMessage 进行交互。
    """

    def __init__(self, capture: BaseCaptureMethod, hwnd_window: HwndWindow):
        """
        初始化 PostMessageInteraction 实例。

        参数:
            capture (BaseCaptureMethod): 捕获方法。
            hwnd_window (HwndWindow): 窗口句柄对象。
        """
        ...

    @property
    def hwnd(self) -> int:
        """
        获取窗口句柄。

        返回:
            int: 窗口句柄。
        """
        ...

    def on_visible(self, visible: bool):
        """
        窗口可见性改变时执行的操作。

        参数:
            visible (bool): 窗口是否可见。
        """
        ...

    def send_key(self, key, down_time: float = ...):
        """
        发送按键事件。

        参数:
            key: 按键。
            down_time (float): 按下时间（秒）。
        """
        ...

    def send_key_down(self, key, activate: bool = ...):
        """
        模拟按下按键。

        参数:
            key: 按键。
            activate (bool): 是否尝试激活窗口。
        """
        ...

    def send_key_up(self, key):
        """
        模拟释放按键。

        参数:
            key: 按键。
        """
        ...

    def get_key_by_str(self, key):
        """
        根据字符串获取按键的 VK Code。

        参数:
            key (str): 按键字符串。

        返回:
            按键的 VK Code。
        """
        ...

    def move(self, x: int, y: int, down_btn: int = ...):
        """
        模拟鼠标移动。

        参数:
            x (int): x 坐标。
            y (int): y 坐标。
            down_btn (int): 按下的鼠标按钮常量。
        """
        ...

    def scroll(self, x: int, y: int, scroll_amount: int):
        """
        模拟滚动。

        参数:
            x (int): 滚动中心 x 坐标。
            y (int): 滚动中心 y 坐标。
            scroll_amount (int): 滚动量。
        """
        ...

    def post(self, message: int, wParam: int = ..., lParam: int = ...):
        """
        发送 PostMessage。

        参数:
            message (int): 消息常量。
            wParam (int): wParam 参数。
            lParam (int): lParam 参数。
        """
        ...

    def swipe(self, x1: int, y1: int, x2: int, y2: int, duration: int = ..., after_sleep: float = ...,
              settle_time: float = ...):
        """
        模拟滑动。

        参数:
            x1 (int): 起始 x 坐标。
            y1 (int): 起始 y 坐标。
            x2 (int): 结束 x 坐标。
            y2 (int): 结束 y 坐标。
            duration (int): 持续时间。
            after_sleep (float): 滑动后休眠时间（秒）。
            settle_time (float): 稳定时间（秒）。
        """
        ...

    def activate(self):
        """
        激活窗口。
        """
        ...

    def deactivate(self):
        """
        取消激活窗口。
        """
        ...

    def try_activate(self):
        """
        如果窗口不在前台，尝试激活窗口。
        """
        ...

    def click(self, x: int = ..., y: int = ..., move_back: bool = ..., name: Optional[str] = ..., move: bool = ...,
              down_time: float = ..., key: str = ...):
        """
        模拟鼠标点击。

        参数:
            x (int): x 坐标。
            y (int): y 坐标。
            move_back (bool): 点击后是否将鼠标移回原位。
            name (Optional[str]): 点击的名称。
            move (bool): 是否移动鼠标到点击位置。
            down_time (float): 按下时间（秒）。
            key (str): 鼠标键。
        """
        ...

    def right_click(self, x: int = ..., y: int = ..., move_back: bool = ..., name: Optional[str] = ...):
        """
        模拟鼠标右键点击。

        参数:
            x (int): x 坐标。
            y (int): y 坐标。
            move_back (bool): 点击后是否将鼠标移回原位。
            name (Optional[str]): 点击的名称。
        """
        ...

    def mouse_down(self, x: int = ..., y: int = ..., name: Optional[str] = ..., key: str = ...):
        """
        模拟鼠标按下。

        参数:
            x (int): x 坐标。
            y (int): y 坐标。
            name (Optional[str]): 按下的名称。
            key (str): 鼠标键。
        """
        ...

    def update_mouse_pos(self, x: int, y: int, activate: bool = ...):
        """
        更新鼠标位置并返回 lParam。
        """
        ...

    def mouse_up(self, key: str = ...):
        """
        模拟鼠标释放。

        参数:
            key (str): 鼠标键。
        """
        ...

    def should_capture(self) -> bool:
        """
        检查是否应该捕获。

        返回:
            bool: 如果应该捕获返回 True，否则返回 False。
        """
        ...


vk_key_dict: dict = ...


class DoNothingInteraction(BaseInteraction):
    """
    不执行任何操作的交互类。
    """
    ...


class ADBInteraction(BaseInteraction):
    """
    使用 ADB 进行交互。
    """

    def __init__(self, device_manager: "DeviceManager", capture: BaseCaptureMethod, device_width: int,
                 device_height: int):
        """
        初始化 ADBInteraction 实例。

        参数:
            device_manager (DeviceManager): 设备管理器。
            capture (BaseCaptureMethod): 捕获方法。
            device_width (int): 设备宽度。
            device_height (int): 设备高度。
        """
        ...

    def send_key(self, key, down_time: float = ..., after_sleep: float = ...):
        """
        发送按键事件。

        参数:
            key: 按键。
            down_time (float): 按下时间（秒）。
            after_sleep (float): 操作后休眠时间（秒）。
        """
        ...

    def input_text(self, text: str):
        """
        输入文本。

        参数:
            text (str): 要输入的文本。
        """
        ...

    @property
    def u2(self):
        """
        获取 uiautomator2 设备对象。
        """
        ...

    def swipe_u2(self, from_x: int, from_y: int, to_x: int, to_y: int, duration: float, after_sleep: float = ...,
                 settle_time: float = ...):
        """
        使用 uiautomator2 模拟滑动。

        参数:
            from_x (int): 起始 x 坐标。
            from_y (int): 起始 y 坐标。
            to_x (int): 结束 x 坐标。
            to_y (int): 结束 y 坐标。
            duration (float): 持续时间（秒）。
            after_sleep (float): 滑动后休眠时间（秒）。
            settle_time (float): 稳定时间（秒）。
        """
        ...

    def swipe(self, from_x: int, from_y: int, to_x: int, to_y: int, duration: float, after_sleep: float = ...,
              settle_time: float = ...):
        """
        模拟滑动。

        参数:
            from_x (int): 起始 x 坐标。
            from_y (int): 起始 y 坐标。
            to_x (int): 结束 x 坐标。
            to_y (int): 结束 y 坐标。
            duration (float): 持续时间（秒）。
            after_sleep (float): 滑动后休眠时间（秒）。
            settle_time (float): 稳定时间（秒）。
        """
        ...

    def click(self, x: int = ..., y: int = ..., move_back: bool = ..., name: Optional[str] = ..., move: bool = ...,
              down_time: float = ..., key: Optional[str] = ...):
        """
        模拟鼠标点击。

        参数:
            x (int): x 坐标。
            y (int): y 坐标。
            move_back (bool): 点击后是否将鼠标移回原位。
            name (Optional[str]): 点击的名称。
            move (bool): 是否移动鼠标到点击位置。
            down_time (float): 按下时间（秒）。
            key (Optional[str]): 鼠标键。
        """
        ...

    def back(self, after_sleep: float = ...):
        """
        模拟返回操作。

        参数:
            after_sleep (float): 操作后休眠时间（秒）。
        """
        ...


class MOUSEINPUT(ctypes.Structure):
    """
    MOUSEINPUT 结构体。
    """
    ...


class INPUT(ctypes.Structure):
    """
    INPUT 结构体。
    """
    ...


SendInput: object


class GenshinInteraction(BaseInteraction):
    """
    原神交互类，针对原神窗口进行交互。
    """

    def __init__(self, capture: BaseCaptureMethod, hwnd_window: HwndWindow):
        """
        初始化 GenshinInteraction 实例。

        参数:
            capture (BaseCaptureMethod): 捕获方法。
            hwnd_window (HwndWindow): 窗口句柄对象。
        """
        ...

    @property
    def hwnd(self) -> int:
        """
        获取窗口句柄。

        返回:
            int: 窗口句柄。
        """
        ...

    def do_post_scroll(self, x: int, y: int, scroll_amount: int):
        """
        执行 PostMessage 滚动操作。
        """
        ...

    def do_send_key(self, key, down_time: float = ...):
        """
        执行发送按键操作。
        """
        ...

    def operate(self, fun: callable, block: bool = ...):
        """
        执行操作，处理窗口激活和输入阻塞。
        """
        ...

    def send_key(self, key, down_time: float = ...):
        """
        发送按键事件。

        参数:
            key: 按键。
            down_time (float): 按下时间（秒）。
        """
        ...

    def block_input(self):
        """
        阻塞输入。
        """
        ...

    def unblock_input(self):
        """
        解除阻塞输入。
        """
        ...

    def send_key_down(self, key):
        """
        模拟按下按键。

        参数:
            key: 按键。
        """
        ...

    def do_send_key_down(self, key):
        """
        执行模拟按下按键操作。
        """
        ...

    def do_send_key_up(self, key):
        """
        执行模拟释放按键操作。
        """
        ...

    def send_key_up(self, key):
        """
        模拟释放按键。

        参数:
            key: 按键。
        """
        ...

    def get_key_by_str(self, key):
        """
        根据字符串获取按键的 VK Code。

        参数:
            key (str): 按键字符串。

        返回:
            按键的 VK Code。
        """
        ...

    def move_mouse_by(self, x: int = ..., y: int = ...):
        """
        相对于当前位置移动鼠标。
        """
        ...

    def move(self, x: int, y: int, down_btn: int = ...):
        """
        模拟鼠标移动。

        参数:
            x (int): x 坐标。
            y (int): y 坐标。
            down_btn (int): 按下的鼠标按钮常量。
        """
        ...

    def middle_click(self, x: int = ..., y: int = ..., move_back: bool = ..., name: Optional[str] = ...,
                     down_time: float = ...):
        """
        模拟鼠标中键点击。

        参数:
            x (int): x 坐标。
            y (int): y 坐标。
            move_back (bool): 点击后是否将鼠标移回原位。
            name (Optional[str]): 点击的名称。
            down_time (float): 按下时间（秒）。
        """
        ...

    def do_scroll(self, x: int, y: int, scroll_amount: int):
        """
        执行滚动操作。
        """
        ...

    def scroll(self, x: int, y: int, scroll_amount: int):
        """
        模拟滚动。

        参数:
            x (int): 滚动中心 x 坐标。
            y (int): 滚动中心 y 坐标。
            scroll_amount (int): 滚动量。
        """
        ...

    def post(self, message: int, wParam: int = ..., lParam: int = ...):
        """
        发送 PostMessage。

        参数:
            message (int): 消息常量。
            wParam (int): wParam 参数。
            lParam (int): lParam 参数。
        """
        ...

    def swipe(self, x1: int, y1: int, x2: int, y2: int, duration: int = ..., after_sleep: float = ...,
              settle_time: float = ...):
        """
        模拟滑动。

        参数:
            x1 (int): 起始 x 坐标。
            y1 (int): 起始 y 坐标。
            x2 (int): 结束 x 坐标。
            y2 (int): 结束 y 坐标。
            duration (int): 持续时间。
            after_sleep (float): 滑动后休眠时间（秒）。
            settle_time (float): 稳定时间（秒）。
        """
        ...

    def activate(self):
        """
        激活窗口。
        """
        ...

    def deactivate(self):
        """
        取消激活窗口。
        """
        ...

    def try_activate(self):
        """
        如果窗口不在前台，尝试激活窗口。
        """
        ...

    def click(self, x: int = ..., y: int = ..., move_back: bool = ..., name: Optional[str] = ...,
              down_time: float = ..., move: bool = ..., key: str = ...):
        """
        模拟鼠标点击。

        参数:
            x (int): x 坐标。
            y (int): y 坐标。
            move_back (bool): 点击后是否将鼠标移回原位。
            name (Optional[str]): 点击的名称。
            down_time (float): 按下时间（秒）。
            move (bool): 是否移动鼠标到点击位置。
            key (str): 鼠标键。
        """
        ...

    def do_middle_click(self, x: int = ..., y: int = ..., move_back: bool = ..., name: Optional[str] = ...,
                        down_time: float = ...):
        """
        执行模拟鼠标中键点击操作。
        """
        ...

    def do_click(self, x: int = ..., y: int = ..., move_back: bool = ..., name: Optional[str] = ...,
                 down_time: float = ..., move: bool = ..., key: str = ...):
        """
        执行模拟鼠标点击操作。
        """
        ...

    def do_mouse_up(self, x: int = ..., y: int = ..., move_back: bool = ..., move: bool = ...,
                    btn: Optional[str] = ...):
        """
        执行模拟鼠标释放操作。
        """
        ...

    def right_click(self, x: int = ..., y: int = ..., move_back: bool = ..., name: Optional[str] = ...,
                    down_time: float = ...):
        """
        模拟鼠标右键点击。

        参数:
            x (int): x 坐标。
            y (int): y 坐标。
            move_back (bool): 点击后是否将鼠标移回原位。
            name (Optional[str]): 点击的名称。
            down_time (float): 按下时间（秒）。
        """
        ...

    def mouse_down(self, x: int = ..., y: int = ..., name: Optional[str] = ..., key: str = ...):
        """
        模拟鼠标按下。

        参数:
            x (int): x 坐标。
            y (int): y 坐标。
            name (Optional[str]): 按下的名称。
            key (str): 鼠标键。
        """
        ...

    def do_mouse_down(self, x: int = ..., y: int = ..., name: Optional[str] = ..., key: str = ...):
        """
        执行模拟鼠标按下操作。
        """
        ...

    def make_mouse_position(self, x: int, y: int):
        """
        创建鼠标位置的 lParam。
        """
        ...

    def do_mouse_up(self, x: int = ..., y: int = ..., key: str = ...):
        """
        执行模拟鼠标释放操作。
        """
        ...

    def update_mouse_pos(self, x: int, y: int, activate: bool = ...):
        """
        更新鼠标位置并返回 lParam。
        """
        ...

    def mouse_up(self, x: int = ..., y: int = ..., key: str = ...):
        """
        模拟鼠标释放。

        参数:
            x (int): x 坐标。
            y (int): y 坐标。
            key (str): 鼠标键。
        """
        ...

    def should_capture(self) -> bool:
        """
        检查是否应该捕获。

        返回:
            bool: 如果应该捕获返回 True，否则返回 False。
        """
        ...

    def on_visible(self, visible: bool):
        """
        窗口可见性改变时执行的操作。

        参数:
            visible (bool): 窗口是否可见。
        """
        ...

    def move_mouse_relative(self, dx: int, dy: int):
        """
        相对于当前位置移动鼠标。

        参数:
            dx (int): 水平移动量。
            dy (int): 垂直移动量。
        """
        ...

    def do_move_mouse_relative(self, dx: int, dy: int):
        """
        执行相对于当前位置移动鼠标操作。
        """
        ...


def is_cuda_12_or_above() -> bool:
    """
    检查 CUDA 版本是否大于等于 12.0。

    返回:
        bool: 如果 CUDA 版本大于等于 12.0 返回 True，否则返回 False。
    """
    ...


class ForegroundPostMessageInteraction(GenshinInteraction):
    """
    前台 PostMessage 交互类。
    """

    def __init__(self, capture: BaseCaptureMethod, hwnd_window: HwndWindow):
        """
        初始化 ForegroundPostMessageInteraction 实例。

        参数:
            capture (BaseCaptureMethod): 捕获方法。
            hwnd_window (HwndWindow): 窗口句柄对象。
        """
        ...

    def clickable(self) -> bool:
        """
        检查是否可点击（前台）。

        返回:
            bool: 如果可点击返回 True，否则返回 False。
        """
        ...

    def should_capture(self) -> bool:
        """
        检查是否应该捕获。

        返回:
            bool: 如果应该捕获返回 True，否则返回 False。
        """
        ...

    def on_run(self):
        """
        运行时执行的操作。
        """
        ...


def read_from_json(coco_json, width: int = ..., height: int = ...) -> tuple[dict, dict, Optional[bool], bool]:
    """
    从 JSON 文件读取特征数据。

    参数:
        coco_json (str): JSON 文件路径。
        width (int): 目标宽度。
        height (int): 目标高度。

    返回:
        tuple[dict, dict, Optional[bool], bool]: 特征字典、Box 字典、是否压缩和加载是否成功。
    """
    ...


def load_json(coco_json):
    """
    加载 JSON 文件。
    """
    ...


def un_fk_label_studio_path(path: str) -> str:
    """
    修复 Label Studio 路径。

    参数:
        path (str): 原始路径。

    返回:
        str: 修复后的路径。
    """
    ...


def adjust_coordinates(x, y, w, h, screen_width: int, screen_height: int, image_width: int, image_height: int,
                       hcenter: bool = ...) -> tuple[int, int, int, int, float]:
    """
    调整坐标以适应屏幕尺寸。

    参数:
        x: 原始 x 坐标。
        y: 原始 y 坐标。
        w: 原始宽度。
        h: 原始高度。
        screen_width (int): 屏幕宽度。
        screen_height (int): 屏幕高度。
        image_width (int): 图像宽度。
        image_height (int): 图像高度。
        hcenter (bool): 是否水平居中。

    返回:
        tuple[int, int, int, int, float]: 调整后的坐标 (x, y, w, h) 和缩放因子。
    """
    ...


def scale_by_anchor(x, image_width: int, screen_width: int, scale: float, hcenter: bool = ...) -> int:
    """
    按锚点缩放坐标。
    """
    ...


def replace_extension(filename: str) -> tuple[str, bool]:
    """
    替换文件扩展名。

    参数:
        filename (str): 文件名。

    返回:
        tuple[str, bool]: 新的文件名和是否替换成功。
    """
    ...


def filter_and_sort_matches(result, threshold: float, w: int, h: int) -> list[tuple[tuple[int, int], float]]:
    """
    过滤并排序匹配结果。

    参数:
        result: 匹配结果。
        threshold (float): 置信度阈值。
        w (int): 模板宽度。
        h (int): 模板高度。

    返回:
        list[tuple[tuple[int, int], float]]: 过滤并排序后的匹配结果列表。
    """
    ...


def mask_white(image, lower_white: int = ...):
    """
    创建白色像素的掩码。

    参数:
        image: 输入图像。
        lower_white (int): 白色像素的下界阈值。
    """
    ...


class Feature:
    """
    表示一个特征对象。
    """

    def __init__(self, mat: np.ndarray, x: int = ..., y: int = ..., scaling: float = ...):
        """
        初始化 Feature 实例。

        参数:
            mat (np.ndarray): 特征图像。
            x (int): x 坐标。
            y (int): y 坐标。
            scaling (float): 缩放比例。
        """
        ...

    @property
    def width(self) -> int:
        """
        获取特征宽度。

        返回:
            int: 宽度。
        """
        ...

    @property
    def height(self) -> int:
        """
        获取特征高度。

        返回:
            int: 高度。
        """
        ...

    def scaling(self) -> float:
        """
        获取缩放比例。

        返回:
            float: 缩放比例。
        """
        ...


class MainWindow(MSFluentWindow):
    """
    主窗口类。
    """

    def __init__(self, app: App, config: dict, ok_config: Config, icon: QIcon, title: str, version: str,
                 debug: bool = ..., about: Optional[str] = ..., exit_event: Optional[ExitEvent] = ...,
                 global_config: Optional[GlobalConfig] = ...):
        """
        初始化 MainWindow 实例。

        参数:
            app (App): 应用程序实例。
            config (dict): 配置字典。
            ok_config (Config): OK 配置。
            icon (QIcon): 窗口图标。
            title (str): 窗口标题。
            version (str): 应用程序版本。
            debug (bool): 是否处于调试模式。
            about (Optional[str]): 关于信息。
            exit_event (Optional[ExitEvent]): 可选的退出事件。
            global_config (Optional[GlobalConfig]): 可选的全局配置。
        """
        ...

    def setMicaEffectEnabled(self, isEnabled: bool):
        """
        启用或禁用 Mica 效果。
        """
        ...

    def on_tray_icon_activated(self, reason):
        """
        处理系统托盘图标激活事件。
        """
        ...

    def _onThemeChangedFinished(self):
        """
        主题改变完成时执行的操作。
        """
        ...

    def goto_global_config(self, key):
        """
        跳转到全局配置页面。
        """
        ...

    def tray_quit(self):
        """
        通过系统托盘退出应用程序。
        """
        ...

    def must_update(self):
        """
        显示必须更新的消息。
        """
        ...

    def show_ok(self):
        """
        显示 OK 消息。
        """
        ...

    def showEvent(self, event: QEvent):
        """
        处理窗口显示事件。
        """
        ...

    def set_window_size(self, width: int, height: int, min_width: int, min_height: int):
        """
        设置窗口尺寸。

        参数:
            width (int): 窗口宽度。
            height (int): 窗口高度。
            min_width (int): 最小宽度。
            min_height (int): 最小高度。
        """
        ...

    def do_check_auth(self):
        """
        执行授权检查。
        """
        ...

    def show_act(self):
        """
        显示激活窗口。
        """
        ...

    def eventFilter(self, obj, event):
        """
        事件过滤器。
        """
        ...

    def update_ok_config(self):
        """
        更新 OK 配置中的窗口信息。
        """
        ...

    def starting_emulator(self, done: bool, error, seconds_left: int):
        """
        处理模拟器启动状态。
        """
        ...

    def config_validation(self, message: str):
        """
        显示配置验证错误消息。
        """
        ...

    def show_notification(self, message: str, title: Optional[str] = ..., error: bool = ..., tray: bool = ...,
                          show_tab: Optional[str] = ...):
        """
        显示通知。
        """
        ...

    def capture_error(self):
        """
        显示捕获错误消息。
        """
        ...

    def navigate_tab(self, index: str):
        """
        导航到指定选项卡。
        """
        ...

    def executor_paused(self, paused: bool):
        """
        执行器暂停状态改变时执行的操作。
        """
        ...

    def closeEvent(self, event: QEvent):
        """
        处理窗口关闭事件。
        """
        ...


def kill_exe(relative_path: Optional[str] = ..., abs_path: Optional[str] = ...):
    """
    杀死匹配可执行文件路径的进程。

    参数:
        relative_path (Optional[str]): 可执行文件的相对路径。
        abs_path (Optional[str]): 可执行文件的绝对路径。
    """
    ...


def read_game_gpu_pref(game_executable_path) -> tuple[Optional[bool], Optional[bool]]:
    """
    检查特定游戏可执行文件的 GPU 偏好设置。

    参数:
        game_executable_path (str): 游戏可执行文件的完整路径。

    返回:
        tuple[Optional[bool], Optional[bool]]: 一个元组，包含 Auto HDR 是否启用和 SwapEffectUpgradeEnable 是否启用，如果设置未找到则返回 None。
    """
    ...


def parse_arguments_to_map(description: str = ...) -> dict:
    """
    解析命令行参数并返回字典。

    参数:
        description (str): 描述。

    返回:
        dict: 参数字典。
    """
    ...


def parse_reg_value(directx_string: str, the_key: str):
    """
    解析注册表值字符串。
    """
    ...


def read_global_gpu_pref() -> tuple[Optional[bool], Optional[bool]]:
    """
    读取全局 GPU 偏好设置。

    返回:
        tuple[Optional[bool], Optional[bool]]: 一个元组，包含 Auto HDR 是否启用和 SwapEffectUpgradeEnable 是否启用，如果设置未找到则返回 None。
    """
    ...


def get_first_gpu_free_memory_mib() -> int:
    """
    获取第一个可用 NVIDIA GPU 的空闲内存（MiB）。

    返回:
        int: 空闲内存（MiB），如果获取失败则返回 -1。
    """
    ...


class DiagnosisTask(BaseTask):
    """
    诊断任务类（性能测试）。
    """

    def __init__(self, *args, **kwargs):
        """
        初始化 DiagnosisTask 实例。
        """
        ...

    def run(self):
        """
        执行诊断任务。
        """
        ...


def get_median(my_list: list) -> float:
    """
    计算列表中值的中间值。

    参数:
        my_list (list): 输入列表。

    返回:
        float: 中间值，如果列表为空则返回 0。
    """
    ...


def get_current_process_memory_usage() -> tuple[float, float, Optional[float]]:
    """
    获取当前进程的内存使用情况。

    返回:
        tuple[float, float, Optional[float]]: 一个元组，包含驻留集大小 (RSS)、虚拟内存大小 (VMS) 和共享内存 (SHM)（MB）。
    """
    ...


def get_language_fallbacks(locale_name: str) -> list[str]:
    """
    为给定区域设置名称（如 'en_US'）生成回退列表。

    参数:
        locale_name (str): 区域设置名称。

    返回:
        list[str]: 区域设置回退列表。
    """
    ...
