from ..core.handler import handler
from ..core.matcher import MatchType
from ..core.message import send_text_msg


@handler.register(MatchType.STARTS_WITH, "你好")
def send():

    # 处理其他逻辑
    # ...
    # 发送消息
    send_text_msg("你好呀", "")
