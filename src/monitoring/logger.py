from loguru import logger

# Configure logger (optional)
logger.add("logs/bot.log", rotation="10 MB", level="INFO")