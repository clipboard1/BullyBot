import tokens
from random import randint
from mc import PhraseGenerator
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from os import listdir, path, mkdir


class TelegramBot:
    def __init__(self):
        storage = MemoryStorage()
        self.token = tokens.telegram_api_token
        self.aiogramClient = Bot(token=self.token)
        self.dispatcher = Dispatcher(self.bot, storage=storage)
        self.allowidlist = tokens.allowidlist
        self.path_to_txt = "Dialogs/"
        self.chat_storage_path = ""
        self.stickers_storage_path = ""
        self.pics_storage_path = ""
        self.pics = ""
        self.chance = 50
    
    @staticmethod
    def _CheckChatStorages(id):
        if not (TelegramBot._ChatStorageExists):
            TelegramBot._CreateChatStorage(self, id)
        TelegramBot._SetChatStoragePath(self, id)
        if not (TelegramBot._StickersStorageExists(self, id)):
            TelegramBot._CreateChatStorage(self, id)
        TelegramBot._SetStickersStoragePath(self, id)
        if not(TelegramBot._PicsStorageExists):
            TelegramBot._CreatePicsStorage(self, id)
        TelegramBot._SetPicsStorageExists(self, id)

    @staticmethod
    def _ChatStorageExists(self, id):
        return path.exists(f"{TelegramBot.path_to_txt}/{str(id)}/{str(id)}.txt")

    @staticmethod
    def _StickersStorageExists(self, id):
        return path.exists(f"{TelegramBot.path_to_txt}/{str(id)}/{str(id)}stickers.txt")

    @staticmethod
    def _PicsStorageExists(self, id):
        return path.exists(f"{TelegramBot.path_to_txt}/{str(id)}/pics")

    @staticmethod
    def _CreateChatStorage(self, id):
        mkdir(f"{TelegramBot.path_to_txt}/{str(id)}/")
        TelegramBot._CreateTxtStorage(self, "", id)

    @staticmethod
    def _CreateStickersStorage(self, id):
        TelegramBot._CreateTxtStorage(self, "stickers", id)

    @staticmethod
    def _CreateTxtStorage(self, name, id):
        pathToStorage = f"{TelegramBot.path_to_txt}/{str(id)}/{str(id)}{name}.txt"
        with open(pathToStorage, "w") as storageFile:
            storageFile.write("")

    @staticmethod
    def _CreatePicsStorage(self, id):
        mkdir(f"{TelegramBot.path_to_txt}/{str(id)}/pics")

    @staticmethod
    def _SetChatStoragePath(self, id):
        TelegramBot.chat_storage_path = f"{TelegramBot.path_to_txt}/{str(id)}/{str(id)}.txt"

    @staticmethod
    def _SetStickersStoragePath(self, id):
        TelegramBot.stickers_storage_path = (
            f"{TelegramBot.path_to_txt}/{str(id)}/{str(id)}stickers.txt"
        )

    @staticmethod
    def _SetPicsStorageExists(self, id):
        TelegramBot.pics_storage_path = f"{TelegramBot.path_to_txt}/{str(id)}/pics"

    @staticmethod
    def _GetAndSplitAllMessages(pathToMessages):
        with open(pathToMessages, encoding="utf8") as file:
            return file.read().split(",")

    @staticmethod
    def _GeneratePhrase(pathToMessages):
            samplesForGenerator = TelegramBot._GetAndSplitAllMessages(pathToMessages)
            phraseGenerator = PhraseGenerator(samples=samplesForGenerator)
            generatedPhrase = phraseGenerator.generate_phrase()
            if len(generatedPhrase < 3):
                generatedPhrase = "Error"
            return generatedPhrase

    @staticmethod
    def _GetListOfPics():
        return listdir(path=TelegramBot.pics_storage_path)

    def _ChooseRandomPicture(arrayOfPictures):
        return arrayOfPictures[randint(0, len(arrayOfPictures) - 1)]

    def _CreateDemotivator(text):
        pass
        
    def _StartPolling(self):
        executor.start_polling(self)

    