import json
from datetime import datetime
from models.message import Message
from utils.logger import setup_logger
from handlers.handler_interface import MessageHandlerInterface

class BaseMessageHandler(MessageHandlerInterface):
    """基础消息处理器"""
    
    def __init__(self, platform_name):
        self.platform_name = platform_name
        self.logger = setup_logger(f"{platform_name}Handler")
    
    def save_message(self, message: Message) -> None:
        """保存消息（示例实现）"""
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f"data/{self.platform_name}/{timestamp}-{message.id}.json"
        
        # 确保目录存在
        import os
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # 手动创建消息字典
        message_dict = {
            "id": message.id,
            "content": message.content,
            "platform": message.platform,
            "author_id": message.author_id,
            "author_name": message.author_name,
            "timestamp": message.timestamp,
            "attachments": message.attachments,
            "metadata": message.metadata
        }
        
        # 将消息转换为JSON并保存
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(message_dict, f, ensure_ascii=False, indent=2, default=str)
        
        self.logger.info(f"消息已保存到 {filename}")
    
    def handle_message(self, message: Message) -> None:
        """处理消息的通用方法"""
        self.logger.info(f"接收到 {self.platform_name} 消息: {message.content[:50]}...")
        # self.save_message(message) 