import sys
import time
from .logger import Logger
from .. import message
from ..models import Message, Authorization

last_timestamp: int
last_sender_uid: str


async def run():
    global last_timestamp,last_sender_uid
    Logger.info("bilibili消息助手正在运行...")
    try:
        while True:
            if (
                    Message.Timestamp != last_timestamp
                    and Message.SenderUid != Authorization.SelfUid
            ):
                Logger.message(f"用户[{Message.SenderUid}]:{Message.MsgContent}")
                if '你好' in Message.MsgContent:
                    await message.send_text_msg(
                        '(*´▽｀)ノノ你好鸭~~',

                    )
            last_timestamp = Message.Timestamp
            time.sleep(2)
    except KeyboardInterrupt:
        Logger.info('进程终止')
        sys.exit()
