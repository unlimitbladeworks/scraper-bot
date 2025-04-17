import logging
import sys
from logging.handlers import RotatingFileHandler
from config.settings import LOG_LEVEL, LOG_FORMAT, LOG_FILE

def setup_logger(name):
    """
    设置并返回一个配置好的logger实例
    
    Args:
        name: logger的名称，通常是模块名
        
    Returns:
        logging.Logger: 配置好的logger实例
    """
    logger = logging.getLogger(name)
    
    # 设置日志级别
    level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
    logger.setLevel(level)
    
    # 如果已经有处理器则不添加
    if logger.handlers:
        return logger
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_formatter = logging.Formatter(LOG_FORMAT)
    console_handler.setFormatter(console_formatter)
    
    # 创建文件处理器 (轮转日志)
    file_handler = RotatingFileHandler(
        LOG_FILE, 
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(level)
    file_formatter = logging.Formatter(LOG_FORMAT)
    file_handler.setFormatter(file_formatter)
    
    # 添加处理器到logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger 