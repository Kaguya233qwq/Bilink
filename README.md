<div align="center">

<p align="center">
  <a href=""><img src="https://github.com/Kaguya233qwq/Bilink/blob/main/icon.png?raw=ture" width="" height="" alt="bilink"></a>
</p>

✨ 基于异步架构的轻量级 Bilibili 自动化机器人框架 ✨

<p align="center">
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python">
</p>

_“模块化，高性能，全自动”_

</div>

---

## 📖 项目介绍

**Bilink** 是一款为 Bilibili 量身定制的轻量级异步自动化框架。起初作为基于轮询的自动回复机器人，现已全面重构并演进为一个**高度模块化的多功能自动化系统**。

通过引入灵活的插件机制、定时任务调度以及底层自适应 API 代理，Bilink 不仅可以处理实时的私信互动，更能够轻松实现后台无人值守的服务——如：**自动同步收藏夹视频**、**订阅式关注 UP 主新投稿并自动下载**防和谐等。

## ✨ 特性概览

- ⚡ **原生异步并发**：底层采用 `httpx[http2]` 与 `asyncio`，在高并发请求与大体积视频下载场景下保持优异性能。
- 📦 **模块化插件机制**：只需通过简单的装饰器即可注册不同的事件监听（如 `CRON` 定时任务、消息关键词匹配等），按需加载，极易扩展。
- 🔐 **智能鉴权引擎**：内置终端扫码登录登录流水线，自动缓存并维护 Cookie 原生状态；支持自动解算 Bilibili 的 WBI 签名（`nav` API解析 + MD5验签），从容应对反爬风控策略。
- ⏱️ **强大的定时调度**：融入 `aiocron` 系统，提供 Linux Cron 风格的时间表达式，完美支持毫秒级差异的后台定时轮询作业。

## 🚀 快速开始

### 💿 安装依赖（推荐使用 uv）
```bash
uv sync
```
### ▶️ 运行项目
```bash
uv run python main.py
```

## 🧩 插件开发与示例

框架采用装饰器注册机制来分发事件，您可以在 `bilink/plugins/` 目录下自由创建您的业务脚本。以下是一个典型的**定时运行**插件示例：

```python
from ..core.handler import handler
from ..core.matcher import MatchType
from ..utils.logger import Logger

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..bot import Bot

# 使用 CRON 表达式，此处代表每分钟执行一次
@handler.register(MatchType.CRON, "* * * * *")
async def my_custom_job(bot: "Bot"):
    Logger.info("定时任务已被触发")
    
    # 你可以随时获取 bot 的原生 api 发起高权限动作
    api = bot.api
    # 调用自己封装的接口等
    # await api.send_msg("服务器巡检正常！", receiver_id=12345678)
```
*只需上述寥寥几行代码，即可实现一个常驻后台、具有自动守护能力的插件服务*

## 📃 更新记录

<details>
<summary>点击查看历史与最近的大版本更新</summary>

### 🔔 近期核心更新 (2026.05)
- **🎉 全新插件: UP 主视频自动订阅监听 (`up_sync.py`)**：新增订阅指定 UP 主（`TARGET_UP_MIDS`）列表逻辑，当探测到 UP 主有新视频发布时，自动化执行高清晰度视频持久化入库，并自动按结构分类保存至 `Download/UP_{作者}_{MID}/`。
- **🎉 全新插件: 收藏夹全自动后台同步 (`fav_sync.py`)**：剥离旧版手动敲指令抓取的繁琐，基于 CRON 接管后台。实现文件状态的缓存对比、异常过滤、合法化命名，以及对 302 重定向错误的全面适配，实现了高可用的视频安全备份功能。
- **✨ 机制升级: 引入 AIOCRON 定时任务系统**：事件路由 (`handler.py` 与 `matcher.py`) 现在原生支持 `MatchType.CRON` 类型，支持灵活编排各种后台时间驱动任务。

### 📌 历史版本追溯
- **1.0.0 (2025.06)**：新增全量非系统消息匹配，新增 AI 回复插件示例。
- **0.9.0-b7 ~ b5 (2024.01)**：修复异步流程阻塞。新增插件按需加载机制。重构了基于 Matcher 和 MessageManager 的现代处理钩子。
- **0.9.0-b4 (2023.12)**：重组项目大文件架构。
- **0.9.0-beta ~ b2 (2022.11 - 2023.08)**：初版异步重构，添加 Logger 库渲染并提供初版扫码登录（二维码缓存控制）。
</details>

## 🔗 致谢

感谢易姐的api收集项目为本项目提供大量的api参考：[哔哩哔哩-API收集](https://github.com/SocialSisterYi/bilibili-API-collect)

感谢非常好用的异步bot开发框架为本项目提供开发灵感：[Nonebot2](https://github.com/nonebot/nonebot2)

## 📜 开源许可

本项目采用 GNU GPLv3 许可证。详情请参阅 LICENSE 文件。
