from pydantic import BaseModel, Field


class MessageEvent(BaseModel):
    """消息体数据模型"""

    SenderUID: int = Field(default=0, alias="sender_uid", description="发送人的uid")
    SendToUID: int = Field(
        default=0, alias="send_to_uid", description="发送目标用户的uid"
    )
    Content: str = Field(default="", alias="content", description="消息内容")
    Timestamp: int = Field(default=0, alias="timestamp", description="时间戳")

    def is_empty(self) -> bool:
        """判断消息是否为空"""
        return self.Timestamp == 0
