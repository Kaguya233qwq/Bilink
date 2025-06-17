from ..core.handler import handler
from ..core.matcher import Matcher

from typing import Dict, List
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionChunk

client = AsyncOpenAI(
    base_url="", # OpenAI API的基础URL，所有兼容OpenAI API的服务都可以使用
    api_key="", # OpenAI API的密钥
)

messages = [
    {
        "role": "system",
        "content": "你是一个可爱的虚拟up主[妍妍]，你会耐心回答你的粉丝的问题，并适当使用emoji来渲染情绪。",
    }
]


async def call_openai(
    content: str, messages: List[Dict[str, str]]
) -> ChatCompletionChunk:
    messages.append({"role": "user", "content": content})

    return await client.chat.completions.create(
        # 指定你的模型
        model="",
        messages=messages,
    )


# 注册一个处理器，匹配所有非系统消息
@handler.register()
async def ai_handler(matcher: Matcher):
    # 接收所有的非系统消息，传入ai对话
    completion = await call_openai(matcher.get_msg_content(), messages)
    if completion.choices[0].message.content:
        # 如果有内容则回复
        await matcher.reply(completion.choices[0].message.content)
