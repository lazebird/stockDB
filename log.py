import os.path
import time, sys


class Logger:
    _instance = None
    level = 6
    logpath = None

    def __new__(self, *args, **kw):  # single instance
        self._instance = object.__new__(self) if self._instance is None else self._instance
        return self._instance

    def __init__(self, logpath=None):
        self.logpath = logpath if logpath != None else self.logpath

    def set_level(self, level):
        self.level = level
        return self  # support currying

    def clear(self):
        if self.logpath != None:
            with open(self.logpath, "w") as f:
                f.write("{}\n".format(time.strftime("==== %Y-%m-%d %H:%M:%S ====", time.localtime())))
        return self  # support currying

    def log(self, msg, level, banner, path=None):
        frame = sys._getframe(2)
        newmsg = "{}{}[{}:{}] {}".format(time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime()), banner, os.path.basename(frame.f_code.co_filename), frame.f_lineno, msg)
        path = self.logpath if path == None else path
        if path != None:
            try:
                with open(path, "a") as f:
                    f.write("{}\n".format(newmsg))
            except Exception as e:
                print("Path {} open failed, error {}".format(path, e))
        self.level >= level and print(newmsg)

    def dbg(self, msg, path=None):
        self.log(msg, 7, "[Debug]", path)

    def info(self, msg, path=None):
        self.log(msg, 6, "[Info]", path)

    def err(self, msg, path=None):
        self.log(msg, 4, "[Error]", path)
