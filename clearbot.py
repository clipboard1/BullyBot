from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from tokens import bot_token
storage = MemoryStorage()

bot = Bot(token=bot_token)
dp = Dispatcher(bot, storage=storage)

executor.start_polling(dp)