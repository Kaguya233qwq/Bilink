import inspect
import functools
from typing import TYPE_CHECKING, Callable
from collections.abc import Coroutine
from .matcher import MatchType, Matcher

if TYPE_CHECKING:
    from ..bot import Bot


class _Handler:
    """
    消息处理器
    """

    def __init__(self) -> None:
        self.handle_list: list[
            tuple[
                str,
                tuple[object, ...],
                Callable[[Matcher], Coroutine[object, object, object]],
                tuple[str, ...],
            ]
        ] = []
        self.cron_list: list[
            tuple[str, Callable[["Bot"], Coroutine[object, object, object]]]
        ] = []

    def register(self, match_type: str = MatchType.NEW_MSG, *params: object):
        """
        装饰器：注册一个handler
        """

        def decorator(callback_func: Callable[..., Coroutine[object, object, object]]):
            if match_type == MatchType.CRON:
                cron_expr = str(params[0]) if params else ""
                self.cron_list.append((cron_expr, callback_func))
                return callback_func

            signature = inspect.signature(callback_func)
            callback_params = tuple(
                [param.name for param in signature.parameters.values()]
            )

            @functools.wraps(callback_func)
            async def wrapper(matcher: Matcher) -> object:
                return await callback_func(matcher)

            self.handle_list.append(
                (match_type, params, callback_func, callback_params)
            )  # type: ignore
            return wrapper

        return decorator

    async def handle_all(self, matcher: Matcher) -> None:
        """
        尝试触发消息处理器列表中的所有注册的handler
        """
        from ..utils.logger import Logger

        for handler_item in self.handle_list:
            matcher_method: Callable[[tuple[object, ...]], bool] = getattr(  # pyright: ignore[reportAny]
                matcher, handler_item[0]
            )
            # 调用注册的matcher中的匹配方法
            if matcher_method(handler_item[1]):
                # 如果为True，则触发回调函数
                try:
                    await handler_item[2](matcher)  # pyright: ignore[reportUnusedCallResult]
                except Exception as e:
                    Logger.error(f"插件 {handler_item[2].__name__} 执行出错: {e}")

    def start_cron_jobs(self, bot: "Bot") -> None:
        """
        启动所有通过 CRON 注册的定时任务 (需要 aiocron 模块)
        """
        if not self.cron_list:
            return

        import aiocron
        from ..utils.logger import Logger

        for cron_expr, callback_func in self.cron_list:
            # 允许 cron 函数接收 bot 作为参数，如果参数为空则不传
            signature = inspect.signature(callback_func)

            async def cron_wrapper(func=callback_func, sig=signature):
                try:
                    if len(sig.parameters) > 0:
                        await func(bot)
                    else:
                        await func()
                except Exception as e:
                    Logger.error(f"定时任务 {func.__name__} 执行出错: {e}")

            aiocron.crontab(cron_expr, func=cron_wrapper, start=True)
            Logger.info(f"已启动定时任务: {callback_func.__name__} [{cron_expr}]")


handler = _Handler()
