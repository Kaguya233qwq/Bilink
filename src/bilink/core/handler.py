from typing import Callable, List, Tuple
from matcher import MatchType, Matcher


class _Handler:
    """
    消息处理器
    """
    def __init__(self) -> None:
        self.handle_list: List[Tuple[Callable, Tuple, dict]] = []

    def add_handler(self, match_type: MatchType, matcher: Matcher, *args, **kwargs) -> None:
        method: Callable = getattr(matcher, match_type)
        self.handle_list.append((method, args, kwargs))

    def handle_all(self) -> None:
        for handler in self.handle_list:
            handler[0](*handler[1], **handler[2])

handler = _Handler()
