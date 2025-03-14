import os

import numpy as np

from ok import ConfigOption

version = "v0.0.24"

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


auto_combat_config = ConfigOption('Auto Combat Config', {
    'Combat Sequence': '1EQ2EQ3EQ4EQ',
}, config_description={
    'Combat Sequence': 'Number = Switch, E = Elemental Skill(L = Long Press),\n Q = Elemental Burst, A = Normal Attack,\n best to use a shielder first'
},
                                  description='How to Combat')

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
        'target_height': 540,
        # 'det_model_path': os.path.join('assets', 'ocr_models', 'en_PP-OCRv3_det_infer.onnx'),
        # 'rec_model_path': os.path.join('assets', 'ocr_models', 'en_PP-OCRv4_rec_infer.onnx'),
        # 'rec_keys_path': os.path.join('assets', 'ocr_models', 'ppocr_keys_v1.txt'),
    },
    'windows': {  # required  when supporting windows game
        'exe': ['GenshinImpact.exe', 'YuanShen.exe'],
        # 'calculate_pc_exe_path': calculate_pc_exe_path,
        # 'hwnd_class': 'UnrealWindow',
        'interaction': 'Genshin',
        'can_bit_blt': True,  # default false, opengl games does not support bit_blt
        # 'bit_blt_render_full': True,
        'check_hdr': True,
        'force_no_hdr': False,
        # 'check_night_light': True,
        'force_no_night_light': False,
        'require_bg': True
    },
    'links': {
        'default': {
            'github': 'https://github.com/ok-oldking/ok-genshin-impact',
            'discord': 'https://discord.gg/Q8utYcPQA3',
            'share': 'Download OK-WW from https://github.com/ok-oldking/ok-genshin-impact/releases/latest',
            'faq': 'https://github.com/ok-oldking/ok-genshin-impact#FAQ'
        },
        'zh_CN': {
            'github': 'https://github.com/ok-oldking/ok-genshin-impact',
            'discord': 'https://discord.gg/Q8utYcPQA3',
            'share': 'OK-WW 夸克网盘下载：https://pan.quark.cn/s/75b55ef72a34 GitHub下载: https://github.com/ok-oldking/ok-genshin-impact/releases/latest',
            'qq_channel': 'https://pd.qq.com/s/e2wvbypn7',
            'faq': 'https://g-frfh1513.coding.net/p/ok-wuthering-waves/d/ok-gi/git/tree/master/README_CN.md#FAQ',
        },
    },
    'about': """
        <p style="color:red;">
        <strong>本软件是免费的。</strong> 如果你被收费，请立即退款。请访问GitHub下载最新的官方版本。
        </p>
        <p style="color:red;">
            <strong>本软件仅供个人使用，用于学习Python编程、计算机视觉、UI自动化等。</strong> 请勿将其用于任何营利性或商业用途。
        </p>
        <p style="color:red;">
            <strong>使用本软件可能会导致账号被封。</strong> 请在了解风险后再使用。
        </p>
    """,
    'start_timeout': 120,  # default 60
    'wait_until_settle_time': 0,
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
        ["src.tasks.ClaimDailyRewardTask", "ClaimDailyRewardTask"],
        ["src.tasks.CraftResinTask", "CraftResinTask"],
    ],
    'trigger_tasks': [  # tasks to execute
        ["src.tasks.AutoPickTask", "AutoPickTask"],
        ["src.tasks.AutoDialogTask", "AutoDialogTask"],
        ["src.tasks.AutoLoginTask", "AutoLoginTask"],
        ["src.tasks.AutoCombatTask", "AutoCombatTask"],
    ],
    'my_app': ['src.globals', 'Globals'],
    'global_configs': [auto_combat_config],
}
