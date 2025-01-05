from asyncio import sleep

from .message import Message, fetch_msg
from .matcher import Matcher, MatchType
from .handler import handler


async def run():
    """轮询获取最新消息并进行比对"""
    while True:
        # 获取并初始化最新的消息
        msg: Message = await fetch_msg()
        # 实例化一个matcher，匹配消息内容
        matcher = Matcher(msg)
        # 注册处理函数
        handler.add_handler(MatchType.STARTS_WITH, matcher, "你好")
        await sleep(2)
