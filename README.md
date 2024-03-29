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

## 测试版

目前在测试阶段，仅供参考，非项目最终结构

## 使用

克隆项目，运行main或在你的测试函数中直接import包bilink

在server文件中可以构造自动回复命令，示例：向当前登录用户私信发送“`你好`”，则自动回复“ `(*´▽｀)ノノ你好鸭~~`

```python
await message.fetch_msgs()
await message.auto_reply('你好', '(*´▽｀)ノノ你好鸭~~')
Message.LastTimestamp = Message.Timestamp
await sleep(2)
```

---

## 更新记录
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
