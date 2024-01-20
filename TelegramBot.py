from TelegramBotMessageHandler import MessageHandler
from photoEditor import addTextAndBorderToPhoto
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from os import listdir, path, mkdir
from random import choices, randint
from mc import PhraseGenerator
import ast

class TelegramBot:
    def __init__(self):
        self.telegramAPIToken = ""
        self.openaiToken = ""
        self.allowIDList = []
        self.UpdateTokensValues()
        self.BaseFolder = "Dialogs"
        self.ChatStoragePath = ""
        self.StickersStoragePath = ""
        self.PicsStoragePath = ""
        self.answerChance = 50
        self.message_handler = MessageHandler(self)
        self.storage = MemoryStorage()
        self.bot = Bot(token=self.telegramAPIToken)
        self.dispatcher = Dispatcher(self.bot, storage=self.storage)

    def CheckChatStorages(self, id):
        if not (self._ChatStorageExists(id)):
            self._CreateChatStorage(id)
        self._SetChatStoragePath(id)
        if not (self._StickersStorageExists(id)):
            self._CreateStickersStorage(id)
        self._SetStickersStoragePath(id)
        if not (self._PicsStorageExists(id)):
            self._CreatePicsStorage(id)
        self._SetPicsStorage(id)

    def _ChatStorageExists(self, id):
        return path.exists(f"{self.BaseFolder}/{str(id)}/{str(id)}.txt")

    def _StickersStorageExists(self, id):
        return path.exists(f"{self.BaseFolder}/{str(id)}/{str(id)}stickers.txt")

    def _PicsStorageExists(self, id):
        return path.exists(f"{self.BaseFolder}/{str(id)}/pics")

    def _CreateChatStorage(self, id):
        mkdir(f"{self.BaseFolder}/{str(id)}/")
        self._CreateTxtStorage("", id)
    
    def _CreateStickersStorage(self, id):
        self._CreateTxtStorage( "stickers", id)

    def _CreatePicsStorage(self, id):
        mkdir(f"{self.BaseFolder}/{str(id)}/pics/")
    
    def _CreateTxtStorage(self, name, id):
        pathToStorage = f"{self.BaseFolder}/{str(id)}/{str(id)}{name}.txt"
        with open(pathToStorage, "w") as storageFile:
            storageFile.write("")

    def UpdateTokensValues(self):
        tokens = self._ReadTokensValues()
        self.telegramAPIToken = tokens["telegramAPIToken"]
        self.openaiToken = tokens["openaiAPIToken"]
        self.allowIDList = tokens["allowidlist"]

    def _SetChatStoragePath(self, id):
        self.ChatStoragePath = f"{self.BaseFolder}/{str(id)}/{str(id)}.txt"

    def _SetStickersStoragePath(self, id):
        self.StickersStoragePath = f"{self.BaseFolder}/{str(id)}/{str(id)}stickers.txt"
    
    def _SetPicsStorage(self, id):
        self.PicsStoragePath = f"{self.BaseFolder}/{str(id)}/pics"

    @staticmethod
    def _ReadTokensValues():
        tokens = {}
        with open('tokens.txt', 'r') as f:
            for line in f:
                partsOfLine = line.strip().split(':', 1)
                key = partsOfLine[0].strip()
                value = partsOfLine[1].strip()
                if '[' in value and ']' in value:
                    value = ast.literal_eval(value)
                tokens[key] = value
        return tokens

    @staticmethod
    def _GetAndSplitAllData(pathToStorage):
        with open(pathToStorage, encoding="utf8") as file:
            return file.read().split(",")

    def _GeneratePhrase(self):
            samplesForGenerator = self._GetAndSplitAllData(self.ChatStoragePath)
            phraseGenerator = PhraseGenerator(samples=samplesForGenerator)
            generatedPhrase = phraseGenerator.generate_phrase()
            if len(generatedPhrase) < 3:
                generatedPhrase = "Error"
            return generatedPhrase
    
    def TryAddPhraseToBotDict(self, word):
        if not(word.lower() in self._GetAndSplitAllData(self.ChatStoragePath)):
            with open(self.ChatStoragePath, "a", encoding="utf8") as messagesFile:
                    messagesFile.write(f'{word},')

    def _ChooseRandomSticker(self):
        stickersStorage = self._GetAndSplitAllData(self.StickersStoragePath)
        try:
            return stickersStorage[randint(0, len(stickersStorage))]
        except Exception as exception:
            print(exception)
            return "CAACAgIAAxkBAAEBNB1lqt1DrpkldtSDmdo8gcx162H6ygACqSEAAsNGaEsRQ1Q-0S5RGDQE"

    def TryAddStickerIdToBotDict(self, stickerId):
        if not(stickerId in self._GetAndSplitAllData(self.StickersStoragePath)):
            with open(self.StickersStoragePath, "a", encoding="utf8") as stickersIdFile:
                    stickersIdFile.write(f'{stickerId},')
                    
    def BotWillAnswer(self):
       magicAnswer = choices(['yes', 'no'], weights=[self.answerChance,100 - self.answerChance])
       messagesDict = self._GetAndSplitAllData(self.ChatStoragePath)
       stickersDict = self._GetAndSplitAllData(self.StickersStoragePath)
       whatsWrong = magicAnswer == ['yes'] and (len(messagesDict) > 0 or len(stickersDict) > 0)
       return whatsWrong

    def HowBotWillAnswer(self):
        magicAnswer = choices(['text', 'sticker', 'demotivator'], weights=[0, 0, 100])
        return magicAnswer[0]
    
    def GenerateMessage(self, magicAnswer):
        waysToAnswer = {
            'text': self._GeneratePhrase(),
            'sticker': self._ChooseRandomSticker(),
            'demotivator' : self.CreateDemotivator()
        }
        return {'AnswerWay': magicAnswer, 'Value': waysToAnswer[magicAnswer]}

    def _GetListOfPics(self):
        arrayOfPaths = []
        for picPath in listdir(path=self.PicsStoragePath):
            arrayOfPaths.append(path.join(self.PicsStoragePath, picPath))
        return arrayOfPaths

    def _ChooseRandomPicture(self):
        arrayOfPictures = self._GetListOfPics()
        return arrayOfPictures[randint(0, len(arrayOfPictures) - 1)]

    def CreateDemotivator(self):
        phraseForDemotivator = self._GeneratePhrase()
        pathToRawImage = self._ChooseRandomPicture()
        pathToNewImage = addTextAndBorderToPhoto(phraseForDemotivator, pathToRawImage)
        return pathToNewImage

    def _GeneratePathForPicture(self):
        return f"{self.PicsStoragePath}/0_{str(randint(1,1000))}.jpg" 

    async def SuccessfulDownloadPhotoFromMessage(self, message):
        pathToNewPicture = self._GeneratePathForPicture()
        await message.photo[-1].download(destination_file=pathToNewPicture)
        return path.exists(pathToNewPicture)

    def register_message_handlers(self):
        self.dispatcher.register_message_handler(self.message_handler.Help, commands=['help'])
        self.dispatcher.register_message_handler(self.message_handler.Startgpt, commands=['startgpt'])
        self.dispatcher.register_message_handler(self.message_handler.Stopgpt, commands=['stopgpt'])
        self.dispatcher.register_message_handler(self.message_handler.SetAnswerchance, commands=['setchance'])
        self.dispatcher.register_message_handler(self.message_handler.Demotivator, commands=['demot'])
        self.dispatcher.register_message_handler(self.message_handler.ProcessUserSticker, content_types=["sticker"])
        self.dispatcher.register_message_handler(self.message_handler.ProcessUserPhoto, content_types=["photo"])
        self.dispatcher.register_message_handler(self.message_handler.ProcessUserMessage)
        