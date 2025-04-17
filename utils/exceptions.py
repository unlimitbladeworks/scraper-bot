class ScraperBotError(Exception):
    """刮刀机器人基础异常类"""
    pass


class ConfigError(ScraperBotError):
    """配置错误异常"""
    pass


class ListenerError(ScraperBotError):
    """监听器错误基础异常"""
    pass


class DiscordListenerError(ListenerError):
    """Discord监听器异常"""
    pass


class TwitterListenerError(ListenerError):
    """Twitter监听器异常"""
    pass


class TelegramListenerError(ListenerError):
    """Telegram监听器异常"""
    pass


class MessageHandlerError(ScraperBotError):
    """消息处理器异常"""
    pass 