import subprocess
from WindowCapture import WindowCapture
import time
from pathlib import Path
import shutil


def main(qmk_msys_exe: Path, qmk_home_dir: Path, keymap_dir: Path, keyboard_name: str):
    # open qmk
    results = subprocess.Popen(
        qmk_msys_exe,
    )

    # wait until qmk terminal is open
    qmk_window = None
    while qmk_window == None:
        try:
            qmk_window = WindowCapture('bash')
        except Exception as e:
            print('Waiting for qmk terminal')
            time.sleep(2)

    # convert json to c
    qmk_window.send_command(
        f'qmk json2c {(keymap_dir / "keymap.json").as_posix()} -o {(keymap_dir / "keymap.c").as_posix()}'
    )

    # copy keymap to path qmk can access
    qmk_keyboards_dir = qmk_home_dir / 'keyboards'
    assert qmk_keyboards_dir / keyboard_name.parent in [keyboard for keyboard in qmk_keyboards_dir.iterdir()],  \
        'Specified keyboard not found in qmk dir'
    shutil.copytree(
        keymap_dir,
        qmk_keyboards_dir / keyboard_name.parent / 'keymaps' / keymap_dir.name,
        dirs_exist_ok=True,
    )

    # compile firmware with qmk
    qmk_window.send_command(
        f'qmk compile -kb {keyboard_name.as_posix()} -km {keymap_dir.name}'
    )
    # wait until qmk is finished compiling
    compiled_filename = f'{keyboard_name.parent}_{keyboard_name.name}_{keymap_dir.name}.bin'
    compiled_firmware_path = qmk_home_dir / compiled_filename
    while not compiled_firmware_path.is_file():
        time.sleep(1)
        print('waiting for firmware to be compiled')
    print('firmware finished compiling')



if __name__ == '__main__':
    qmk_exe_path = 'C:\QMK_MSYS\conemu\ConEmu64.exe'
    keymap_json_path = '../src/preonic_rev3_qitbit_keymap.json'
    keymap_c_path = '../src/qitbit/keymap.c'
    main(qmk_exe_path, keymap_json_path, keymap_c_path)
