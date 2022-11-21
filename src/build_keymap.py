import subprocess
from WindowCapture import WindowCapture
import time
from pathlib import Path
import shutil


def main(qmk_msys_exe_path: Path, qmk_home_dir: Path, keymap_dir: Path, keyboard_name: str):
    # open qmk
    print('Opening qmk terminal')
    results = subprocess.Popen(
        qmk_msys_exe_path,
    )

    # wait until qmk terminal is open
    print('Waiting until qmk terminal is opened')
    qmk_window = None
    while qmk_window == None:
        try:
            qmk_window = WindowCapture('bash')
        except Exception as e:
            print('- Waiting')
            time.sleep(2)

    # convert json to c
    print('Converting json keymap to c file for firmware')
    qmk_window.send_command(
        f'qmk json2c {(keymap_dir / "keymap.json").as_posix()} -o {(keymap_dir / "keymap.c").as_posix()}'
    )

    # copy keymap to path qmk can access
    print('Copying keymap to path qmk can access')
    qmk_keyboards_dir = qmk_home_dir / 'keyboards'
    assert qmk_keyboards_dir / keyboard_name.parent in [keyboard for keyboard in qmk_keyboards_dir.iterdir()],  \
        'Specified keyboard not found in qmk dir'
    shutil.copytree(
        keymap_dir,
        qmk_keyboards_dir / keyboard_name.parent / 'keymaps' / keymap_dir.name,
        dirs_exist_ok=True,
    )

    # compile firmware with qmk
    print('Compiling firmware')
    qmk_window.send_command(
        f'qmk compile -kb {keyboard_name.as_posix()} -km {keymap_dir.name}'
    )
    # wait until qmk is finished compiling
    compiled_filename = f'{keyboard_name.parent}_{keyboard_name.name}_{keymap_dir.name}.bin'
    compiled_firmware_path = qmk_home_dir / compiled_filename
    while not compiled_firmware_path.is_file():
        time.sleep(1)
        print('- Waiting')
    print('- Finished')

    # move firmware to repo
    print('Moving firmware to repo')
    output_path = keymap_dir.parent.parent / 'dist' / compiled_filename
    shutil.move(compiled_firmware_path, output_path)

    # close qmk terminal
    qmk_window.close_window()


if __name__ == '__main__':
    import argparse
    import os

    arg_parser = argparse.ArgumentParser(
        description='',
    )
    arg_parser.add_argument(
        '--qmk_msys_exe_path',
        help='path to QMK MSYS executable',
        required=True,
        type=Path
    )
    arg_parser.add_argument(
        '--qmk_home_dir',
        help='qmk home directory, in QMK MSYS running `qmk env` can tell you this',
        required=True,
        type=Path
    )
    arg_parser.add_argument(
        '--keymap_dir',
        help='directory of keymap to compile',
        required=True,
        type=Path
    )
    arg_parser.add_argument(
        '--keyboard_name',
        help='name of the keyboard compiling firmware fore',
        required=True,
        type=Path
    )
    script_path = Path(os.getcwd())

    args = arg_parser.parse_args()

    main(
        args.qmk_msys_exe_path,
        args.qmk_home_dir,
        args.keymap_dir,
        args.keyboard_name,
    )
