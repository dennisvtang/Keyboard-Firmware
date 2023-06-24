import json
import pathlib

# read keymap from json file
keymap_path = pathlib.Path(
    'C:/Users/denni/Desktop/Programming/Keyboard-Firmware/Preonic/src/qitbit/keymap.json')
with open(keymap_path) as file:
    keymap = json.load(file)['layers']
print(json.dumps(keymap, indent=4, default=str))

# todo convert lists to markdown
