from aiogram import types, Bot
import asyncio


@bot.dp.message_handler(commands=["help"])
async def process_start_command(bot: Bot, msg: types.Message):
    if msg.chat.id in bot.allowidlist:
        await msg.reply(
            "\nПиши /demot для генерации демотиватора"
            "\nПиши /startgpt для начала диалога с ChatGPT"
            "\nДля завершения диалога с ChatGPT отправь /stopgpt"
            "\nДля изменения шанса ответа отправь /setchance 0-100"
        )
    else:
        await bot.send_message(
            msg.chat.id,
            f"Я вас не знаю, не пишите мне. Добавьте себя в список допущенных id, вот ваш id {str(msg.chat.id)}",
        )


async def timer_callback(bot: Bot, seconds, msg: types.Message):
    await asyncio.sleep(seconds)
    chat_gpt.gpton = False
    chat_gpt.gptuserid = 0
    chat_gpt.gptchatid = 0
    chat_gpt.messages = []
    await bot.send_message(msg.chat.id, "Завершаю сессию с GPT-3.5-turbo")
    await bot.send_message(msg.chat.id, "История общения обнулена")
    chat_gpt.timer.cancel()


async def startgpt(bot: Bot, msg: types.Message):
    if msg.chat.id in bot.allowid:
        if not (chat_gpt.gpton):
            chat_gpt.gpton = True
            chat_gpt.gptuserid = msg.from_user.id
            chat_gpt.gptchatid = msg.chat.id
            chat_gpt.timer = asyncio.create_task(timer_callback(bot, 300, msg))
            await bot.send_message(msg.chat.id, "Запускаю сессию с GPT-3.5-turbo")
            await bot.send_message(
                msg.chat.id,
                "Задавайте вопрос, время ответа зависит от вопроса, в среднем около 5-30 секунд",
            )
            await bot.send_message(
                msg.chat.id, "Для завершения диалога с ChatGPT отправь /stopgpt"
            )
        else:
            await bot.send_message(msg.chat.id, "Сессия уже запущена")
    else:
        await bot.send_message(
            msg.chat.id,
            "Я вас не знаю, не пишите мне. Добавьте себя в список допущенных id, вот ваш id "
            + str(msg.chat.id),
        )


async def stopgpt(bot: Bot, msg: types.Message):
    if msg.chat.id in bot.allowid:
        if chat_gpt.gpton:
            chat_gpt.gpton = False
            chat_gpt.gptuserid = 0
            chat_gpt.gptchatid = 0
            chat_gpt.messages = []
            chat_gpt.timer.cancel()
            await bot.send_message(msg.chat.id, "Завершаю сессию с GPT-3.5-turbo")
            await bot.send_message(msg.chat.id, "История общения обнулена")
        else:
            await bot.send_message(msg.chat.id, "Отсуствует сессия для завершения")
    else:
        await bot.send_message(msg.chat.id, "Я")
