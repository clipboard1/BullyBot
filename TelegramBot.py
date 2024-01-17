import tokens
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from os import listdir, path, mkdir
from TelegramBotMessageHandler import MessageHandler

class TelegramBot:
    def __init__(self):
        storage = MemoryStorage()
        self.token = tokens.telegram_api_token
        self.bot = Bot(token=self.token)
        self.dispatcher = Dispatcher(self.bot, storage=storage)
        self.path_to_txt = "Dialogs/"
        self.chat_storage_path = ""
        self.stickers_storage_path = ""
        self.pics = ""
        self.chance = 50
        self.message_handler = MessageHandler(self)

    
    def CheckChatStorages(bot, id):
        if not (bot._ChatStorageExists):
            bot._CreateChatStorage(id)
        bot._SetChatStoragePath(id)
        if not (bot._StickersStorageExists(id)):
            bot._CreateStickersStorage(id)
        bot._SetStickersStoragePath(id)

    
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
   
    def register_message_handlers(self):
        self.dispatcher.register_message_handler(self.message_handler.help, commands=['help'])
        self.dispatcher.register_message_handler(self.message_handler.startgpt, commands=['startgpt'])
        self.dispatcher.register_message_handler(self.message_handler.stopgpt, commands=['stopgpt'])
