import re
from typing import TYPE_CHECKING
from ..events.message import MessageEvent
from ..events.segment import MessageSegment

if TYPE_CHECKING:
    from ..bot import Bot


class MatchType:
    """
    消息匹配类型
    """

    NEW_MSG: str = "new_msg"
    STARTS_WITH: str = "starts_with"
    ENDS_WITH: str = "ends_with"
    CONTAINS: str = "contains"
    SEND_BY_USER: str = "send_by_user"
    REGEX: str = "regex"
    CRON: str = "cron"


class Matcher:
    """
    消息匹配器
    """

    def __init__(self, bot: "Bot", message: MessageEvent):
        self.bot: "Bot" = bot
        self.message: MessageEvent = message
        self.is_new_msg: bool = True

    def get_msg(self) -> MessageEvent:
        """获取当前消息对象"""
        return self.message

    def get_msg_content(self) -> str:
        """获取当前消息"""
        return self.message.Content

    def get_msg_sender(self) -> int:
        """获取当前消息发送者的UID"""
        return self.message.SenderUID

    def get_msg_send_to(self) -> int:
        """获取当前消息发送目标的UID"""
        return self.message.SendToUID

    def get_msg_timestamp(self) -> int:
        """获取当前消息的时间戳"""
        return self.message.Timestamp

    def new_msg(self, _: object) -> bool:
        """如果是新消息且不是bot自己的消息时"""
        return self.is_new_msg

    def starts_with(self, params: tuple[object, ...]) -> bool:
        """如果消息以指定内容开头时"""
        content = str(params[0]) if params else ""
        return self.is_new_msg and self.message.Content.startswith(content)

    def ends_with(self, params: tuple[object, ...]) -> bool:
        """如果消息以指定内容结尾时"""
        content = str(params[0]) if params else ""
        return self.is_new_msg and self.message.Content.endswith(content)

    def contains(self, params: tuple[object, ...]) -> bool:
        """如果消息内容中包含指定内容时"""
        content = str(params[0]) if params else ""
        return self.is_new_msg and content in self.message.Content

    def send_by_user(self, params: tuple[object, ...]) -> bool:
        """如果发送人为指定用户时"""
        user_id = int(str(params[0])) if params else 0
        return self.is_new_msg and self.message.SenderUID == user_id

    def regex(self, params: tuple[object, ...]) -> bool:
        """如果消息匹配指定正则表达式"""
        pattern = str(params[0]) if params else ""
        return self.is_new_msg and bool(re.findall(pattern, self.message.Content))

    async def reply(self, content: str | MessageSegment) -> None:
        """统一回复消息段"""
        api = getattr(self.bot, "api")  # type: ignore
        if isinstance(content, str):
            segment = MessageSegment.text(content)
        else:
            segment = content

        await api.send_msg(segment, self.message.SenderUID)
