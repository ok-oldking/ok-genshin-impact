import codecs
import os
import re
import typing as t
import winreg
from dataclasses import dataclass

from ok.alas.utils import iter_folder


def abspath(path):
    return os.path.abspath(path)


def get_serial_pair(serial):
    """
    Args:
        serial (str):

    Returns:
        str, str: `127.0.0.1:5555+{X}` and `emulator-5554+{X}`, 0 <= X <= 32
    """
    if serial.startswith('127.0.0.1:'):
        try:
            port = int(serial[10:])
            if 5555 <= port <= 5555 + 32:
                return f'127.0.0.1:{port}', f'emulator-{port - 1}'
        except (ValueError, IndexError):
            pass
    if serial.startswith('emulator-'):
        try:
            port = int(serial[9:])
            if 5554 <= port <= 5554 + 32:
                return f'127.0.0.1:{port + 1}', f'emulator-{port}'
        except (ValueError, IndexError):
            pass

    return None, None


def remove_duplicated_path(paths):
    """
    Args:
        paths (list[str]):

    Returns:
        list[str]:
    """
    paths = sorted(set(paths))
    dic = {}
    for path in paths:
        dic.setdefault(path.lower(), path)
    return list(dic.values())


@dataclass
class EmulatorInstanceBase:
    # Serial for adb connection
    serial: str
    # Emulator instance name, used for start/stop emulator
    name: str
    # Path to emulator .exe
    path: str

    def __str__(self):
        return f'{self.type}(serial="{self.serial}", name="{self.name}", path="{self.path}")'

    @property
    def type(self) -> str:
        """
        Returns:
            str: Emulator type, such as Emulator.NoxPlayer
        """
        return self.emulator.type

    @property
    def emulator(self):
        """
        Returns:
            Emulator:
        """
        return EmulatorBase(self.path)

    def __eq__(self, other):
        if isinstance(other, str) and self.type == other:
            return True
        if isinstance(other, list) and self.type in other:
            return True
        if isinstance(other, EmulatorInstanceBase):
            return super().__eq__(other) and self.type == other.type
        return super().__eq__(other)

    def __hash__(self):
        return hash(str(self))

    def __bool__(self):
        return True

    @property
    def MuMuPlayer12_id(self):
        """
        Convert MuMu 12 instance name to instance id.
        Example names:
            MuMuPlayer-12.0-3
            YXArkNights-12.0-1

        Returns:
            int: Instance ID, or None if this is not a MuMu 12 instance
        """
        res = re.search(r'MuMuPlayer(?:Global)?-12.0-(\d+)', self.name)
        if res:
            return int(res.group(1))
        res = re.search(r'YXArkNights-12.0-(\d+)', self.name)
        if res:
            return int(res.group(1))

        return None

    @property
    def player_id(self):

        # Find all integer groups in the string that are at the end of the string
        integers = re.findall(r'\d+$', self.name)
        # Return the last integer if it exists, otherwise return 0
        return int(integers[0]) if integers else 0


