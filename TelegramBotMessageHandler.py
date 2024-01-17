from aiogram import types, Bot
import asyncio
from tokens import allowidlist
from IGPTAPI import openAIEntity

class MessageHandler(Bot):

    def __init__(self, bot):
        self.ITelegramBot = bot
        self.openai_entity = openAIEntity()

    @staticmethod
    def CanUserUseBot(id):
        return id in allowidlist

    async def help(self, message: types.Message):
        if self.CanUserUseBot(message.chat.id):     
            await message.reply("\nПиши /demot для генерации демотиватора"
                                "\nПиши /startgpt для начала диалога с ChatGPT"
                                "\nДля завершения диалога с ChatGPT отправь /stopgpt"
                                "\nДля изменения шанса ответа отправь /setchance 0-100")
        else:
            await message.reply('Я вас не знаю, не пишите мне. Добавьте себя в список допущенных id, вот ваш id ' + str(message.chat.id))
        self.ITelegramBot.CheckChatStorages(message.chat.id)


    async def startgpt(self, message: types.Message):
        if self.CanUserUseBot(message.from_user.id):
            if not self.openai_entity.isBusy:
                self.openai_entity._SecureAIForAPerson(message.chat.id, message.from_user.id)
                await self.ITelegramBot.bot.send_message(message.chat.id, "Запускаю сессию с GPT-3.5-turbo")
                await self.ITelegramBot.bot.send_message(
                    message.chat.id,
                    "Задавайте вопрос, время ответа зависит от вопроса, в среднем около 5-30 секунд",
                )
                await self.ITelegramBot.bot.send_message(
                    message.chat.id, "Для завершения диалога с ChatGPT отправь /stopgpt"
                )
            else:
                await self.ITelegramBot.bot.send_message(message.chat.id, "Сессия уже запущена")
        else:
            await self.ITelegramBot.bot.send_message(
                message.chat.id,
                "Я вас не знаю, не пишите мне. Добавьте себя в список допущенных id, вот ваш id "
                + str(message.chat.id),
            )
    
    async def stopgpt(self, message: types.Message):
        if self.CanUserUseBot(message.from_user.id):
            if self.openai_entity.isBusy:
                self.openai_entity._CloseAISession()
                await self.ITelegramBot.bot.send_message(message.chat.id, "Завершаю сессию с GPT-3.5-turbo")
                await self.ITelegramBot.bot.send_message(message.chat.id, "История общения обнулена")
            else:
                await self.ITelegramBot.bot.send_message(message.chat.id, "Отсуствует сессия для завершения")
        else:
            await self.ITelegramBot.bot.send_message(
                message.chat.id,
                "Я вас не знаю, не пишите мне. Добавьте себя в список допущенных id, вот ваш id "
                + str(message.chat.id),
            )



