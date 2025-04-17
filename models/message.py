from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any, List


@dataclass
class Message:
    """
    统一消息模型，用于表示从不同平台获取到的消息
    """
    # 消息唯一标识符
    id: str
    
    # 消息内容
    content: str
    
    # 消息来源平台 (discord, twitter, telegram)
    platform: str
    
    # 发送者信息
    author_id: str
    author_name: str
    
    # 消息发送时间
    timestamp: datetime = field(default_factory=datetime.now)
    
    # 消息附件 (URL列表)
    attachments: List[str] = field(default_factory=list)
    
    # 原始消息对象 (平台相关)
    raw_message: Any = None
    
    # 元数据 (可用于存储平台特定的额外信息)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __str__(self) -> str:
        """返回消息的字符串表示"""
        return f"[{self.platform}] {self.author_name}: {self.content}"
        
    def to_dict(self) -> Dict[str, Any]:
        """将消息对象转换为字典"""
        return {
            "id": self.id,
            "content": self.content,
            "platform": self.platform,
            "author_id": self.author_id,
            "author_name": self.author_name,
            "timestamp": self.timestamp,
            "attachments": self.attachments,
            "metadata": self.metadata
        } 