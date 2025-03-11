import os

import numpy as np

from src.GenshinInteractionLocal import GenshinInteraction

version = "v5.0.11"

def make_bottom_right_black(frame):
    """
    Changes a portion of the frame's pixels at the bottom right to black.

    Args:
        frame: The input frame (NumPy array) from OpenCV.

    Returns:
        The modified frame with the bottom-right corner blackened.  Returns the original frame
        if there's an error (e.g., invalid frame).
    """
    try:
        height, width = frame.shape[:2]  # Get height and width

        # Calculate the size of the black rectangle
        black_width = int(0.13 * width)
        black_height = int(0.025 * height)

        # Calculate the starting coordinates of the rectangle
        start_x = width - black_width
        start_y = height - black_height

        # Create a black rectangle (NumPy array of zeros)
        black_rect = np.zeros((black_height, black_width, frame.shape[2]), dtype=frame.dtype)  # Ensure same dtype

        # Replace the bottom-right portion of the frame with the black rectangle
        frame[start_y:height, start_x:width] = black_rect

        return frame
    except Exception as e:
        print(f"Error processing frame: {e}")
        return frame

config = {
    'debug': False,  # Optional, default: False
    'use_gui': True,
    'config_folder': 'configs',
    'gui_icon': 'icon.png',
    'debug_cover_uid': True,
    'screenshot_processor': make_bottom_right_black,
    'template_matching': {
        'coco_feature_json': os.path.join('assets', 'result.json'),
        'default_horizontal_variance': 0.002,
        'default_vertical_variance': 0.002,
        'default_threshold': 0.8,
    },
    'ocr': {
        'lib': 'rapidocr_openvino',
        'target_height': 540
    },
    'windows': {  # required  when supporting windows game
        'exe': ['GenshinImpact.exe', 'YuanShen.exe'],
        # 'calculate_pc_exe_path': calculate_pc_exe_path,
        # 'hwnd_class': 'UnrealWindow',
        'interaction': GenshinInteraction,
        'can_bit_blt': True,  # default false, opengl games does not support bit_blt
        # 'bit_blt_render_full': True,
        'check_hdr': True,
        'force_no_hdr': False,
        # 'check_night_light': True,
        'force_no_night_light': False,
        'require_bg': True
    },
    'start_timeout': 120,  # default 60
    'wait_until_before_delay': 0,  # default 1 , for wait_until() function
    'wait_until_check_delay': 0,
    # 'template_matching': {
    #     'coco_feature_json': os.path.join('assets', 'result.json'),
    #     'default_horizontal_variance': 0.003,
    #     'default_vertical_variance': 0.003,
    #     'default_threshold': 0.78,
    # },
    'window_size': {
        'width': 1200,
        'height': 800,
        'min_width': 600,
        'min_height': 450,
    },
    'supported_resolution': {
        'ratio': '16:9',
        'min_size': (1280, 720),
    },
    'git_update': {'sources': [{
        'name': 'Global',
        'git_url': 'https://github.com/ok-oldking/ok-genshin-impact.git',
        'pip_url': 'https://pypi.org/simple/'
        },
        {
            'name': '阿里云',
            'git_url': 'https://e.coding.net/g-frfh1513/ok-wuthering-waves/ok-gi.git',
            'pip_url': 'https://mirrors.aliyun.com/pypi/simple'
        },
        {
            'name': '清华大学',
            'git_url': 'https://e.coding.net/g-frfh1513/ok-wuthering-waves/ok-gi.git',
            'pip_url': 'https://pypi.tuna.tsinghua.edu.cn/simple'
        },
        {
            'name': '腾讯云',
            'git_url': 'https://e.coding.net/g-frfh1513/ok-wuthering-waves/ok-gi.git',
            'pip_url': 'https://mirrors.cloud.tencent.com/pypi/simple'
        },
    ]},
    'screenshots_folder': "screenshots",
    'gui_title': 'OK-GI',  # Optional
    # 'coco_feature_folder': get_path(__file__, 'assets/coco_feature'),  # required if using feature detection
    'log_file': 'logs/ok-ww.log',  # Optional, auto rotating every day
    'error_log_file': 'logs/ok-ww_error.log',
    'version': version,
    'onetime_tasks': [  # tasks to execute
        ["src.tasks.DailyTask", "DailyTask"],
        ["src.tasks.FarmRelicTask", "FarmRelicTask"],
    ],
    'trigger_tasks': [  # tasks to execute
        ["src.tasks.AutoPickTask", "AutoPickTask"],
        ["src.tasks.AutoDialogTask", "AutoDialogTask"],
        ["src.tasks.AutoLoginTask", "AutoLoginTask"],
    ],
    'my_app': ['src.globals', 'Globals'],
}