class EmulatorBase:
    # Values here must match those in argument.yaml EmulatorInfo.Emulator.option
    NoxPlayer = 'NoxPlayer'
    NoxPlayer64 = 'NoxPlayer64'
    NoxPlayerFamily = [NoxPlayer, NoxPlayer64]
    BlueStacks4 = 'BlueStacks4'
    BlueStacks5 = 'BlueStacks5'
    BlueStacks4HyperV = 'BlueStacks4HyperV'
    BlueStacks5HyperV = 'BlueStacks5HyperV'
    BlueStacksFamily = [BlueStacks4, BlueStacks5]
    LDPlayer3 = 'LDPlayer3'
    LDPlayer4 = 'LDPlayer4'
    LDPlayer9 = 'LDPlayer9'
    LDPlayerFamily = [LDPlayer3, LDPlayer4, LDPlayer9]
    MuMuPlayer = 'MuMuPlayer'
    MuMuPlayerX = 'MuMuPlayerX'
    MuMuPlayer12 = 'MuMuPlayer12'
    MuMuPlayerFamily = [MuMuPlayer, MuMuPlayerX, MuMuPlayer12]
    MEmuPlayer = 'MEmuPlayer'

    @classmethod
    def path_to_type(cls, path: str) -> str:
        """
        Args:
            path: Path to .exe file

        Returns:
            str: Emulator type, such as Emulator.NoxPlayer,
                or '' if this is not a emulator.
        """
        return ''

    def iter_instances(self) -> t.Iterable[EmulatorInstanceBase]:
        """
        Yields:
            EmulatorInstance: Emulator instances found in this emulator
        """
        pass

    def iter_adb_binaries(self) -> t.Iterable[str]:
        """
        Yields:
            str: Filepath to adb binaries found in this emulator
        """
        pass

    def __init__(self, path):
        # Path to .exe file
        self.path = path
        # Path to emulator folder
        self.dir = os.path.dirname(path)
        # str: Emulator type, or '' if this is not a emulator.
        self.type = self.__class__.path_to_type(path)

    def __eq__(self, other):
        if isinstance(other, str) and self.type == other:
            return True
        if isinstance(other, list) and self.type in other:
            return True
        return super().__eq__(other)

    def __str__(self):
        return f'{self.type}(path="{self.path}")'

    __repr__ = __str__

    def __hash__(self):
        return hash(self.path)

    def __bool__(self):
        return True

    def abspath(self, path, folder=None):
        if folder is None:
            folder = self.dir
        return abspath(os.path.join(folder, path))

    @classmethod
    def is_emulator(cls, path: str) -> bool:
        """
        Args:
            path: Path to .exe file.

        Returns:
            bool: If this is a emulator.
        """
        return bool(cls.path_to_type(path))

    def list_folder(self, folder, is_dir=False, ext=None):
        """
        Safely list files in a folder

        Args:
            folder:
            is_dir:
            ext:

        Returns:
            list[str]:
        """
        folder = self.abspath(folder)
        return list(iter_folder(folder, is_dir=is_dir, ext=ext))


class EmulatorManagerBase:
    @staticmethod
    def iter_running_emulator():
        """
        Yields:
            str: Path to emulator executables, may contains duplicate values
        """
        return

    @property
    def all_emulators(self) -> t.List[EmulatorBase]:
        """
        Get all emulators installed on current computer.
        """
        return []

    @property
    def all_emulator_instances(self) -> t.List[EmulatorInstanceBase]:
        """
        Get all emulator instances installed on current computer.
        """
        return []

    @property
    def all_emulator_serials(self) -> t.List[str]:
        """
        Returns:
            list[str]: All possible serials on current computer.
        """
        out = []
        for emulator in self.all_emulator_instances:
            out.append(emulator.serial)
            # Also add serial like `emulator-5554`
            port_serial, emu_serial = get_serial_pair(emulator.serial)
            if emu_serial:
                out.append(emu_serial)
        return out

    @property
    def all_adb_binaries(self) -> t.List[str]:
        """
        Returns:
            list[str]: All adb binaries of emulators on current computer.
        """
        out = []
        for emulator in self.all_emulators:
            for exe in emulator.iter_adb_binaries():
                out.append(exe)
        return out


@dataclass
class RegValue:
    name: str
    value: str
    typ: int


def list_reg(reg) -> t.List[RegValue]:
    """
    List all values in a reg key
    """
    rows = []
    index = 0
    try:
        while 1:
            value = RegValue(*winreg.EnumValue(reg, index))
            index += 1
            rows.append(value)
    except OSError:
        pass
    return rows


def list_key(reg) -> t.List[RegValue]:
    """
    List all values in a reg key
    """
    rows = []
    index = 0
    try:
        while 1:
            value = winreg.EnumKey(reg, index)
            index += 1
            rows.append(value)
    except OSError:
        pass
    return rows



class EmulatorInstance(EmulatorInstanceBase):
    @property
    def emulator(self):
        """
        Returns:
            Emulator:
        """
        return Emulator(self.path)


