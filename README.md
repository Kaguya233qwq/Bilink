<div align="center">

<p align="center">
  <a href=""><img src="https://github.com/Kaguya233qwq/Bilink/blob/main/icon.png?raw=ture" width="" height="" alt="bilink"></a>
</p>

✨ 基于轮询的原生哔哩哔哩消息自动回复bot ✨_

<p align="center">
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python">
</p>

_“简单，轻量，快速”_

</div>

---

## ✨️特性概览

- 使用异步函数，轻量且快速

- 内置扫码登录，自动保存登录信息

- 插件式开发，可以模块化实现想要的功能

## 🚀快速开始

### 💿安装依赖
```bash
pdm install
```
### ▶️运行项目
```bash
pdm run python main.py
```
### 🧩插件编写

下面是一个示例插件reply_hello.py，位于bilink/plugins包：

```python

from ..core.handler import handler
from ..core.matcher import MatchType, Matcher


@handler.register(MatchType.STARTS_WITH, "你好")
async def say_hello(matcher: Matcher):

    # 处理其他逻辑
    # ...
    # 调用回复方法
    await matcher.reply("你好呀！")

```

- 使用handler.register注册一个消息处理器

其接收参数为匹配类型MatchType以及它对应的参数，一般为消息匹配参数。实例中使用了STARTS_WITH类型，并传入“你好”作为匹配参数，表示匹配以“你好”开头的所有消息。

- 注入Matcher参数

Matcher为handler装饰器目标函数所必需的一个参数，你可以使用它来回复消息，或是调用其他api。当然，你也可以什么都不做，仅仅用来占位。像这样：

```python
@handler.register(MatchType.STARTS_WITH, "你好")
async def do_nothing(_: Matcher):
    # 一个收到你好后什么都不做的handler
    pass
```

## 📃更新记录

<details>
<summary>点击展开</summary>
<p>
2025.6.17 1.0.0

新增全量非系统消息匹配，插件新增ai插件示例

2024.1.7 0.9.0-b7

修复异步问题，修改插件示例

2024.1.7 0.9.0-b6

新增插件加载机制，引入插件式开发

其他一定程度的重构

2024.1.3 0.9.0-b5

新增matcher模块，重构Matcher类

重构Message类，新增MessageManager类管理最新的消息

重构server模块

新增消息handler机制与hook机制

2024.12.24 0.9.0-b4

项目结构结构重构，若干函数重构与优化

2024.2.6 0.9.0-b3

修复数据获取失败导致的崩溃问题

2023.8.12 0.9.0-b2

项目结构重构，优化代码编写规范，使用异步函数

2022.12.6 0.9.0-b1

1.修复消息列表最新一条为自动回复消息时程序崩溃问题

2.增加cookie失效异常捕获

3.修复当二维码失效时的程序异常退出问题

2022.11.16 0.9.0-beta

1.增加格式化日志类

2.增加cookie缓存功能，仅第一次登录需扫码

3.其他一定程度的改动与重构
</p>
</details>

## 🔗致谢

感谢易姐的api收集项目为本项目提供大量的api参考：[哔哩哔哩-API收集](https://github.com/SocialSisterYi/bilibili-API-collect)

感谢非常好用的异步bot开发框架为本项目提供开发灵感：[Nonebot2](https://github.com/nonebot/nonebot2)

## 📜开源许可

本项目采用 GNU GPLv3 许可证。详情请参阅 LICENSE 文件。
