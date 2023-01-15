import os
import sys
import time
from threading import Thread

import sty
from sty import fg, rs
import colorsys


class Rainbow:
    def __init__(self, text: str, speed: float = 1):
        self.lines = [text.replace("\n", "").replace("\r", "")] if IS_PYCHARM else text.split("\n")
        self.speed = speed
        self.strength = 3
        self.vertical_strength = 1
        self.update_delay = 1 / 30
        self.hue = 0
        self.running = False

    def get_color(self, i: int):
        hue = (self.hue + i * self.strength) % 256

        return map(lambda x: int(x * 255), colorsys.hsv_to_rgb(hue / 255, 1, 1))

    def increase_hue(self):
        self.hue += self.speed * self.update_delay * 100
        self.hue %= 256

    def get_rainbowed_text(self):
        if not SUPPORTS_ANSI:
            # ignore color
            return "\n".join(self.lines)

        return "\n".join(
            ["".join(
                [fg(*self.get_color(i + j * self.vertical_strength)) + char for i, char in enumerate(line)]
            ) for j, line in enumerate(self.lines)]
        ) + rs.fg

    def loop(self):
        while self.running:
            # print with rainbow
            print("\r" + self.get_rainbowed_text(), end="", flush=True)

            # go up one line for every \n that is used
            if len(self.lines) - 1 >= 1:
                print(f"\u001b[{len(self.lines) - 1}F", end="", flush=True)

            # increase hue
            self.increase_hue()

            # sleep
            time.sleep(self.update_delay)

    def start(self):
        self.running = True
        t = Thread(target=self.loop)
        t.daemon = True
        t.start()

    def stop(self):
        self.running = False
        print("\n" * len(self.lines))


def rainbow(text: str, speed: float = 1):
    rainbow_obj = Rainbow(text, speed)
    rainbow_obj.start()

    return rainbow_obj


def windows_stdout(text: str):
    # this prints a \n so we need to move one line up
    os.system(f"@echo {text}\u001b[1F")


def cmd_enable_ansi():
    # this is somewhat undocumented, an empty string printed will enable ansi support for cmds
    windows_stdout("")


def windows_check_for_ansi_support():
    from ctypes import LibraryLoader, wintypes
    import ctypes

    windll = LibraryLoader(ctypes.WinDLL)

    std_handle = windll.kernel32.GetStdHandle(-11)  # stdout

    mode = wintypes.DWORD()

    out = windll.kernel32.GetConsoleMode(std_handle, ctypes.byref(mode))

    if out == 0:
        # error
        return False

        # noinspection PyUnreachableCode
        errno = windll.kernel32.GetLastError()

        print(f"GetConsoleMode failed: {errno=}")

        # don't ask why the size is 101, I copied it from the official example
        size = 100 + 1
        err_message_buffer = ctypes.create_string_buffer(size)

        FORMAT_MESSAGE_FROM_SYSTEM = 0x00001000
        FORMAT_MESSAGE_IGNORE_INSERTS = 0x00000200

        err_message_len = windll.kernel32.FormatMessageA(
            FORMAT_MESSAGE_FROM_SYSTEM | FORMAT_MESSAGE_IGNORE_INSERTS,  # dwFlags
            None,  # lpSource = ignored
            errno,  # dwMessageId
            0,  # dwLanguageId = default (0)
            err_message_buffer,  # lpBuffer = where our message goes
            size,  # nSize = the size of our message buffer
            0  # va_list: *Arguments = ignored?
        )

        if err_message_len == 0:
            # error
            print(f"FormatMessage failed: {err_message_len=}")
        else:
            print(f"ErrorMessage: {err_message_buffer[:err_message_len].decode()}")

        # out = win32api.FormatMessage(errno)
        # print(f"ErrorMessage: {out}")
    else:
        # print(f"{out=}")

        mode = mode.value

        # print(f"mode={bin(mode)}")
        if 0x0001 & mode:
            return True
            # print(f"* ANSI is enabled")
            # print("\u001b[38;2;255;182;135mbefore additional enable\u001b[39m")
            # windows_enable_ansi_lol()
            # print("\u001b[38;2;255;182;135mafter additional enable\u001b[39m")
            # print(Rainbow('RAINBOW TEST').get_rainbowed_text())


def check_for_support():
    global SUPPORTS_ANSI, IS_PYCHARM

    IS_PYCHARM = 'PYCHARM_HOSTED' in os.environ and os.environ['PYCHARM_HOSTED'] == '1'

    if (hasattr(sys.stdout, "isatty") and sys.stdout.isatty()) or \
            ('TERM' in os.environ and os.environ['TERM'] == 'ANSI') or IS_PYCHARM:
        # terminal supposedly supports ansi
        SUPPORTS_ANSI = True

    else:
        # terminal doesn't supports ansi
        SUPPORTS_ANSI = False

    if os.name == "nt":
        # on cmds we need to "enable" ansi support
        cmd_enable_ansi()


def stderr_print(text, **kwargs):
    if SUPPORTS_ANSI:
        print(sty.fg.red + text + sty.rs.fg, **kwargs, file=sys.stderr)
    else:
        print(text, **kwargs, file=sys.stderr)


def rainbow_print(text, **kwargs):
    global __HUE
    if SUPPORTS_ANSI:
        r = Rainbow(text)
        r.hue = __HUE
        r.strength = 4
        __HUE += len(text)
        print(r.get_rainbowed_text(), **kwargs)
    else:
        print(text, **kwargs, file=sys.stderr)


# def win_next_red():
#     if os.name != "nt":
#         return
#     from ctypes import LibraryLoader, WinDLL
#
#     windll = LibraryLoader(WinDLL)
#     std_err_handle = windll.kernel32.GetStdHandle(-12)
#
#     windll.kernel32.SetConsoleTextAttribute(std_err_handle, FOREGROUND_RED)
__HUE = 0
IS_PYCHARM = True
SUPPORTS_ANSI = None
check_for_support()
