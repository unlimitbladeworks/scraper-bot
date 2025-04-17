from typing import Dict, List, Callable, Any
from models.message import Message
from utils.logger import setup_logger


class MessageHandler:
    """
    消息处理器，负责处理从各平台接收到的消息
    """
    
    def __init__(self):
        self.logger = setup_logger("MessageHandler")
        self.global_handlers: List[Callable[[Message], None]] = []
        self.platform_handlers: Dict[str, List[Callable[[Message], None]]] = {}
    
    def register_global_handler(self, handler: Callable[[Message], None]) -> None:
        """注册全局消息处理器"""
        self.global_handlers.append(handler)
        self.logger.info(f"已注册全局消息处理器: {handler.__name__ if hasattr(handler, '__name__') else str(handler)}")
    
    def register_platform_handler(self, platform: str, handler: Callable[[Message], None]) -> None:
        """注册特定平台的消息处理器"""
        if platform not in self.platform_handlers:
            self.platform_handlers[platform] = []
        
        self.platform_handlers[platform].append(handler)
        self.logger.info(f"已注册 {platform} 平台消息处理器: {handler.__name__ if hasattr(handler, '__name__') else str(handler)}")
    
    def handle_message(self, message: Message) -> None:
        """处理接收到的消息"""
        try:
            # 记录接收到的消息
            self.logger.info(f"接收到来自 {message.platform} 的消息, ID: {message.id}, 作者: {message.author_name}")
            
            # 调用全局处理器
            for handler in self.global_handlers:
                try:
                    handler(message)
                except Exception as e:
                    self.logger.error(f"全局处理器执行错误: {e}", exc_info=True)
            
            # 调用平台特定处理器
            if message.platform in self.platform_handlers:
                for handler in self.platform_handlers[message.platform]:
                    try:
                        handler(message)
                    except Exception as e:
                        self.logger.error(f"{message.platform} 平台处理器执行错误: {e}", exc_info=True)
        
        except Exception as e:
            self.logger.error(f"处理消息时发生错误: {e}", exc_info=True) 