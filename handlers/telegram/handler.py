from models.message import Message
from utils.logger import setup_logger
from handlers.base_handler import BaseMessageHandler


class TelegramMessageHandler(BaseMessageHandler):
    """Telegram 消息处理器"""
    
    def __init__(self):
        super().__init__("Telegram")
    
    def handle_message(self, message: Message) -> None:
        self.logger.info(f"处理 Telegram 消息: {message.content[:50]}...")
        super().handle_message(message)
        # Telegram 特定的处理逻辑 