import tokens
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
        self.chat_pics_path = ""
        self.pics = ""
        self.chance = 50

    def _GetListOfPics(self):
        self.pics = listdir(path=self.chat_paste_path)

    def _CheckChatStorages(self, id):
        if not (self.__ChatStorageExists):
            self.__CreateChatStorage(self, id)
        self._SetChatStoragePath(self, id)
        if not (self._StickersStorageExists(self, id)):
            self._CreateChatStorage(self, id)
        self._SetStickersStoragePath(self, id)
        if

    def _ChatStorageExists(self, id):
        return path.exists(f"{self.path_to_txt}/{str(id)}/{str(id)}.txt")

    def _StickersStorageExists(self, id):
        return path.exists(f"{self.path_to_txt}/{str(id)}/{str(id)}stickers.txt")

    def _PicsStorageExists(self, id):
        return path.exists(f"{self.path_to_txt}/{str(id)}/pics")

    def _CreateChatStorage(self, id):
        mkdir(f"{self.path_to_txt}/{str(id)}/")
        self.__CreateTxtStorage(self, "", id)

    def _CreateStickersStorage(self, id):
        self.__CreateTxtStorage(self, "stickers", id)

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

    def _StartPolling(self):
        executor.start_polling(self)

    