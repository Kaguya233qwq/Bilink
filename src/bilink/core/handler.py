import inspect
from typing import Callable, List, Tuple
from .matcher import MatchType, Matcher


class _Handler:
    """
    消息处理器
    """

    def __init__(self) -> None:
        self.handle_list: List[Tuple[MatchType, Tuple]] = []

    def register(self, match_type: MatchType, *params) -> None:
        """
        装饰器：注册一个handler
        """
        def decorator(callback_func):
            signature = inspect.signature(callback_func)
            callback_params = tuple([param.name for param in signature.parameters.values()])
            async def wrapper(*args, **kwargs):
                await callback_func(*args, **kwargs)

            self.handle_list.append(
                    (match_type, params, callback_func, callback_params)
                )
            return wrapper

        return decorator

    async def handle_all(self, matcher: Matcher) -> None:
        """
        尝试触发消息处理器列表中的所有注册的handler
        """
        for handler in self.handle_list:
            matcher_method: Callable = getattr(matcher, handler[0])
            # 调用注册的matcher中的匹配方法
            if matcher_method(handler[1]):
                # 如果为True，则触发回调函数
                await handler[2](matcher)


handler = _Handler()
