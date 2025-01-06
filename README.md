<div align="center">

<p align="center">
  <a href=""><img src="https://github.com/Kaguya233qwq/Bilink/blob/main/icon.png?raw=ture" width="" height="" alt="bilink"></a>
</p>

✨ 基于轮询的原生哔哩哔哩消息自动回复工具 ✨_

<p align="center">
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python">
</p>

_“一个简单的通信服务端”_

</div>

---

## 快速开始

## 安装环境依赖
```bash
pdm install
```
## 运行项目
```bash
pdm run python main.py
```
## 编写插件

```python

bilink.plugins下存放了一个示例插件reply_hello.py

from ..core.handler import handler
from ..core.matcher import MatchType
from ..core.message import send_text_msg


@handler.register(MatchType.STARTS_WITH, "你好")
def send():
    send_text_msg("你好呀", "")

handler.register表示注册一个消息处理器

其接收参数为匹配类型MatchType以及它对应的参数，一般为要匹配的关键词

MatchType下提供了一些常用的匹配类型，请开发者按需使用

```

---

## 更新记录

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
