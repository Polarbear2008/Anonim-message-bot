import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from handlers import setup_routers
from middlewares import UserMiddleware
from config_reader import config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main() -> None:
    logger.info("🚀 Starting bot...")
    
    bot = Bot(
        config.BOT_TOKEN.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    logger.info("📡 Setting up handlers...")
    
    # Register middlewares
    dp.message.middleware(UserMiddleware())
    dp.callback_query.middleware(UserMiddleware())
    
    # Setup routers
    dp.include_router(setup_routers())

    logger.info("🔗 Connecting to Telegram...")
    
    # Start polling
    await bot.delete_webhook(True)
    
    logger.info("✅ Bot started successfully!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())