class Emulator(EmulatorBase):
    @classmethod
    def path_to_type(cls, path: str) -> str:
        """
        Args:
            path: Path to .exe file, case insensitive

        Returns:
            str: Emulator type, such as Emulator.NoxPlayer
        """
        folder, exe = os.path.split(path)
        folder, dir1 = os.path.split(folder)
        folder, dir2 = os.path.split(folder)
        exe = exe.lower()
        dir1 = dir1.lower()
        dir2 = dir2.lower()
        if exe == 'nox.exe':
            if dir2 == 'nox':
                return cls.NoxPlayer
            elif dir2 == 'nox64':
                return cls.NoxPlayer64
            else:
                return cls.NoxPlayer
        if exe == 'bluestacks.exe':
            if dir1 in ['bluestacks', 'bluestacks_cn']:
                return cls.BlueStacks4
            elif dir1 in ['bluestacks_nxt', 'bluestacks_nxt_cn']:
                return cls.BlueStacks5
            else:
                return cls.BlueStacks4
        if exe == 'hd-player.exe':
            if dir1 in ['bluestacks', 'bluestacks_cn']:
                return cls.BlueStacks4
            elif dir1 in ['bluestacks_nxt', 'bluestacks_nxt_cn']:
                return cls.BlueStacks5
            else:
                return cls.BlueStacks5
        if exe == 'dnplayer.exe':
            if dir1 == 'ldplayer':
                return cls.LDPlayer3
            elif dir1 == 'ldplayer4':
                return cls.LDPlayer4
            elif dir1 == 'ldplayer9':
                return cls.LDPlayer9
            else:
                return cls.LDPlayer3
        if exe == 'nemuplayer.exe':
            if dir2 == 'nemu':
                return cls.MuMuPlayer
            elif dir2 == 'nemu9':
                return cls.MuMuPlayerX
            else:
                return cls.MuMuPlayer
        if exe == 'mumuplayer.exe':
            return cls.MuMuPlayer12
        if exe == 'memu.exe':
            return cls.MEmuPlayer

        return ''

    @staticmethod
    def multi_to_single(exe):
        """
        Convert a string that might be a multi-instance manager to its single instance executable.

        Args:
            exe (str): Path to emulator executable

        Yields:
            str: Path to emulator executable
        """
        if 'HD-MultiInstanceManager.exe' in exe:
            yield exe.replace('HD-MultiInstanceManager.exe', 'HD-Player.exe')
            yield exe.replace('HD-MultiInstanceManager.exe', 'Bluestacks.exe')
        elif 'MultiPlayerManager.exe' in exe:
            yield exe.replace('MultiPlayerManager.exe', 'Nox.exe')
        elif 'dnmultiplayer.exe' in exe:
            yield exe.replace('dnmultiplayer.exe', 'dnplayer.exe')
        elif 'NemuMultiPlayer.exe' in exe:
            yield exe.replace('NemuMultiPlayer.exe', 'NemuPlayer.exe')
        elif 'MuMuMultiPlayer.exe' in exe:
            yield exe.replace('MuMuMultiPlayer.exe', 'MuMuPlayer.exe')
        elif 'MuMuManager.exe' in exe:
            yield exe.replace('MuMuManager.exe', 'MuMuPlayer.exe')
        elif 'MEmuConsole.exe' in exe:
            yield exe.replace('MEmuConsole.exe', 'MEmu.exe')
        else:
            yield exe

    @staticmethod
    def vbox_file_to_serial(file: str) -> str:
        """
        Args:
            file: Path to vbox file

        Returns:
            str: serial such as `127.0.0.1:5555`
        """
        regex = re.compile('<*?hostport="(.*?)".*?guestport="5555"/>')
        try:
            with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f.readlines():
                    # <Forwarding name="port2" proto="1" hostip="127.0.0.1" hostport="62026" guestport="5555"/>
                    res = regex.search(line)
                    if res:
                        return str(f'127.0.0.1:{res.group(1)}')
            return ''
        except FileNotFoundError:
            return ''

    def iter_instances(self):
        """
        Yields:
            EmulatorInstance: Emulator instances found in this emulator
        """
        if self == Emulator.NoxPlayerFamily:
            # ./BignoxVMS/{name}/{name}.vbox
            for folder in self.list_folder('./BignoxVMS', is_dir=True):
                for file in iter_folder(folder, ext='.vbox'):
                    serial = Emulator.vbox_file_to_serial(file)
                    if serial:
                        yield EmulatorInstance(
                            serial=serial,
                            name=os.path.basename(folder),
                            path=self.path,
                        )
        elif self == Emulator.BlueStacks5:
            # Get UserDefinedDir, where BlueStacks stores data
            folder = None
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\BlueStacks_nxt") as reg:
                    folder = winreg.QueryValueEx(reg, 'UserDefinedDir')[0]
            except FileNotFoundError:
                pass
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\BlueStacks_nxt_cn") as reg:
                    folder = winreg.QueryValueEx(reg, 'UserDefinedDir')[0]
            except FileNotFoundError:
                pass
            if not folder:
                return
            # Read {UserDefinedDir}/bluestacks.conf
            try:
                with open(self.abspath('./bluestacks.conf', folder), encoding='utf-8') as f:
                    content = f.read()
            except FileNotFoundError:
                return
            # bst.instance.Nougat64.adb_port="5555"
            emulators = re.findall(r'bst.instance.(\w+).status.adb_port="(\d+)"', content)
            for emulator in emulators:
                yield EmulatorInstance(
                    serial=f'127.0.0.1:{emulator[1]}',
                    name=emulator[0],
                    path=self.path,
                )
        elif self == Emulator.BlueStacks4:
            # ../Engine/Android
            regex = re.compile(r'^Android')
            for folder in self.list_folder('../Engine', is_dir=True):
                folder = os.path.basename(folder)
                res = regex.match(folder)
                if not res:
                    continue
                # Serial from BlueStacks4 are not static, they get increased on every emulator launch
                # Assume all use 127.0.0.1:5555
                yield EmulatorInstance(
                    serial=f'127.0.0.1:5555',
                    name=folder,
                    path=self.path
                )
        elif self == Emulator.LDPlayerFamily:
            # ./vms/leidian0
            regex = re.compile(r'^leidian(\d+)$')
            for folder in self.list_folder('./vms', is_dir=True):
                folder = os.path.basename(folder)
                res = regex.match(folder)
                if not res:
                    continue
                # LDPlayer has no forward port config in .vbox file
                # Ports are auto increase, 5555, 5557, 5559, etc
                port = int(res.group(1)) * 2 + 5555
                yield EmulatorInstance(
                    serial=f'127.0.0.1:{port}',
                    name=folder,
                    path=self.path
                )
        elif self == Emulator.MuMuPlayer:
            # MuMu has no multi instances, on 7555 only
            yield EmulatorInstance(
                serial='127.0.0.1:7555',
                name='',
                path=self.path,
            )
        elif self == Emulator.MuMuPlayerX:
            # vms/nemu-12.0-x64-default
            for folder in self.list_folder('../vms', is_dir=True):
                for file in iter_folder(folder, ext='.nemu'):
                    serial = Emulator.vbox_file_to_serial(file)
                    if serial:
                        yield EmulatorInstance(
                            serial=serial,
                            name=os.path.basename(folder),
                            path=self.path,
                        )
        elif self == Emulator.MuMuPlayer12:
            # vms/MuMuPlayer-12.0-0
            for folder in self.list_folder('../vms', is_dir=True):
                for file in iter_folder(folder, ext='.nemu'):
                    serial = Emulator.vbox_file_to_serial(file)
                    if serial:
                        yield EmulatorInstance(
                            serial=serial,
                            name=os.path.basename(folder),
                            path=self.path,
                        )
        elif self == Emulator.MEmuPlayer:
            # ./MemuHyperv VMs/{name}/{name}.memu
            for folder in self.list_folder('./MemuHyperv VMs', is_dir=True):
                for file in iter_folder(folder, ext='.memu'):
                    serial = Emulator.vbox_file_to_serial(file)
                    if serial:
                        yield EmulatorInstance(
                            serial=serial,
                            name=os.path.basename(folder),
                            path=self.path,
                        )

    def iter_adb_binaries(self) -> t.Iterable[str]:
        """
        Yields:
            str: Filepath to adb binaries found in this emulator
        """
        if self == Emulator.NoxPlayerFamily:
            exe = self.abspath('./nox_adb.exe')
            if os.path.exists(exe):
                yield exe
        if self == Emulator.MuMuPlayerFamily:
            # From MuMu9\emulator\nemu9\EmulatorShell
            # to MuMu9\emulator\nemu9\vmonitor\bin\adb_server.exe
            exe = self.abspath('../vmonitor/bin/adb_server.exe')
            if os.path.exists(exe):
                yield exe

        # All emulators have adb.exe
        exe = self.abspath('./adb.exe')
        if os.path.exists(exe):
            yield exe


