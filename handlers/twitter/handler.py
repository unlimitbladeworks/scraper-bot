from models.message import Message
from handlers.base_handler import BaseMessageHandler


class TwitterMessageHandler(BaseMessageHandler):
    """Twitter 消息处理器"""
    
    def __init__(self):
        super().__init__("Twitter")
    
    def handle_message(self, message: Message) -> None:
        self.logger.info(f"处理 Twitter 消息: {message.content[:50]}...")
        super().handle_message(message)
        # Twitter 特定的处理逻辑 