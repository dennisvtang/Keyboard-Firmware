import subprocess
from WindowCapture import WindowCapture
import time


def main(qmk_exe_path: str):
    # open qmk and wait for it to start
    results = subprocess.Popen(
        qmk_exe_path,
        shell=True,
    )
    time.sleep(1)

    # identify qmk terminal
    qmk_window = WindowCapture('bash')
    # todo convert json to c
    # todo copy results
    # todo overwrite keymap.c
    # todo build with qmk
    # todo copy resulting bin file


if __name__ == '__main__':
    qmk_exe_path = 'C:\QMK_MSYS\conemu\ConEmu64.exe'
    main(qmk_exe_path)
