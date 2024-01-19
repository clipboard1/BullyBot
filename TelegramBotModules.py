from mc import PhraseGenerator
from random import randint
from os import listdir, path, mkdir
from TelegramBot import TelegramBot
from photo_editor import addTextAndBorderToPhoto
class DemotivatorModule(TelegramBot):
    def __init__(self):
        self.pics_storage_path = ""
        if not(self._PicsStorageExists):
            self._CreatePicsStorage(self, id)
        self._SetPicsStorageExists(self, id)
    
    def _PicsStorageExists(id):
        return path.exists(f"{TelegramBot.path_to_txt}/{str(id)}/pics")

    def _CreatePicsStorage(id):
        mkdir(f"{TelegramBot.path_to_txt}/{str(id)}/pics")
    
    @staticmethod
    def _SetPicsStorageExists(id):
        DemotivatorModule.pics_storage_path = f"{TelegramBot.path_to_txt}/{str(id)}/pics"

    @staticmethod
    def _GetListOfPics():
        return listdir(path=DemotivatorModule.pics_storage_path)

    @staticmethod
    def _ChooseRandomPicture():
        arrayOfPictures = DemotivatorModule._GetListOfPics()
        return arrayOfPictures[randint(0, len(arrayOfPictures) - 1)]

    @staticmethod
    def _CreateDemotivator(text):
        phraseForDemotivator = DemotivatorModule._GeneratePhrase(TelegramBot.chat_storage_path)
        pathToRawImage = DemotivatorModule._ChooseRandomPicture()
        pathToNewImage = addTextAndBorderToPhoto(phraseForDemotivator, pathToRawImage)
        return pathToNewImage
        