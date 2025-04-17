from abc import ABC, abstractmethod
from models.message import Message

class DiscordMessageStrategy(ABC):
    """Discord消息处理策略接口"""
    
    @abstractmethod
    def process(self, message: Message) -> bool:
        """
        处理Discord消息
        
        Args:
            message: 统一的消息模型
            
        Returns:
            bool: 是否成功处理消息
        """
        pass
    
    @abstractmethod
    def can_handle(self, message: Message) -> bool:
        """
        判断该策略是否能处理此消息
        
        Args:
            message: 统一的消息模型
            
        Returns:
            bool: 是否能处理此消息
        """
        pass 