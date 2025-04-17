# 刮刀机器人 (Scraper Bot)

这是一个简单易用的机器人程序，可以帮你监听并处理来自不同平台（如Discord、推特、电报等）的消息。

## 🌟 功能介绍

- **模块化设计**：像搭积木一样，可以轻松添加新功能
- **多平台支持**：目前已实现 Discord 平台，未来计划支持 Twitter、Telegram 等
- **统一消息处理**：所有平台的消息处理流程一致，方便管理
- **完善的日志系统**：记录程序运行情况，出错时容易查找原因

## 📂 项目文件夹结构说明

```
scraper-bot/
├── config/                    # 配置文件目录，存放各种设置
├── core/                      # 核心功能模块
│   ├── base_listener.py       # 基础监听器（所有平台监听器的"父类"）
│   ├── discord/               # Discord平台相关代码
│   ├── twitter/               # Twitter平台相关代码（待实现）
│   └── telegram/              # Telegram平台相关代码（待实现）
├── handlers/                  # 消息处理模块，负责处理收到的消息
├── models/                    # 数据模型，定义各种数据的格式
├── utils/                     # 工具函数，提供各种辅助功能
│   ├── logger.py              # 日志工具，记录程序运行情况
│   └── exceptions.py          # 异常处理，定义可能出现的错误类型
├── main.py                    # 主程序入口文件
└── requirements.txt           # 依赖库列表，记录需要安装的第三方包
```

## 💻 运行环境要求

- Python 3.8 或更高版本
- 需要安装 requirements.txt 中列出的所有第三方库

## 🔧 安装步骤

### 1. 下载程序代码

```bash
# 使用git克隆仓库（如果你不会用git，可以直接从网页下载压缩包）
git clone https://github.com/yourusername/scraper-bot.git
cd scraper-bot
```

### 2. 创建虚拟环境（推荐，但非必须）

虚拟环境可以避免与电脑上其他Python程序的依赖冲突。

```bash
# 创建名为.venv的虚拟环境
python -m venv .venv

# 启动虚拟环境
# Windows系统:
.venv\Scripts\activate
# Mac或Linux系统:
source .venv/bin/activate
```

当你看到命令行前面出现(.venv)时，说明虚拟环境已经启动。

### 3. 安装所需的第三方库

```bash
# 安装requirements.txt中列出的所有依赖库
pip install -r requirements.txt
```

### 4. 配置环境变量

1. 将`.env.example`文件复制一份，并重命名为`.env`
2. 用记事本或任意文本编辑器打开`.env`文件
3. 根据你的需要修改各项配置，必须设置的内容包括:

```
# 日志设置（一般保持默认即可）
LOG_LEVEL=INFO
LOG_FILE=scraper-bot.log

# Discord设置（如果使用Discord功能）
DISCORD_TOKEN=你的discord机器人token
DISCORD_CHANNEL_IDS=要监听的频道ID（多个ID用逗号分隔）
DISCORD_TARGET_USER_IDS=要关注的用户ID（多个ID用逗号分隔）

# 启用的平台（目前只支持discord）
ENABLED_PLATFORMS=discord

# 代理设置（如果你在国内需要使用代理）
OPEN_PROXY=True
HTTP_PROXY=http://127.0.0.1:7890
```

## 📱 使用方法

### 启动机器人

```bash
# 确保你在项目目录下，并且已经启动了虚拟环境（如果有）
python main.py
```

启动后，机器人会开始监听你在配置文件中指定的平台和频道。所有接收到的消息将会被记录到日志文件中，同时终端也会显示运行状态。

### 停止机器人

在终端中按下 `Ctrl+C` 组合键可以停止机器人运行。

## 🔍 常见问题解答

1. **问题**: 启动时报错"ModuleNotFoundError: No module named 'xxx'"
   **解决方法**: 这说明某个依赖库没有安装成功，请重新运行 `pip install -r requirements.txt`

2. **问题**: Discord机器人无法连接
   **解决方法**: 检查你的Discord Token是否正确，以及网络连接是否正常。如果在国内使用，可能需要启用代理

3. **问题**: 如何查看日志？
   **解决方法**: 程序运行日志保存在项目目录下的scraper-bot.log文件中，可以用任意文本编辑器打开查看

## 📚 进阶使用：添加新的平台支持

如果你有一定的编程基础，可以尝试为机器人添加新的平台支持：

1. 在`core/`目录下创建新平台的文件夹（例如`core/new_platform/`）
2. 创建一个继承自`BaseListener`的新监听器类
3. 在`.env`文件中添加新平台所需的配置项
4. 在`main.py`的`setup_listeners`方法中添加新平台的处理逻辑


## 📄 许可证

[MIT License](LICENSE) - 你可以自由使用、修改和分发此项目。