class EmulatorManager(EmulatorManagerBase):
    @staticmethod
    def iter_user_assist():
        """
        Get recently executed programs in UserAssist
        https://github.com/forensicmatt/MonitorUserAssist

        Yields:
            str: Path to emulator executables, may contains duplicate values
        """
        path = r'Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist'
        # {XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX}\xxx.exe
        regex_hash = re.compile(r'{.*}')
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, path) as reg:
                folders = list_key(reg)
        except FileNotFoundError:
            return

        for folder in folders:
            try:
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, f'{path}\\{folder}\\Count') as reg:
                    for key in list_reg(reg):
                        key = codecs.decode(key.name, 'rot-13')
                        # Skip those with hash
                        if regex_hash.search(key):
                            continue
                        for file in Emulator.multi_to_single(key):
                            yield file
            except FileNotFoundError:
                # FileNotFoundError: [WinError 2] 系统找不到指定的文件。
                # Might be a random directory without "Count" subdirectory
                continue

    @staticmethod
    def iter_mui_cache():
        """
        Iter emulator executables that has ever run.
        http://what-when-how.com/windows-forensic-analysis/registry-analysis-windows-forensic-analysis-part-8/
        https://3gstudent.github.io/%E6%B8%97%E9%80%8F%E6%8A%80%E5%B7%A7-Windows%E7%B3%BB%E7%BB%9F%E6%96%87%E4%BB%B6%E6%89%A7%E8%A1%8C%E8%AE%B0%E5%BD%95%E7%9A%84%E8%8E%B7%E5%8F%96%E4%B8%8E%E6%B8%85%E9%99%A4

        Yields:
            str: Path to emulator executable, may contains duplicate values
        """
        path = r'Software\Classes\Local Settings\Software\Microsoft\Windows\Shell\MuiCache'
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, path) as reg:
                rows = list_reg(reg)
        except FileNotFoundError:
            return

        regex = re.compile(r'(^.*\.exe)\.')
        for row in rows:
            res = regex.search(row.name)
            if not res:
                continue
            for file in Emulator.multi_to_single(res.group(1)):
                yield file

    @staticmethod
    def get_install_dir_from_reg(path, key):
        """
        Args:
            path (str): f'SOFTWARE\\leidian\\ldplayer'
            key (str): 'InstallDir'

        Returns:
            str: Installation dir or None
        """
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, path) as reg:
                root = winreg.QueryValueEx(reg, key)[0]
                return root
        except FileNotFoundError:
            pass
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path) as reg:
                root = winreg.QueryValueEx(reg, key)[0]
                return root
        except FileNotFoundError:
            pass

        return None

    @staticmethod
    def iter_uninstall_registry():
        """
        Iter emulator uninstaller from registry.

        Yields:
            str: Path to uninstall exe file
        """
        known_uninstall_registry_path = [
            r'SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall',
            r'Software\Microsoft\Windows\CurrentVersion\Uninstall'
        ]
        known_emulator_registry_name = [
            'Nox',
            'Nox64',
            'BlueStacks',
            'BlueStacks_nxt',
            'BlueStacks_cn',
            'BlueStacks_nxt_cn',
            'LDPlayer',
            'LDPlayer4',
            'LDPlayer9',
            'leidian',
            'leidian4',
            'leidian9',
            'Nemu',
            'Nemu9',
            'MuMuPlayer-12.0'
            'MEmu',
        ]
        for path in known_uninstall_registry_path:
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path) as reg:
                    software_list = list_key(reg)
            except FileNotFoundError:
                continue
            for software in software_list:
                if software not in known_emulator_registry_name:
                    continue
                try:
                    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, f'{path}\\{software}') as software_reg:
                        uninstall = winreg.QueryValueEx(software_reg, 'UninstallString')[0]
                except FileNotFoundError:
                    continue
                if not uninstall:
                    continue
                # UninstallString is like:
                # C:\Program Files\BlueStacks_nxt\BlueStacksUninstaller.exe -tmp
                # "E:\ProgramFiles\Microvirt\MEmu\uninstall\uninstall.exe" -u
                # Extract path in ""
                res = re.search('"(.*?)"', uninstall)
                uninstall = res.group(1) if res else uninstall
                yield uninstall

    @staticmethod
    def iter_running_emulator():
        """
        Yields:
            str: Path to emulator executables, may contains duplicate values
        """
        try:
            import psutil
        except ModuleNotFoundError:
            return
        # Since this is a one-time-usage, we access psutil._psplatform.Process directly
        # to bypass the call of psutil.Process.is_running().
        # This only costs about 0.017s.
        for pid in psutil.pids():
            proc = psutil._psplatform.Process(pid)
            try:
                exe = proc.cmdline()
                exe = exe[0]
            except (psutil.AccessDenied, psutil.NoSuchProcess, IndexError):
                # psutil.AccessDenied
                continue

            if Emulator.is_emulator(exe):
                yield exe

    @property
    def all_emulators(self) -> t.List[Emulator]:
        """
        Get all emulators installed on current computer.
        """
        exe = set([])

        # MuiCache
        for file in EmulatorManager.iter_mui_cache():
            if Emulator.is_emulator(file) and os.path.exists(file):
                exe.add(file)

        # UserAssist
        for file in EmulatorManager.iter_user_assist():
            if Emulator.is_emulator(file) and os.path.exists(file):
                exe.add(file)

        # LDPlayer install path
        for path in [r'SOFTWARE\leidian\ldplayer',
                     r'SOFTWARE\leidian\ldplayer9']:
            ld = self.get_install_dir_from_reg(path, 'InstallDir')
            if ld:
                ld = abspath(os.path.join(ld, './dnplayer.exe'))
                if Emulator.is_emulator(ld) and os.path.exists(ld):
                    exe.add(ld)

        # Uninstall registry
        for uninstall in EmulatorManager.iter_uninstall_registry():
            # Find emulator executable from uninstaller
            for file in iter_folder(abspath(os.path.dirname(uninstall)), ext='.exe'):
                if Emulator.is_emulator(file) and os.path.exists(file):
                    exe.add(file)
            # Find from parent directory
            for file in iter_folder(abspath(os.path.join(os.path.dirname(uninstall), '../')), ext='.exe'):
                if Emulator.is_emulator(file) and os.path.exists(file):
                    exe.add(file)
            # MuMu specific directory
            for file in iter_folder(abspath(os.path.join(os.path.dirname(uninstall), 'EmulatorShell')), ext='.exe'):
                if Emulator.is_emulator(file) and os.path.exists(file):
                    exe.add(file)

        # Running
        for file in EmulatorManager.iter_running_emulator():
            if os.path.exists(file):
                exe.add(file)

        # De-redundancy
        exe = [Emulator(path).path for path in exe if Emulator.is_emulator(path)]
        exe = [Emulator(path) for path in remove_duplicated_path(exe)]
        return exe

    @property
    def all_emulator_instances(self) -> t.List[EmulatorInstance]:
        """
        Get all emulator instances installed on current computer.
        """
        instances = []
        for emulator in self.all_emulators:
            instances += list(emulator.iter_instances())

        instances: t.List[EmulatorInstance] = sorted(instances, key=lambda x: str(x))
        return instances


