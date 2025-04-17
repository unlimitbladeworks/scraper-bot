import re
from typing import List
from models.message import Message
from handlers.base_handler import BaseMessageHandler
from handlers.discord.strategies.base_strategy import DiscordMessageStrategy
from handlers.discord.strategies.thunderbolt_strategy import ThunderboltMonitorStrategy


class DiscordMessageHandler(BaseMessageHandler):
    """Discord 消息处理器"""

    def __init__(self):
        super().__init__("Discord")
        # Discord 特定的指令模式
        self.command_pattern = re.compile(r'^!(\w+)\s*(.*)')

        # 初始化策略列表
        self.strategies: List[DiscordMessageStrategy] = []
        self._init_strategies()

    def _init_strategies(self):
        """初始化所有策略"""
        # 添加 thunder 监听策略
        monitor_strategy = ThunderboltMonitorStrategy()
        self.strategies.append(monitor_strategy)

        # todo 后续在这里可以新增不同的业务策略

    def add_strategy(self, strategy: DiscordMessageStrategy):
        """ 添加新策略 """
        self.strategies.append(strategy)
        self.logger.info(f"添加了新的处理策略: {strategy.__class__.__name__}")

    def handle_message(self, message: Message) -> None:
        """处理 Discord 消息"""
        self.logger.info(f"进入DiscordMessageHandler.handle_message方法，消息内容：{message.content[:30]}...")
        super().handle_message(message)

        # 使用策略模式处理消息
        for strategy in self.strategies:
            if strategy.can_handle(message):
                self.logger.info(f"使用 {strategy.__class__.__name__} 处理消息")
                success = strategy.process(message)
                if success:
                    break  # 如果某个策略成功处理，则停止

        self.logger.info("完成DiscordMessageHandler.handle_message处理")
