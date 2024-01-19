from aiogram import types, Bot
import asyncio
from tokens import allowidlist
from IGPTAPI import openAIEntity

class MessageHandler(Bot):

    def __init__(self, bot):
        self.ITelegramBot = bot
        self.openai_entity = openAIEntity()

    @staticmethod
    def UserCanUseBot(id):
        return id in allowidlist
    
    @staticmethod
    def MessageIsValid(message: types.Message):
        return not(message['from'].is_bot) and message.text != "" and len(message.text) > 2

    async def UseRightWayToSendBotAnswer(self, message: types.Message):
        generatedAnswer = self.ITelegramBot.GenerateMessage(self.ITelegramBot.HowBotWillAnswer())
        if generatedAnswer['AnswerWay'] == 'text':
            await self.ITelegramBot.bot.send_message(message.chat.id, generatedAnswer['Value'])
        elif generatedAnswer['AnswerWay'] == 'sticker':
            await self.ITelegramBot.bot.send_sticker(message.chat.id,sticker=generatedAnswer['Value'])

    async def Help(self, message: types.Message):
        if self.UserCanUseBot(message.chat.id):     
            await message.reply("\nПиши /demot для генерации демотиватора"
                                "\nПиши /startgpt для начала диалога с ChatGPT"
                                "\nДля завершения диалога с ChatGPT отправь /stopgpt"
                                "\nДля изменения шанса ответа отправь /setchance 0-100")
        else:
            await message.reply('Я вас не знаю, не пишите мне. Добавьте себя в список допущенных id, вот ваш id ' + str(message.chat.id))
        self.ITelegramBot.CheckChatStorages(message.chat.id)

    
    async def Startgpt(self, message: types.Message):
        if self.UserCanUseBot(message.from_user.id):
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
    
    async def Stopgpt(self, message: types.Message):
        if self.UserCanUseBot(message.from_user.id):
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

    async def SetAnswerchance(self, message: types.Message):
        if self.UserCanUseBot(message.from_user.id):
            messageArguments = message.get_args()
            if messageArguments.isdigit():
                self.answerChance = int(messageArguments)
                await self.ITelegramBot.bot.send_message(message.chat.id, "Шанс ответа изменен на " + messageArguments)
            else:
                await self.ITelegramBot.bot.send_message(message.chat.id, "Неправильный аргумент")
        else:
            await self.ITelegramBot.bot.send_message(message.chat.id, 'Я вас не знаю, не пишите мне. Добавьте себя в список допущенных id, вот ваш id ' + str(msg.chat.id))

    async def ProcessUserMessage(self, message: types.Message):
        if self.MessageIsValid(message) and self.UserCanUseBot(message.from_user.id):
            self.ITelegramBot.CheckChatStorages(message.from_user.id)
            if (self.openai_entity.CanUserUseGPT(message.from_user.id)):
                openaiResponse = self.openai_entity._GenerateAnswer(message.text)
                await self.ITelegramBot.bot.send_message(message.chat.id, openaiResponse)
            else:
                self.ITelegramBot.TryAddPhraseToBotDict(message.text)
                if (self.ITelegramBot.BotWillAnswer()):
                    await self.UseRightWayToSendBotAnswer(message)   

    async def ProcessUserSticker(self, message: types.Message):
        if (self.UserCanUseBot(message.from_user.id)):
            self.ITelegramBot.CheckChatStorages(message.from_user.id)
            self.ITelegramBot.TryAddStickerIdToBotDict(message.sticker.file_id)
        if (self.ITelegramBot.BotWillAnswer()):
            await self.UseRightWayToSendBotAnswer(message)