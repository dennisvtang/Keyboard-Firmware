import win32gui
import win32com.client
import time


class WindowCapture:
    def __init__(self, window_name):
        # find the handle for the window we want to capture
        self.hwnd = win32gui.FindWindow(None, window_name)
        if not self.hwnd:
            window_names = self.get_window_names()
            exception_message = '\n'.join(window_names)
            exception_message += f'\nWindow "{window_name}" not found above are the windows found'
            raise Exception(
                exception_message
            )

    # find the name of the window you're interested in.
    # once you have it, update window_capture()
    # https://stackoverflow.com/questions/55547940/how-to-get-a-list-of-the-name-of-every-open-window
    def get_window_names(self):
        def winEnumHandler(hwnd, extra_args):
            # only get windows that are visible
            if win32gui.IsWindowVisible(hwnd):
                window_names.append(
                    f'{hex(hwnd)} {win32gui.GetWindowText(hwnd)}'
                )
        window_names = []

        # enumerate top-level windows on screen with a callback function
        win32gui.EnumWindows(winEnumHandler, None)

        return window_names

    def send_command(self, command, send_enter=True):
        # make window active
        win32gui.SetForegroundWindow(self.hwnd)

        # setup window to allow communication
        shell = win32com.client.Dispatch('WScript.Shell')

        # send command
        for char in command:
            shell.SendKeys(char)
            time.sleep(0.01)
        if send_enter:
            shell.SendKeys('{ENTER}')
