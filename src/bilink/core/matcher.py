from re import Pattern
import re
from typing import AnyStr
from .message import Message

class MatchType:
    """
    消息匹配类型
    """
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

    def starts_with(self, content: str) -> bool:
        """如果消息以指定内容开头时"""
        return self.message.is_new_msg() and self.message.Content.startswith(content)
    
    def ends_with(self, content: str) -> bool:
        """如果消息以指定内容结尾时"""
        return self.message.is_new_msg() and self.message.Content.endswith(content)
    
    def contains(self, content: str) -> bool:
        """如果消息内容中包含指定内容时"""
        return self.message.is_new_msg() and content in self.message.Content

    def send_by_user(self, user_id: str) -> bool:
        """如果发送人为指定用户时"""
        return self.message.is_new_msg() and self.message.SenderUID == user_id

    def regex(self, pattern: Pattern[AnyStr]) -> bool:
        """如果消息匹配指定正则表达式"""
        return self.message.is_new_msg() and bool(re.findall(pattern, self.message.Content))