import subprocess
from WindowCapture import WindowCapture
import time
from pathlib import Path


def main(qmk_msys_exe: Path, qmk_dir: Path, keymap_dir: Path):
    # open qmk and wait for it to start
    results = subprocess.Popen(
        qmk_msys_exe,
    )

    # identify qmk terminal
    qmk_window = None
    while qmk_window == None:
        try:
            qmk_window = WindowCapture('bash')
        except Exception as e:
            print("Can't find qmk terminal")
            time.sleep(2)

    # convert json to c
    qmk_window.send_command(
        f'qmk json2c {(keymap_dir / "keymap.json").as_posix()} -o {(keymap_dir / "keymap.c").as_posix()}'
    )

    # todo build with qmk
    # todo copy resulting bin file


if __name__ == '__main__':
    qmk_exe_path = 'C:\QMK_MSYS\conemu\ConEmu64.exe'
    keymap_json_path = '../src/preonic_rev3_qitbit_keymap.json'
    keymap_c_path = '../src/qitbit/keymap.c'
    main(qmk_exe_path, keymap_json_path, keymap_c_path)
