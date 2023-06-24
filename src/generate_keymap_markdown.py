import json
import pathlib

# read keymap from json file
keymap_path = pathlib.Path(
    'C:/Users/denni/Desktop/Programming/Keyboard-Firmware/Preonic/src/qitbit/keymap.json')
with open(keymap_path) as file:
    keymap = json.load(file)['layers']


max_row_size = 12  # todo read this value from a keymap file

# todo generate corresponding markdown
for index, layer in enumerate(keymap):
    organized_layer = []

    # split layer into rows
    row = []
    for key in layer:
        if len(row) == max_row_size:
            organized_layer.append(row)
            row = []
        row.append(key)
    organized_layer.append(row)
