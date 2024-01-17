from TelegramBot import TelegramBot
from aiogram.utils import executor

if __name__ == "__main__":
    bot = TelegramBot()
    bot.register_message_handlers()
    executor.start_polling(bot.dispatcher)