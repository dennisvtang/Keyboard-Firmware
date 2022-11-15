import subprocess
from WindowCapture import WindowCapture
import time


def main(qmk_exe_path: str, keymap_json_path: str, keymap_c_path: str):
    # open qmk and wait for it to start
    results = subprocess.Popen(
        qmk_exe_path,
        shell=True,
    )
    time.sleep(1)

    # identify qmk terminal
    qmk_window = WindowCapture('bash')

    # convert json to c
    qmk_window.send_command(
        f'qmk json2c {keymap_json_path} -o {keymap_c_path}'
    )

    # todo build with qmk
    # todo copy resulting bin file


if __name__ == '__main__':
    qmk_exe_path = 'C:\QMK_MSYS\conemu\ConEmu64.exe'
    keymap_json_path = '../src/preonic_rev3_qitbit_keymap.json'
    keymap_c_path = '../src/qitbit/keymap.c'
    main(qmk_exe_path, keymap_json_path, keymap_c_path)
