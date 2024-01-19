import tokens
from TelegramBotMessageHandler import MessageHandler
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from os import listdir, path, mkdir
from random import choices, randint
from mc import PhraseGenerator

class TelegramBot:
    def __init__(self):
        storage = MemoryStorage()
        self.token = tokens.telegram_api_token
        self.bot = Bot(token=self.token)
        self.dispatcher = Dispatcher(self.bot, storage=storage)
        self.path_to_txt = "Dialogs"
        self.chat_storage_path = ""
        self.stickers_storage_path = ""
        self.pics = ""
        self.answerChance = 50
        self.message_handler = MessageHandler(self)

    
    def CheckChatStorages(self, id):
        if not (self._ChatStorageExists(id)):
            self._CreateChatStorage(id)
        self._SetChatStoragePath(id)
        if not (self._StickersStorageExists(id)):
            self._CreateStickersStorage(id)
        self._SetStickersStoragePath(id)

    
    def _ChatStorageExists(self, id):
        return path.exists(f"{self.path_to_txt}/{str(id)}/{str(id)}.txt")

    
    def _StickersStorageExists(self, id):
        return path.exists(f"{self.path_to_txt}/{str(id)}/{str(id)}stickers.txt")

    
    def _CreateChatStorage(self, id):
        mkdir(f"{self.path_to_txt}/{str(id)}/")
        self._CreateTxtStorage("", id)
    
    def _CreateStickersStorage(self, id):
        self._CreateTxtStorage( "stickers", id)

    
    def _CreateTxtStorage(self, name, id):
        pathToStorage = f"{self.path_to_txt}/{str(id)}/{str(id)}{name}.txt"
        with open(pathToStorage, "w") as storageFile:
            storageFile.write("")

    
    def _SetChatStoragePath(self, id):
        self.chat_storage_path = f"{self.path_to_txt}/{str(id)}/{str(id)}.txt"

    
    def _SetStickersStoragePath(self, id):
        self.stickers_storage_path = (
            f"{self.path_to_txt}/{str(id)}/{str(id)}stickers.txt"
        )
    
    @staticmethod
    def _GetAndSplitAllData(pathToStorage):
        with open(pathToStorage, encoding="utf8") as file:
            return file.read().split(",")

    def _GeneratePhrase(self):
            samplesForGenerator = self._GetAndSplitAllData(self.chat_storage_path)
            phraseGenerator = PhraseGenerator(samples=samplesForGenerator)
            generatedPhrase = phraseGenerator.generate_phrase()
            if len(generatedPhrase) < 3:
                generatedPhrase = "Error"
            return generatedPhrase
    
    def TryAddPhraseToBotDict(self, word):
        if not(word.lower() in self._GetAndSplitAllData(self.chat_storage_path)):
            with open(self.chat_storage_path, "a", encoding="utf8") as messagesFile:
                    messagesFile.write(f'{word},')

    def _ChooseRandomSticker(self):
        stickersStorage = self._GetAndSplitAllData(self.stickers_storage_path)
        try:
            return stickersStorage[randint(0, len(stickersStorage))]
        except Exception as exception:
            print(exception)
            return "CAACAgIAAxkBAAEBNB1lqt1DrpkldtSDmdo8gcx162H6ygACqSEAAsNGaEsRQ1Q-0S5RGDQE"

    def TryAddStickerIdToBotDict(self, stickerId):
        if not(stickerId in self._GetAndSplitAllData(self.stickers_storage_path)):
            with open(self.stickers_storage_path, "a", encoding="utf8") as stickersIdFile:
                    stickersIdFile.write(f'{stickerId},')
                    
    def BotWillAnswer(self):
       magicAnswer = choices(['yes', 'no'], weights=[self.answerChance,100 - self.answerChance])
       messagesDict = self._GetAndSplitAllData(self.chat_storage_path)
       stickersDict = self._GetAndSplitAllData(self.stickers_storage_path)
       whatsWrong = magicAnswer == ['yes'] and (len(messagesDict) > 0 or len(stickersDict) > 0)
       return whatsWrong

    def HowBotWillAnswer(self):
        magicAnswer = choices(['text', 'sticker', 'demotivator'], weights=[20, 60, 20])
        return magicAnswer[0]
    
    def GenerateMessage(self, magicAnswer):
        waysToAnswer = {
            'text': self._GeneratePhrase(),
            'sticker': self._ChooseRandomSticker(),
            'demot' : None
        }

        return {'AnswerWay': magicAnswer, 'Value': waysToAnswer[magicAnswer]}

    def register_message_handlers(self):
        self.dispatcher.register_message_handler(self.message_handler.Help, commands=['help'])
        self.dispatcher.register_message_handler(self.message_handler.Startgpt, commands=['startgpt'])
        self.dispatcher.register_message_handler(self.message_handler.Stopgpt, commands=['stopgpt'])
        self.dispatcher.register_message_handler(self.message_handler.SetAnswerchance, commands=['setchance'])
        self.dispatcher.register_message_handler(self.message_handler.ProcessUserMessage)
        self.dispatcher.register_message_handler(self.message_handler.ProcessUserSticker, content_types=["sticker"])
        