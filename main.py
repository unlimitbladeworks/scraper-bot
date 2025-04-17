import asyncio
import signal
import sys
from typing import Dict, List

from config.settings import ENABLED_PLATFORMS
from core.base_listener import BaseListener
from core.discord.listener import DiscordListener
from handlers.message_handler import MessageHandler
from models.message import Message
from utils.logger import setup_logger
from utils.exceptions import ScraperBotError
from handlers.discord.handler import DiscordMessageHandler
from handlers.twitter.handler import TwitterMessageHandler
from handlers.telegram.handler import TelegramMessageHandler

# 设置主日志记录器
logger = setup_logger("main")


class ScraperBot:
    """
    刮刀机器人主类
    """

    def __init__(self):
        self.listeners: Dict[str, BaseListener] = {}
        self.handler = MessageHandler()
        self.running = False
        self.tasks: List[asyncio.Task] = []

    def setup_handlers(self) -> None:
        """设置消息处理器"""

        # 创建平台特定的处理器
        discord_handler = DiscordMessageHandler()
        twitter_handler = TwitterMessageHandler()
        telegram_handler = TelegramMessageHandler()

        # 添加调试日志，确认使用的是哪个类
        logger.info(f"使用的Discord处理器: {discord_handler.__class__.__module__}.{discord_handler.__class__.__name__}")

        # 注册处理器
        self.handler.register_platform_handler("discord", discord_handler.handle_message)
        self.handler.register_platform_handler("twitter", twitter_handler.handle_message)
        self.handler.register_platform_handler("telegram", telegram_handler.handle_message)

        # 可以添加一个全局处理器用于记录或者其他共通操作
        def global_message_logger(message: Message) -> None:
            logger.info(f"消息接收: [{message.platform}] {message.author_name}: {message.content[:30]}...")

        self.handler.register_global_handler(global_message_logger)

    def setup_listeners(self) -> None:
        """设置平台监听器"""

        for platform in ENABLED_PLATFORMS:
            try:
                if platform == "discord":
                    self.listeners[platform] = DiscordListener()
                # 其他平台监听器在这里添加...

                # 如果成功创建监听器，注册消息回调
                if platform in self.listeners:
                    self.listeners[platform].register_callback(self.handler.handle_message)
                    logger.info(f"已设置 {platform} 监听器")
                else:
                    logger.warning(f"未知平台: {platform}，跳过")

            except Exception as e:
                logger.error(f"设置 {platform} 监听器时出错: {e}", exc_info=True)

    async def start(self) -> None:
        """启动机器人"""
        if self.running:
            logger.warning("机器人已经在运行中")
            return

        logger.info("正在启动刮刀机器人...")

        # 设置处理器和监听器
        self.setup_handlers()
        self.setup_listeners()

        # 启动所有监听器
        for platform, listener in self.listeners.items():
            task = asyncio.create_task(self._start_listener(platform, listener))
            self.tasks.append(task)

        self.running = True
        logger.info("刮刀机器人启动完成")

    async def _start_listener(self, platform: str, listener: BaseListener) -> None:
        """启动单个监听器的异步任务"""
        try:
            logger.info(f"启动 {platform} 监听器")
            await listener.start()
        except Exception as e:
            logger.error(f"启动 {platform} 监听器时出错: {e}", exc_info=True)

    async def stop(self) -> None:
        """停止机器人"""
        if not self.running:
            return

        logger.info("正在停止刮刀机器人...")

        # 停止所有监听器
        for platform, listener in self.listeners.items():
            try:
                await listener.stop()
                logger.info(f"已停止 {platform} 监听器")
            except Exception as e:
                logger.error(f"停止 {platform} 监听器时出错: {e}", exc_info=True)

        # 取消所有任务
        for task in self.tasks:
            task.cancel()

        self.running = False
        logger.info("刮刀机器人已停止")


async def main() -> None:
    """主函数"""
    # 创建机器人实例
    bot = ScraperBot()

    # 设置信号处理
    loop = asyncio.get_event_loop()

    def signal_handler():
        logger.info("接收到终止信号，正在关闭...")
        asyncio.create_task(shutdown())

    async def shutdown():
        await bot.stop()
        loop.stop()

    # 注册信号处理器
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, signal_handler)

    try:
        # 启动机器人
        await bot.start()

        # 保持程序运行
        while bot.running:
            await asyncio.sleep(1)

    except ScraperBotError as e:
        logger.error(f"机器人运行错误: {e}", exc_info=True)
        await bot.stop()
        sys.exit(1)
    except Exception as e:
        logger.error(f"发生未知错误: {e}", exc_info=True)
        await bot.stop()
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("程序被用户中断")
    except Exception as e:
        logger.critical(f"程序崩溃: {e}", exc_info=True)
        sys.exit(1)
