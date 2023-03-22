import asyncio
from aiogram import Bot, Dispatcher
import config
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from utils.db_api.postgresql import DataBase

loop = asyncio.get_event_loop()
bot = Bot(str(config.BOT_TOKEN), parse_mode='HTML')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = DataBase(loop)


if __name__ == '__main__':
    from handlers import dp
    from aiogram import executor
    executor.start_polling(dp)