import utime
import sys
import io


ERROR = 40
WARNING = 30
INFO = 20
DEBUG = 10


class Logger:
    def __init__(self, name=None, level=INFO):
        """
        Inititalizes a new logger. if `name` is `None` then it will print to stdout.
        """
        self.name = name
        self.file = None
        self.level = level
        self.open()

    def open(self):
        if self.file is None:
            if self.name is None:
                self.file = sys.stdout
            else:
                self.file = open("{}.log".format(self.name), "at")

    def close(self):
        if self.file:
            if self.name is not None:
                self.file.close()
            self.file = None

    def __enter__(self):
        self.open()

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def log(self, msg):
        tt = utime.localtime()[3:6]
        prefix = "{:02d}:{:02d}.{:02d} ".format(*tt)
        print(prefix + msg)
        self.file.write(prefix + msg + "\n")
        if hasattr(self.file, "flush"):
            self.file.flush()

    def error(self, msg, exception=None):
        if (exception is not None):
            output = io.StringIO()
            sys.print_exception(exception, output)
            msg = msg + " " + output.getvalue()
            output.close()

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
