import os
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()

# 日志配置
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FILE = os.getenv('LOG_FILE', 'scraper-bot.log')

# Discord配置
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_CHANNEL_IDS = os.getenv('DISCORD_CHANNEL_IDS', '').split(',') if os.getenv('DISCORD_CHANNEL_IDS') else []
DISCORD_CHANNEL_ID = os.getenv('DISCORD_CHANNEL_ID')
DISCORD_TARGET_USER_IDS = os.getenv('DISCORD_TARGET_USER_IDS', '').split(',') if os.getenv(
    'DISCORD_TARGET_USER_IDS') else []

# Twitter配置 (预留)
TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_SECRET = os.getenv('TWITTER_ACCESS_SECRET')
TWITTER_TARGET_USER_ID = os.getenv('TWITTER_TARGET_USER_ID')

# Telegram配置 (预留)
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
TELEGRAM_TARGET_USER_ID = os.getenv('TELEGRAM_TARGET_USER_ID')

# 服务配置
ENABLED_PLATFORMS = os.getenv('ENABLED_PLATFORMS', 'discord').split(',')

# 代理设置
OPEN_PROXY = os.getenv('OPEN_PROXY') == 'True'
HTTP_PROXY = os.getenv('HTTP_PROXY')
