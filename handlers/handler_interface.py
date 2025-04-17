from abc import ABC, abstractmethod
from models.message import Message

class MessageHandlerInterface(ABC):
    """消息处理器接口"""
    
    @abstractmethod
    def handle_message(self, message: Message) -> None:
        """
        处理消息
        
        Args:
            message: 统一的消息模型
        """
        pass 