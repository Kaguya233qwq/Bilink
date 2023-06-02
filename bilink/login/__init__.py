import asyncio
from typing import Union

from .qr_scan import login_by_qrcode
from ..utils.logger import Logger


def login():
    """
    通用bilibili登录
    :return:
    """
