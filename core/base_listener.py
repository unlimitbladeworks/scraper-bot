from abc import ABC, abstractmethod
from typing import Callable, Any, Optional

from models.message import Message
from utils.logger import setup_logger


class BaseListener(ABC):
    """
    监听器抽象基类，所有平台特定的监听器都应该继承此类
    """
    
    def __init__(self, platform_name: str):
        """
        初始化监听器
        
        Args:
            platform_name: 平台名称
        """
        self.platform_name = platform_name
        self.logger = setup_logger(f"{self.__class__.__name__}")
        self.message_callback = None
        self.running = False
    
    def register_callback(self, callback: Callable[[Message], None]) -> None:
        """
        注册消息处理回调函数
        
        Args:
            callback: 处理接收到消息的回调函数
        """
        self.message_callback = callback
        self.logger.info(f"已注册消息处理回调函数")
    
    @abstractmethod
    async def start(self) -> None:
        """启动监听器"""
        pass
    
    @abstractmethod
    async def stop(self) -> None:
        """停止监听器"""
        pass
    
    @abstractmethod
    async def process_message(self, raw_message: Any) -> Optional[Message]:
        """
        处理原始消息，转换为统一的消息模型
        
        Args:
            raw_message: 平台特定的原始消息对象
            
        Returns:
            Optional[Message]: 转换后的统一消息模型，如果消息应该被忽略则返回None
        """
        pass
    
    def _handle_message(self, message: Message) -> None:
        """
        内部消息处理方法，调用注册的回调函数
        
        Args:
            message: 统一的消息模型
        """
        if self.message_callback:
            try:
                self.message_callback(message)
            except Exception as e:
                self.logger.error(f"处理消息时发生错误: {e}", exc_info=True)
        else:
            self.logger.warning("未注册消息处理回调函数，消息将被忽略") 