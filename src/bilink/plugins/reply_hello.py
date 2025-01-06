from ..core.handler import handler
from ..core.matcher import MatchType, Matcher


@handler.register(MatchType.STARTS_WITH, "你好")
async def say_hello(matcher: Matcher):

    # 处理其他逻辑
    # ...
    # 调用回复方法
    await matcher.reply("你好呀！")
