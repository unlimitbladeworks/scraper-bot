import discord
from datetime import datetime
from typing import Optional, Any
import asyncio
import aiohttp
import ssl

from config.settings import DISCORD_TOKEN, DISCORD_CHANNEL_ID, DISCORD_TARGET_USER_IDS, HTTP_PROXY, DISCORD_CHANNEL_IDS, \
    OPEN_PROXY
from core.base_listener import BaseListener
from models.message import Message
from utils.exceptions import DiscordListenerError


class DiscordListener(BaseListener):
    """
    Discord平台的消息监听器
    """

    def __init__(self):
        super().__init__(platform_name="discord")

        # 检查配置
        if not DISCORD_TOKEN:
            raise DiscordListenerError("Discord token未配置")

        # 创建Discord客户端 (用户端)
        # 用户端不需要intents设置，简化初始化

        # 创建SSL上下文但禁用证书验证
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        if OPEN_PROXY:
            # 设置代理
            proxy = HTTP_PROXY
            # 初始化用户客户端
            self.client = discord.Client(
                proxy=proxy,
                http_timeout=60.0
            )
        else:
            self.client = discord.Client(
                http_timeout=60.0
            )

        # 设置SSL上下文
        if hasattr(self.client, 'http') and hasattr(self.client.http, 'connector'):
            self.client.http.connector = aiohttp.TCPConnector(ssl=ssl_context)

        # 支持多频道监听
        self.target_channel_ids = DISCORD_CHANNEL_IDS
        # 向后兼容：如果设置了单一频道ID且多频道列表为空，添加到列表中
        if DISCORD_CHANNEL_ID and not self.target_channel_ids:
            self.target_channel_ids.append(DISCORD_CHANNEL_ID)

        self.target_user_ids = DISCORD_TARGET_USER_IDS

        # 设置事件处理器
        @self.client.event
        async def on_ready():
            self.logger.info(f"已登录为 {self.client.user}")
            self.running = True

        @self.client.event
        async def on_message(message):
            try:
                # 处理消息
                processed_message = await self.process_message(message)
                if processed_message:
                    self._handle_message(processed_message)
            except Exception as e:
                self.logger.error(f"处理Discord消息时发生错误: {e}", exc_info=True)

    async def start(self) -> None:
        """启动Discord监听器"""
        max_retries = 3
        retry_delay = 5  # 秒

        for attempt in range(max_retries):
            try:
                self.logger.info("正在启动Discord监听器...")
                # 确保每次尝试使用正确格式的令牌
                token = DISCORD_TOKEN.strip()  # 去除可能的空格
                if token.startswith('"') and token.endswith('"'):
                    token = token[1:-1]  # 去除可能的引号

                await self.client.start(token)
                break  # 如果成功连接，跳出循环
            except Exception as e:
                if attempt < max_retries - 1:  # 如果不是最后一次尝试
                    self.logger.warning(f"连接Discord失败，{retry_delay}秒后重试 ({attempt + 1}/{max_retries}): {e}")
                    await asyncio.sleep(retry_delay)
                    retry_delay *= 2  # 增加重试延迟
                else:
                    raise DiscordListenerError(f"启动Discord监听器失败: {e}") from e

    async def stop(self) -> None:
        """停止Discord监听器"""
        if self.running:
            self.logger.info("正在停止Discord监听器...")

            try:
                # 关闭Discord客户端
                await self.client.close()
                self.running = False
                self.logger.info("Discord监听器已停止")
            except Exception as e:
                self.logger.error(f"停止Discord监听器时出错: {e}", exc_info=True)

    async def process_message(self, raw_message: Any) -> Optional[Message]:
        """
        处理Discord消息
        
        Args:
            raw_message: Discord消息对象
            
        Returns:
            Optional[Message]: 处理后的统一消息对象，如果消息应该被忽略则返回None
        """
        # 如果指定了目标频道，则只处理这些频道的消息
        if self.target_channel_ids and str(raw_message.channel.id) not in self.target_channel_ids:
            return None

        # 修改为支持多个用户
        # 如果指定了目标用户列表且不为空，则只处理这些用户的消息
        if self.target_user_ids and str(raw_message.author.id) not in self.target_user_ids:
            return None

        # 忽略机器人消息
        if raw_message.author.bot:
            return None

        # 提取附件URL
        attachments = [attachment.url for attachment in raw_message.attachments]

        # 创建统一消息模型
        return Message(
            id=str(raw_message.id),
            content=raw_message.content,
            platform="discord",
            author_id=str(raw_message.author.id),
            author_name=f"{raw_message.author.name}#{raw_message.author.discriminator}" if hasattr(raw_message.author,
                                                                                                   "discriminator") else raw_message.author.name,
            timestamp=raw_message.created_at if hasattr(raw_message, "created_at") else datetime.now(),
            attachments=attachments,
            raw_message=raw_message,
            metadata={
                "channel_id": str(raw_message.channel.id),
                "guild_id": str(raw_message.guild.id) if hasattr(raw_message, "guild") and raw_message.guild else None,
            }
        )
