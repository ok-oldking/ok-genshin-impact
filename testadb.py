# from adbutils import adb
import os

import adbutils
from adbutils._utils import _get_bin_dir

bin_dir = _get_bin_dir()
exe = os.path.join(bin_dir, "adb.exe" if os.name == 'nt' else 'adb')
from adbutils._utils import _is_valid_exe

if os.path.isfile(exe) and _is_valid_exe(exe):
    os.environ['ADBUTILS_ADB_PATH'] = exe
adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
print(adb.list())
d = adb.connect('127.0.0.1:16384')
d = adb.device(serial='127.0.0.1:16384')

print(type(d))

png_data = d.shell("screencap -p", encoding=None)
png_data = d.shell("screencap -p", encoding=None)
print(len(png_data))
