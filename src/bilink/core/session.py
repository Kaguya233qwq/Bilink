import time


class MessageManager:
    """消息管理器"""

    def __init__(self):
        self.session_timestamps: dict[int, int] = {}
        self.startup_time: int = int(time.time())

    def check_is_new(self, user_id: int, timestamp: int) -> bool:
        last_ts = self.session_timestamps.get(user_id, self.startup_time)
        return timestamp > last_ts

    def update_latest(self, user_id: int, timestamp: int) -> None:
        self.session_timestamps[user_id] = timestamp


message_manager = MessageManager()
