import datetime
from colorama import init

init(autoreset=True)


class Logger(object):
    """日志类"""

    @classmethod
    def message(cls, message):
        """
        输出收到的消息

        :param message: 收到的消息
        :return:
        """
        results = cls.formatter(
            '\033[1;4;33m%s\033[0m',
            '[MESSAGE]',
            message
        )
        print(results)

    @classmethod
    def auto(cls, message):
        """
        输出自动回复的消息

        :param message: 自动回复的消息
        :return:
        """
        results = cls.formatter(
            '\033[1;4;32m%s\033[0m',
            '[AUTO]',
            message
        )
        print(results)

    @classmethod
    def success(cls, message):
        """
        输出成功信息

        :param message: 成功信息
        :return:
        """
        results = cls.formatter(
            '\033[1;32m%s\033[0m',
            '[SUCCESS]',
            message
        )
        print(results)

    @classmethod
    def info(cls, message):
        """
        输出程序运行详细信息

        :param message: 详细信息
        :return:
        """
        results = cls.formatter(
            '\033[1;34m%s\033[0m',
            '[INFO]',
            message
        )
        print(results)

    @classmethod
    def warning(cls, message):
        """
        输出程序运行警告信息

        :param message: 警告信息
        :return:
        """
        results = cls.formatter(
            '\033[1;33m%s\033[0m',
            '[WARNING]',
            message
        )
        print(results)

    @classmethod
    def error(cls, message):
        """
        输出程序运行错误信息

        :param message: 错误信息
        :return:
        """
        results = cls.formatter(
            '\033[1;31m%s\033[0m',
            '[ERROR]',
            message
        )
        print(results)

    @classmethod
    def fatal(cls, message):
        """
        输出程序运行严重错误信息

        :param message: 严重错误信息
        :return:
        """
        results = cls.formatter(
            '\033[1;35m%s\033[0m',
            '[FATAL]',
            message)
        print(results)

    @classmethod
    def formatter(cls, colors, types, message):
        """
        更改控制台输出的日志颜色并格式化

        :param colors: 颜色
        :param message:提示信息
        :param types: 日志等级
        :return:
        """
        times = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatter = '%s-%s' % (times, colors % types) + message
        return formatter
