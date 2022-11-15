import win32gui
import win32api
import win32con


class WindowCapture:
    def __init__(self, window_name):
        # find the handle for the window we want to capture
        self.hwnd = win32gui.FindWindow(None, window_name)
        if not self.hwnd:
            self.list_window_names()
            raise Exception('Window not found: {}'.format(window_name))

    # find the name of the window you're interested in.
    # once you have it, update window_capture()
    # https://stackoverflow.com/questions/55547940/how-to-get-a-list-of-the-name-of-every-open-window
    def list_window_names(self):
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                print(hex(hwnd), win32gui.GetWindowText(hwnd))
        win32gui.EnumWindows(winEnumHandler, None)

    def send_command(self, command, send_enter=True):
        # https://gist.github.com/chriskiehl/2906125
        VK_CODE = {
            'key_backspace': 0x08,
            'key_tab': 0x09,
            'key_clear': 0x0C,
            'key_enter': 0x0D,
            'key_shift': 0x10,
            'key_ctrl': 0x11,
            'key_alt': 0x12,
            'key_pause': 0x13,
            'key_caps_lock': 0x14,
            'key_esc': 0x1B,
            'key_spacebar': 0x20,
            'key_page_up': 0x21,
            'key_page_down': 0x22,
            'key_end': 0x23,
            'key_home': 0x24,
            'key_left_arrow': 0x25,
            'key_up_arrow': 0x26,
            'key_right_arrow': 0x27,
            'key_down_arrow': 0x28,
            'key_select': 0x29,
            'key_print': 0x2A,
            'key_execute': 0x2B,
            'key_print_screen': 0x2C,
            'key_ins': 0x2D,
            'key_del': 0x2E,
            'key_help': 0x2F,
            '0': 0x30,
            '1': 0x31,
            '2': 0x32,
            '3': 0x33,
            '4': 0x34,
            '5': 0x35,
            '6': 0x36,
            '7': 0x37,
            '8': 0x38,
            '9': 0x39,
            'a': 0x41,
            'b': 0x42,
            'c': 0x43,
            'd': 0x44,
            'e': 0x45,
            'f': 0x46,
            'g': 0x47,
            'h': 0x48,
            'i': 0x49,
            'j': 0x4A,
            'k': 0x4B,
            'l': 0x4C,
            'm': 0x4D,
            'n': 0x4E,
            'o': 0x4F,
            'p': 0x50,
            'q': 0x51,
            'r': 0x52,
            's': 0x53,
            't': 0x54,
            'u': 0x55,
            'v': 0x56,
            'w': 0x57,
            'x': 0x58,
            'y': 0x59,
            'z': 0x5A,
            'numpad_0': 0x60,
            'numpad_1': 0x61,
            'numpad_2': 0x62,
            'numpad_3': 0x63,
            'numpad_4': 0x64,
            'numpad_5': 0x65,
            'numpad_6': 0x66,
            'numpad_7': 0x67,
            'numpad_8': 0x68,
            'numpad_9': 0x69,
            'key_multiply': 0x6A,
            'key_add': 0x6B,
            'key_separator': 0x6C,
            'key_subtract': 0x6D,
            'key_decimal': 0x6E,
            'key_divide': 0x6F,
            'F1': 0x70,
            'F2': 0x71,
            'F3': 0x72,
            'F4': 0x73,
            'F5': 0x74,
            'F6': 0x75,
            'F7': 0x76,
            'F8': 0x77,
            'F9': 0x78,
            'F10': 0x79,
            'F11': 0x7A,
            'F12': 0x7B,
            'F13': 0x7C,
            'F14': 0x7D,
            'F15': 0x7E,
            'F16': 0x7F,
            'F17': 0x80,
            'F18': 0x81,
            'F19': 0x82,
            'F20': 0x83,
            'F21': 0x84,
            'F22': 0x85,
            'F23': 0x86,
            'F24': 0x87,
            'key_num_lock': 0x90,
            'key_scroll_lock': 0x91,
            'key_left_shift': 0xA0,
            'key_right_shift ': 0xA1,
            'key_left_control': 0xA2,
            'key_right_control': 0xA3,
            'key_left_menu': 0xA4,
            'key_right_menu': 0xA5,
            'key_browser_back': 0xA6,
            'key_browser_forward': 0xA7,
            'key_browser_refresh': 0xA8,
            'key_browser_stop': 0xA9,
            'key_browser_search': 0xAA,
            'key_browser_favorites': 0xAB,
            'key_browser_start_and_home': 0xAC,
            'key_volume_mute': 0xAD,
            'key_volume_Down': 0xAE,
            'key_volume_up': 0xAF,
            'key_next_track': 0xB0,
            'key_previous_track': 0xB1,
            'key_stop_media': 0xB2,
            'key_play/pause_media': 0xB3,
            'key_start_mail': 0xB4,
            'key_select_media': 0xB5,
            'key_start_application_1': 0xB6,
            'key_start_application_2': 0xB7,
            'key_attn': 0xF6,
            'key_crsel': 0xF7,
            'key_exsel': 0xF8,
            'key_play': 0xFA,
            'key_zoom': 0xFB,
            'key_clear': 0xFE,
            '+': 0xBB,
            ',': 0xBC,
            '-': 0xBD,
            '.': 0xBE,
            '/': 0xBF,
            '`': 0xC0,
            ';': 0xBA,
            '[': 0xDB,
            '\\': 0xDC,
            ']': 0xDD,
            "'": 0xDE,
            '`': 0xC0
        }

        for char in command:
            win32api.PostMessage(
                self.hwnd,
                win32con.WM_CHAR,
                VK_CODE[char],
                0
            )
        if send_enter:
            win32api.PostMessage(
                self.hwnd,
                win32con.WM_CHAR,
                VK_CODE['key_enter'],
                0
            )
