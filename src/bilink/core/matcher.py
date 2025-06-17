import re
from re import Pattern
from typing import AnyStr
from .message import Message, send_text_msg


class MatchType:
    """
    消息匹配类型
    """

    NEW_MSG = "new_msg"
    STARTS_WITH = "starts_with"
    ENDS_WITH = "ends_with"
    CONTAINS = "contains"
    SEND_BY_USER = "send_by_user"
    REGEX = "regex"


class Matcher:
    """
    消息匹配器
    """

    def __init__(self, message: Message):
        self.message = message
        self.is_new_msg = self.message.is_new_msg()

    def get_msg(self) -> Message:
        """获取当前消息对象"""
        return self.message

    def get_msg_content(self) -> Message:
        """获取当前消息"""
        return self.message.Content

    def get_msg_sender(self) -> str:
        """获取当前消息发送者的UID"""
        return self.message.SenderUID

    def get_msg_send_to(self) -> str:
        """获取当前消息发送目标的UID"""
        return self.message.SendToUID

    def get_msg_timestamp(self) -> int:
        """获取当前消息的时间戳"""
        return self.message.Timestamp

    def new_msg(self, _) -> bool:
        """如果是新消息且不是bot自己的消息时"""
        return self.is_new_msg

    def starts_with(self, content: str) -> bool:
        """如果消息以指定内容开头时"""
        return self.is_new_msg and self.message.Content.startswith(content)

    def ends_with(self, content: str) -> bool:
        """如果消息以指定内容结尾时"""
        return self.is_new_msg and self.message.Content.endswith(content)

    def contains(self, content: str) -> bool:
        """如果消息内容中包含指定内容时"""
        return self.is_new_msg and content in self.message.Content

    def send_by_user(self, user_id: str) -> bool:
        """如果发送人为指定用户时"""
        return self.is_new_msg and self.message.SenderUID == user_id

    def regex(self, pattern: Pattern[AnyStr]) -> bool:
        """如果消息匹配指定正则表达式"""
        return self.is_new_msg and bool(re.findall(pattern, self.message.Content))

    async def reply(self, content: str) -> None:
        """回复消息"""
        await send_text_msg(content, self.message.SenderUID)
