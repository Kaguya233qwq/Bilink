import json
from typing import Any


class MessageSegment:
    """消息段对象，用于构建不同类型的回复内容"""

    def __init__(self, msg_type: int, data: dict[str, Any]):
        self.msg_type = msg_type
        self.data = data

    @property
    def content_str(self) -> str:
        """返回构建给API用的JSON字符串格式内容"""
        return json.dumps(self.data)

    @classmethod
    def text(cls, text: str) -> "MessageSegment":
        """纯文本消息段"""
        return cls(msg_type=1, data={"content": text})

    @classmethod
    def image(cls, url: str) -> "MessageSegment":
        """图片消息段"""
        return cls(msg_type=2, data={"url": url})

    @classmethod
    def video_card(cls, title: str, bvid: str, thumb: str) -> "MessageSegment":
        """视频分享卡片"""
        return cls(
            msg_type=7,
            data={"title": title, "bvid": bvid, "thumb": thumb, "source": 5, "id": 0},
        )
