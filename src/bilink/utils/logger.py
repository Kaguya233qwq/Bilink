import inspect
import logging
from typing import Literal


class Logger:
    """
    控制台日志类
    """

    def __init__(self) -> None:
        self.caller_frame = inspect.stack()[1]  # 获取调用者的帧
        self.caller_module = inspect.getmodule(self.caller_frame[0])  # 获取调用者的模块
        self.caller_filename = self.caller_frame[1]  # 调用者的文件名
        self.caller_lineno = self.caller_frame[2]  # 调用者的行号

    __logger = logging.getLogger(__name__)
    __handler = logging.StreamHandler()
    __handler.setLevel(logging.INFO)
    __logger.setLevel(logging.INFO)
    __logger.addHandler(__handler)

    def get_caller(self):
        """
        获取模块调用信息
        """
        print(
            f"Called from module {self.caller_module.__name__} in file {self.caller_filename}, line {self.caller_lineno}"
        )

    @classmethod
    def set_level(
        cls, level: Literal["NOTSET", "DEBUG", "INFO", "WARN", "ERROR", "FATAL"]
    ):
        """
        设置日志优先级别 一般默认为INFO
        """
        cls.__logger.setLevel(level)
        cls.__handler.setLevel(level)

    @classmethod
    def success(cls, message: str):
        """
        输出程序执行成功信息
        """
        cls.__handler.setFormatter(
            logging.Formatter("%(asctime)s - \033[0;32m[SUCCESS]\033[0m :  %(message)s")
        )
        cls.__logger.info(message)

    @classmethod
    def info(cls, message: str):
        """
        输出程序执行信息
        """
        cls.__handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - \033[0;36m[%(levelname)s]\033[0m :  %(message)s"
            )
        )
        cls.__logger.info(message)

    @classmethod
    def warning(cls, message: str):
        """
        输出警告信息
        """
        cls.__handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - \033[0;33m[%(levelname)s]\033[0m :  %(message)s"
            )
        )
        cls.__logger.warning(message)

    @classmethod
    def error(cls, message: str):
        """
        输出错误信息
        """
        cls.__handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - \033[0;31m[%(levelname)s]\033[0m :  %(message)s"
            )
        )
        cls.__logger.error(message)

    @classmethod
    def fatal(cls, message: str):
        """
        输出致命异常信息
        """
        cls.__handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - \033[1;31m[%(levelname)s]\033[0m :  %(message)s"
            )
        )
        cls.__logger.fatal(message)

    @classmethod
    def debug(cls, message: str):
        """
        输出调试信息
        """
        cls.__handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - \033[0;37m[%(levelname)s]\033[0m :  %(message)s"
            )
        )
        cls.__logger.debug(message)
