import os.path
import time, sys

multiprocessing_mode = False


def read_logpath(default=None):
    if not multiprocessing_mode:
        return default
    cfgfile = ".logpath"
    logpath = default
    if os.path.isfile(cfgfile):
        with open(cfgfile) as f:
            logpath = f.read()
    return logpath


def save_logpath(logpath):
    if not multiprocessing_mode:
        return
    cfgfile = ".logpath"
    if logpath != None:
        with open(cfgfile, "w") as f:
            f.write(logpath)


class Logger:
    _instance = None
    level = 6
    defpath = "D:/pyscript.log" if os.path.isdir("D:/") else "/tmp/pyscript.log"
    logpath = defpath
    logpath = read_logpath(default=logpath)  # share in multiprocessing

    def __new__(self, *args, **kw):  # single instance
        self._instance = object.__new__(self) if self._instance is None else self._instance
        return self._instance

    def __init__(self, logpath=None):
        self.logpath = logpath if logpath != None else self.logpath
        save_logpath(logpath)

    def set_level(self, level):
        self.level = level
        return self  # support currying

    def clear(self):
        with open(self.logpath, "w") as f:
            f.write("{}\n".format(time.strftime("==== %Y-%m-%d %H:%M:%S ====", time.localtime())))
        return self  # support currying

    def log(self, msg, level, banner, path=None):
        frame = sys._getframe(2)
        newmsg = "{}{}[{}:{}] {}".format(time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime()), banner, os.path.basename(frame.f_code.co_filename), frame.f_lineno, msg)
        path = self.logpath if path == None else path
        try:
            with open(path, "a") as f:
                f.write("{}\n".format(newmsg))
        except Exception as e:
            print("Path {} open failed, error {}".format(path, e))
        finally:
            self.level >= level and print(newmsg)

    def dbg(self, msg, path=None):
        self.log(msg, 7, "[Debug]", path)

    def info(self, msg, path=None):
        self.log(msg, 6, "[Info]", path)

    def err(self, msg, path=None):
        self.log(msg, 4, "[Error]", path)
