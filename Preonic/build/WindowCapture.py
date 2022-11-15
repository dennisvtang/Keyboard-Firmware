import win32gui
import win32com.client


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
        # make window active
        win32gui.SetForegroundWindow(self.hwnd)

        # setup window to allow communication
        shell = win32com.client.Dispatch('WScript.Shell')

        # send command
        shell.SendKeys(command)
        if send_enter:
            shell.SendKeys('{ENTER}')
