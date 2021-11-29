import utime


ERROR = 40
WARNING = 30
INFO = 20
DEBUG = 10


class Logger:
    def __init__(self, name, level=INFO):
        self.name = name
        self.file = None
        self.level = level

    def open(self):
        if self.file is None:
            self.file = open("{}.log".format(self.name), "w")

    def close(self):
        if self.file:
            self.file.close()
            self.file = None

    def __enter__(self):
        self.open()

    def __exit__(self):
        self.close()

    def log(self, msg):
        tt = utime.localtime()[3:6]
        prefix = "{:02d}:{:02d}.{:02d} ".format(*tt)
        print(prefix + msg)
        self.file.write(prefix + msg + "\n")
        self.file.flush()

    def error(self, msg):
        self.log("ERROR: " + msg)

    def warn(self, msg):
        if (self.level > WARNING):
            return
        self.log("WARN: " + msg)

    def info(self, msg):
        if (self.level > INFO):
            return
        self.log("INFO: " + msg)

    def debug(self, msg):
        if (self.level > DEBUG):
            return
        self.log("DEBUG: " + msg)
