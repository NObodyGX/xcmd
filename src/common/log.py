import logging
import os
import threading


class ColorText(object):
    _black = 30
    _red = 31
    _green = 32
    _yellow = 33
    _blue = 34
    _purple = 35
    _cyan = 36
    _grey = 37

    @staticmethod
    def render(text, color=None) -> str:
        if color is None:
            return text
        return f"\033[{color}m{text}\033[0m"

    @staticmethod
    def red(text) -> str:
        return ColorText.render(text, ColorText._red)

    @staticmethod
    def yellow(text) -> str:
        return ColorText.render(text, ColorText._yellow)

    @staticmethod
    def green(text) -> str:
        return ColorText.render(text, ColorText._green)

    @staticmethod
    def cyan(text) -> str:
        return ColorText.render(text, ColorText._cyan)

    @staticmethod
    def blue(text) -> str:
        return ColorText.render(text, ColorText._blue)

    @staticmethod
    def grey(text) -> str:
        return ColorText.render(text, ColorText._grey)

    @staticmethod
    def black(text):
        return ColorText.render(text, ColorText._black)


class Glog(object):
    _instance = None
    _lock = threading.Lock()

    @classmethod
    def instance(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.logger = logging.getLogger("dir_toy")
        self.logger.setLevel(logging.DEBUG)
        mode = "a"
        self.enable_f = False
        # 文件输出
        if self.enable_f:
            fullname = os.path.join(os.getcwd(), "..", "logs", f"coomer.log")
            if not os.path.exists(os.path.dirname(fullname)):
                os.makedirs(os.path.dirname(fullname))
            fmt = "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s"
            formatter = logging.Formatter(fmt)
            fh = logging.FileHandler(fullname, mode=mode, encoding="utf-8")
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(formatter)
        # 往屏幕上输出
        nfmt = "%(message)s"
        nfmtter = logging.Formatter(nfmt)
        sh = logging.StreamHandler()
        sh.setLevel(logging.DEBUG)
        sh.setFormatter(nfmtter)
        # 先清空handler, 再添加
        self.logger.handlers = []
        if self.enable_f:
            self.logger.addHandler(fh)
        self.logger.addHandler(sh)

    def error(self, msg: str, keyword="error"):
        self.logger.error(f"[{ColorText.red(keyword)}] {msg}")

    def warn(self, msg: str, keyword="warn"):
        self.logger.warn(f"[{ColorText.yellow(keyword)}] {msg}")

    def info(self, msg: str, keyword="info"):
        self.logger.info(f"[{ColorText.cyan(keyword)}] {msg}")

    def debug(self, msg: str, keyword="debug"):
        self.logger.debug(f"[{ColorText.grey(keyword)}] {msg}")

    def success(self, msg: str, keyword="success"):
        self.logger.info(f"[{ColorText.green(keyword)}] {msg}")

    def meta(self, msg: str, keyword="meta"):
        self.logger.info(f"[{ColorText.blue(keyword)}] {msg}")

    def page(self, msg: str, keyword="page"):
        self.logger.info(f"[{ColorText.cyan(keyword)}] {msg}")

    def welcome(self, name: str):
        self.logger.info(f"💢 欢迎使用 {ColorText.yellow(name)} 💢")
