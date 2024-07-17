import asyncio
import logging
import utilities
import choose_products, gallery, settings, calculator
import mailing, statistics_bot
import admin_levels, change_section
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher
from config import config
from aiogram.fsm.storage.redis import RedisStorage

logging.basicConfig(level=logging.INFO, format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
bot = Bot(token=config.bot_token.get_secret_value(), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
redis_storage = RedisStorage.from_url('redis://localhost:6379/0')
dp = Dispatcher(storage=redis_storage)
from throttling_middleware import ThrottlingMiddleware
async def main():

    dp.include_router(settings.sett)
    dp.include_router(mailing.mail)
    dp.include_router(choose_products.cut)
    dp.include_router(calculator.calc)
    dp.include_router(gallery.gal)
    dp.include_router(utilities.ut)
    dp.include_router(statistics_bot.stat)
    dp.include_router(admin_levels.adm)
    dp.include_router(change_section.sect)

    dp.message.middleware.register(ThrottlingMiddleware(storage=redis_storage))
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped!")
