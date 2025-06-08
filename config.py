import os
import platform
import re

import numpy as np

from ok import ConfigOption

version = "v5.6.13"

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


def calculate_pc_exe_path(running_path):
    if running_path:
        return running_path
    else:
        return get_genshin_executable_path()

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
        'lib': 'rapidocr',
        'target_height': 720,
    },
    'analytics': {
        'report_url': 'http://report.ok-script.cn:8080/report',
    },
    'windows': {  # required  when supporting windows game
        'exe': ['GenshinImpact.exe', 'YuanShen.exe'],
        'calculate_pc_exe_path': calculate_pc_exe_path,
        # 'hwnd_class': 'UnrealWindow',
        'interaction': 'Genshin',
        'can_bit_blt': True,  # default false, opengl games does not support bit_blt
        'bit_blt_render_full': True,
        'check_hdr': True,
        'force_no_hdr': True,
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
        'min_width': 800,
        'min_height': 600,
    },
    'supported_resolution': {
        'ratio': '16:9',
        'min_size': (1280, 720),
        'resize_to': [(2560, 1440), (1920, 1080), (1600, 900), (1280, 720)],
    },
    'git_update': {'sources': [{
        'name': 'Global',
        'git_url': 'https://github.com/ok-oldking/ok-genshin-impact.git',
        'pip_url': 'https://pypi.org/simple/'
        },
        {
            'name': 'China',
            'git_url': 'https://cnb.cool/ok-oldking/ok-genshin-impact.git',
            'pip_url': 'https://mirrors.aliyun.com/pypi/simple'
        }
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
        ["ok", "DiagnosisTask"],
    ],
    'trigger_tasks': [  # tasks to execute
        ["src.tasks.AutoPickTask", "AutoPickTask"],
        ["src.tasks.AutoCombatTask", "AutoCombatTask"],
        ["src.tasks.AutoDialogTask", "AutoDialogTask"],
        ["src.tasks.AutoLoginTask", "AutoLoginTask"],
    ],
    'my_app': ['src.globals', 'Globals'],
    'global_configs': [auto_combat_config],
}


def get_genshin_executable_path():
    """
    Attempts to locate the Genshin Impact executable path.

    This function tries several methods to find the game's installation directory
    and then constructs the full path to the executable.  It prioritizes Steam installs.

    Returns:
        str: The full path to the Genshin Impact executable, or None if not found.
    """

    # 1. Try to find it in Steam
    steam_path = find_steam_game_path("Genshin Impact")
    if steam_path:
        return steam_path

    # 2. Try to find it in the Windows registry (if on Windows)
    if platform.system() == "Windows":
        registry_path = get_genshin_install_path_from_registry("原神")
        if registry_path:
            executable_path = os.path.join(registry_path, 'Genshin Impact game', "YuanShen.exe")
            if os.path.exists(executable_path):
                return executable_path
            else:
                print(
                    "Warning: Registry entry found, but executable not at expected location.{}".format(executable_path))
                return None  # Or handle the error differently
        else:
            registry_path = get_genshin_install_path_from_registry("Genshin Impact")
            if registry_path:
                executable_path = os.path.join(registry_path, 'Genshin Impact game', "GenshinImpact.exe")
                if os.path.exists(executable_path):
                    return executable_path
                else:
                    print("Warning: Registry entry found, but executable not at expected location. {}".format(
                        executable_path))
                    return None  # Or handle the error differently
    else:
        print("Warning: Registry lookup is only supported on Windows.")

    # 3. Try some common installation paths (least reliable)
    common_paths = [
        r"C:\Program Files\Genshin Impact\Genshin Impact Game\GenshinImpact.exe",
        r"D:\Program Files\Genshin Impact\Genshin Impact Game\GenshinImpact.exe",
        r"C:\Program Files\Genshin Impact\GenshinImpact.exe",  # Older versions
        r"D:\Program Files\Genshin Impact\GenshinImpact.exe",  # Older versions
    ]

    for path in common_paths:
        if os.path.exists(path):
            return path

    print("Error: Genshin Impact executable not found.")
    return None


def find_steam_game_path(game_name):
    """
    Attempts to find the install location of a game via Steam's libraryfolders.vdf file.

    Args:
        game_name (str): The name of the game to search for.

    Returns:
        str: The full path to the game executable, or None if not found.
    """

    if platform.system() != "Windows":  # steam paths differ on other systems
        print("Steam path lookup only implemented for Windows at the moment")  # Add Mac/Linux support if needed
        return None

    try:
        # Find Steam's install path.  Uses a registry lookup.
        import winreg  # Requires pywin32 module: pip install pywin32
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Valve\Steam")
        steam_install_path = winreg.QueryValueEx(key, "InstallPath")[0]
        winreg.CloseKey(key)

        # Locate the libraryfolders.vdf file
        libraryfolders_path = os.path.join(steam_install_path, "config", "libraryfolders.vdf")

        if not os.path.exists(libraryfolders_path):
            print("Error: libraryfolders.vdf not found.")
            return None

        with open(libraryfolders_path, "r", encoding="utf-8") as f:
            vdf_content = f.read()

        # Regular expression to find appID
        game_appid = None
        if game_name == "Genshin Impact":
            game_appid = '2094880'  # Hardcode for Genshin

        # Find install path in VDF file.  This relies on game_appid being correct!
        install_path_match = re.search(rf'"path"\s+"(.*?)"[\s\S]*?"{game_appid}"', vdf_content)

        if install_path_match:
            install_path = install_path_match.group(1)
            executable_path = os.path.join(install_path, "steamapps", "common", "Genshin Impact", "GenshinImpact.exe")
            if os.path.exists(executable_path):
                return executable_path
            else:
                executable_path = os.path.join(install_path, "steamapps", "common", "Genshin Impact", "Yuanshen.exe")
                if os.path.exists(executable_path):
                    return executable_path
                else:
                    print(f"Executable not found at {executable_path}")
                    return None

        print(f"{game_name} appID not found in libraryfolders.vdf (or is not installed).")
        return None
    except Exception as e:
        print(f"Error finding Steam game path: {e}")
        return None


def get_genshin_install_path_from_registry(name):
    """
    Retrieves the Genshin Impact installation path from the Windows registry.

    Requires the pywin32 package to be installed.  Use `pip install pywin32`.

    Returns:
        str: The installation path, or None if not found.
    """
    if platform.system() != "Windows":
        print("Warning: Registry lookup is only supported on Windows.")
        return None

    try:
        import winreg  # Requires pywin32 module: pip install pywin32
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                             r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\\" + name)
        install_path = winreg.QueryValueEx(key, "InstallPath")[0]
        winreg.CloseKey(key)
        return install_path
    except FileNotFoundError:
        print("Error: Genshin Impact registry key not found.")
        return None
    except ImportError:
        print("Error: pywin32 module not installed.  Please install it using 'pip install pywin32'.")
        return None
    except Exception as e:
        print(f"Error accessing registry: {e}")
        return None
