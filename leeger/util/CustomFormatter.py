import logging


class CustomFormatter(logging.Formatter):
    """
    Logging colored formatter, adapted from https://stackoverflow.com/a/56944256/3638629
    """

    grey = "\x1b[38;21m"
    blue = "\x1b[38;5;39m"
    yellow = "\x1b[38;5;226m"
    red = "\x1b[38;5;196m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    def __init__(self, formatStr: str, timeFormatStr: str):
        super().__init__()
        self.__formatStr = formatStr
        self.__timeFormatStr = timeFormatStr
        self.FORMATS = {
            logging.DEBUG: self.grey + self.__formatStr + self.reset,
            logging.INFO: self.blue + self.__formatStr + self.reset,
            logging.WARNING: self.yellow + self.__formatStr + self.reset,
            logging.ERROR: self.red + self.__formatStr + self.reset,
            logging.CRITICAL: self.bold_red + self.__formatStr + self.reset,
        }

    def format(self, record):
        logFormat = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(logFormat, self.__timeFormatStr)
        return formatter.format(record)
