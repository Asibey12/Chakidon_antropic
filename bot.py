"""
Main Bot Entry Point
====================
Initializes and runs the Telegram bot with aiogram 3.x
"""

import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import settings
from database.database import init_db, dispose_engine
from middlewares import DatabaseMiddleware, UserStateMiddleware

# Import all handler routers
from handlers.start import router as start_router
from handlers.language import router as language_router
from handlers.service import router as service_router
from handlers.order import router as order_router
from handlers.address import router as address_router
from handlers.customer_info import router as customer_info_router
from handlers.order_summary import router as order_summary_router
from handlers.feedback import router as feedback_router
from handlers.admin import router as admin_router
from handlers.my_orders import router as my_orders_router

# Configure logging
logging.basicConfig(
    level=logging.INFO if not settings.debug else logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


async def on_startup(bot: Bot):
    """
    Execute on bot startup
    
    Args:
        bot: Bot instance
    """
    logger.info("🚀 Starting bot...")
    
    # Initialize database
    try:
        await init_db()
    except Exception as e:
        logger.error(f"❌ Failed to initialize database: {e}")
        sys.exit(1)
    
    # Notify admins that bot started
    for admin_id in settings.admin_ids:
        try:
            await bot.send_message(
                chat_id=admin_id,
                text="✅ <b>Бот запущен и готов к работе!</b>",
                parse_mode=ParseMode.HTML
            )
        except Exception as e:
            logger.warning(f"Could not notify admin {admin_id}: {e}")
    
    logger.info("✅ Bot started successfully")
    logger.info(f"Configured admins: {settings.admin_ids}")


async def on_shutdown(bot: Bot):
    """
    Execute on bot shutdown
    
    Args:
        bot: Bot instance
    """
    logger.info("🛑 Shutting down bot...")
    
    # Dispose database engine
    await dispose_engine()
    
    # Notify admins
    for admin_id in settings.admin_ids:
        try:
            await bot.send_message(
                chat_id=admin_id,
                text="🛑 <b>Бот остановлен</b>",
                parse_mode=ParseMode.HTML
            )
        except:
            pass
    
    logger.info("✅ Bot shutdown complete")


async def main():
    """Main function to run the bot"""
    
    # Initialize bot with default properties
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    # Initialize dispatcher
    dp = Dispatcher()
    
    # Register middlewares (order matters!)
    dp.message.middleware(DatabaseMiddleware())
    dp.callback_query.middleware(DatabaseMiddleware())
    dp.message.middleware(UserStateMiddleware())
    dp.callback_query.middleware(UserStateMiddleware())
    
    # Register routers (order matters - more specific first)
    dp.include_router(start_router)
    dp.include_router(language_router)
    dp.include_router(service_router)
    dp.include_router(order_router)
    dp.include_router(address_router)
    dp.include_router(customer_info_router)
    dp.include_router(order_summary_router)
    dp.include_router(feedback_router)
    dp.include_router(admin_router)
    dp.include_router(my_orders_router)
    
    # Register startup/shutdown handlers
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    # Start polling
    try:
        logger.info("Starting polling...")
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")