# Scraper Bot (刮刀机器人)

一个模块化、可扩展的机器人，用于监听不同平台上的消息。

## 功能特点

- 模块化架构，易于扩展
- 支持多平台监听 (当前实现: Discord, 计划中: Twitter, Telegram)
- 统一的消息处理流程
- 完善的日志和异常处理机制

## 项目结构

```
scraper-bot/
├── config/                    # 配置文件目录
├── core/                      # 核心功能
│   ├── base_listener.py       # 监听器抽象基类
│   ├── discord/               # Discord监听实现
│   ├── twitter/               # Twitter监听实现(预留)
│   └── telegram/              # Telegram监听实现(预留)
├── handlers/                  # 消息处理器
├── models/                    # 数据模型
├── utils/                     # 工具函数
│   ├── logger.py              # 日志工具
│   └── exceptions.py          # 自定义异常
├── main.py                    # 入口文件
└── requirements.txt           # 依赖管理
```

## 环境要求

- Python 3.8+
- 依赖库详见 requirements.txt

## 安装

1. 克隆仓库:
```bash
git clone https://github.com/yourusername/scraper-bot.git
cd scraper-bot
```

2. 创建并激活虚拟环境 (推荐):
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

3. 安装依赖:
```bash
pip install -r requirements.txt
```

4. 配置环境变量:
   - 创建 `.env` 文件，参考以下示例:
```
# 日志设置
LOG_LEVEL=INFO
LOG_FILE=scraper-bot.log

# Discord设置
DISCORD_TOKEN=your_discord_token
DISCORD_CHANNEL_ID=your_channel_id
DISCORD_TARGET_USER_ID=target_user_id

# 启用的平台
ENABLED_PLATFORMS=discord
```

## 使用方法

1. 启动机器人:
```bash
python main.py
```

2. 自定义消息处理:
   - 在 `handlers/message_handler.py` 中添加自定义处理逻辑
   - 在主程序 `main.py` 的 `setup_handlers` 方法中注册你的处理器

## 扩展平台

要添加新平台支持:

1. 创建新的监听器实现:
   - 在 `core/` 目录下创建新的平台子目录
   - 实现继承自 `BaseListener` 的平台特定监听器类
   
2. 更新配置:
   - 在 `config/settings.py` 中添加新平台所需配置
   - 在 `.env` 文件中添加相应的环境变量
   
3. 注册监听器:
   - 在 `main.py` 的 `setup_listeners` 方法中添加新平台处理逻辑

## 贡献

欢迎提交 Pull Request 或提出 Issue 来改进项目。

## 许可证

[MIT License](LICENSE)
