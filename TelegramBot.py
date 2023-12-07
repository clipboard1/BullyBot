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
        self.bot = Bot(token=self.token)
        self.dp = Dispatcher(self.bot, storage=storage)
        self.allowid = tokens.allowidlist
        self.path_to_txt = 'Dialogs/'
        self.main_path = os.getcwd()
        self.chat_storage_path = ''
        self.stickers_storage_path = ''
        self.chat_paste_path = ''
        self.pics = ''
        
        self.chance = 50
        
    def __GetListOfPics(self):
        self.pics = listdir(path=self.chat_paste_path)
        
    def __checkchatpath(self,id):
        if not os.path.exists(self.path_to_txt + str(id) + '/' + str(id) + '.txt'):
            os.mkdir(self.path_to_txt + str(id) + '/')
            f = open(self.path_to_txt + str(id) + '/' + str(id) + '.txt', 'w', encoding='utf8')
            f.write('')
            f.close()
            self.chat_storage_path = self.path_to_txt + str(id) + '/' + str(id) + '.txt'
        else:
            self.chat_storage_path = self.path_to_txt + str(id) + '/' + str(id) + '.txt'
        if not os.path.exists(self.path_to_txt + str(id) + '/' + str(id) + 'stickers' + '.txt'):
            f = open(self.path_to_txt + str(id) + '/' + str(id) + 'stickers' + '.txt', 'w', encoding='utf8')
            f.write('')
            f.close()
            self.stickers_storage_path = self.path_to_txt + str(id) + '/' + str(id) + 'stickers' + '.txt'
        else:
            self.stickers_storage_path = self.path_to_txt + str(id) + '/' + str(id) + 'stickers' + '.txt'
        if not os.path.exists(self.path_to_txt + str(id) + "/paste/"):
            os.mkdir(self.path_to_txt + str(id) + "/paste/")
            self.chat_paste_path = self.path_to_txt + str(id) + "/paste/"
        else:
            self.chat_paste_path = self.path_to_txt + str(id) + "/paste/"
    
    
    
    def __ChatStorageExists(self, id):
        return path.exists(f"{self.path_to_txt}/{str(id)}/{str(id)}.txt")
    
    def __StickersStorageExists(self, id):
        return path.exists(f"{self.path_to_txt}/{str(id)}/{str(id)}stickers.txt")

    def __CreateChatStorage(self, id):
        mkdir(f"{self.path_to_txt}/{str(id)}/")
        self.__CreateTxtStorage(self, '', id)
    
    def __CreateStickersStorage(self, id):
        self.__CreateChatStorage(self, "stickers", id)

    def __CreateTxtStorage(self, name, id):
        with open(f"{self.path_to_txt}/{str(id)}/{str(id)}{name}.txt", 'w') as storageFile:
            storageFile.write('')

    def __SetChatStoragePath(self, id):
        self.chat_storage_path = f"{self.path_to_txt}/{str(id)}/{str(id)}.txt"
    
    def __SetStickersStoragePath(self, id):
        self.stickers_storage_path = f"{self.path_to_txt}/{str(id)}/{str(id)}stickers.txt"

    def __StartPolling(self):
        executor.start_polling(self)
     