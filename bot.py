from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os
import mc
import random
import photo_editor
import openai
import openai.error
import tokens
import asyncio

'''bot settings'''

storage = MemoryStorage()

class TGBot:
    def __init__(self):
        self.token = tokens.bot_token
        self.bot = Bot(token=self.token)
        self.dp = Dispatcher(self.bot, storage=storage)
        self.allowid = tokens.allowidlist
        self.path_to_txt = 'Dialogs/'
        self.main_path = os.getcwd()
        self.chat_path = ''
        self.chat_paste_path = ''
        self.pics = ''
        self.stickers_path = ''
        self.chance = 50
    def checkpics(self):
        self.pics = os.listdir(path=self.chat_paste_path)
    def checkchatpath(self,id):
        if not os.path.exists(self.path_to_txt + str(id) + '/' + str(id) + '.txt'):
            os.mkdir(self.path_to_txt + str(id) + '/')
            f = open(self.path_to_txt + str(id) + '/' + str(id) + '.txt', 'w', encoding='utf8')
            f.write('')
            f.close()
            self.chat_path = self.path_to_txt + str(id) + '/' + str(id) + '.txt'
        else:
            self.chat_path = self.path_to_txt + str(id) + '/' + str(id) + '.txt'
        if not os.path.exists(self.path_to_txt + str(id) + '/' + str(id) + 'stickers' + '.txt'):
            f = open(self.path_to_txt + str(id) + '/' + str(id) + 'stickers' + '.txt', 'w', encoding='utf8')
            f.write('')
            f.close()
            self.stickers_path = self.path_to_txt + str(id) + '/' + str(id) + 'stickers' + '.txt'
        else:
            self.stickers_path = self.path_to_txt + str(id) + '/' + str(id) + 'stickers' + '.txt'
        if not os.path.exists(self.path_to_txt + str(id) + "/paste/"):
            os.mkdir(self.path_to_txt + str(id) + "/paste/")
            self.chat_paste_path = self.path_to_txt + str(id) + "/paste/"
        else:
            self.chat_paste_path = self.path_to_txt + str(id) + "/paste/"

'''gpt settings'''

class GPT:
    def __init__(self):
        openai.api_key = tokens.gpt_token
        self.messages = []
        self.gpton = False
        self.gptuserid = 0
        self.gptchatid = 0
        self.timer = None
        
bot = TGBot()
chat_gpt = GPT()

@bot.dp.message_handler(commands=['help'])
async def process_start_command(msg: types.Message):
    if msg.chat.id in bot.allowid:
        await msg.reply("\nПиши /demot для генерации демотиватора"
                        "\nПиши /startgpt для начала диалога с ChatGPT"
                        "\nДля завершения диалога с ChatGPT отправь /stopgpt"
                        "\nДля изменения шанса ответа отправь /setchance 0-100")
    else:
        await bot.bot.send_message(msg.chat.id, 'Я вас не знаю, не пишите мне. Добавьте себя в список допущенных id, вот ваш id ' + str(msg.chat.id))

async def timer_callback(seconds, msg):
    await asyncio.sleep(seconds)
    chat_gpt.gpton = False
    chat_gpt.gptuserid = 0
    chat_gpt.gptchatid = 0
    chat_gpt.messages = []
    await bot.bot.send_message(msg.chat.id,'Завершаю сессию с GPT-3.5-turbo')
    await bot.bot.send_message(msg.chat.id, 'История общения обнулена')
    chat_gpt.timer.cancel()

@bot.dp.message_handler(commands=['startgpt'])
async def startgpt(msg: types.Message):
    if msg.chat.id in bot.allowid:
        if not(chat_gpt.gpton):
            chat_gpt.gpton = True
            chat_gpt.gptuserid = msg.from_user.id
            chat_gpt.gptchatid = msg.chat.id
            chat_gpt.timer = asyncio.create_task(timer_callback(300,msg))
            await bot.bot.send_message(msg.chat.id, 'Запускаю сессию с GPT-3.5-turbo')
            await bot.bot.send_message(msg.chat.id, 'Задавайте вопрос, время ответа зависит от вопроса, в среднем около 5-30 секунд')
            await bot.bot.send_message(msg.chat.id, 'Для завершения диалога с ChatGPT отправь /stopgpt')
        else:
            await bot.bot.send_message(msg.chat.id, 'Сессия уже запущена')
    else:
        await bot.bot.send_message(msg.chat.id, 'Я вас не знаю, не пишите мне. Добавьте себя в список допущенных id, вот ваш id ' + str(msg.chat.id))

@bot.dp.message_handler(commands=['stopgpt'])
async def stopgpt(msg: types.Message):
    if msg.chat.id in bot.allowid:
        if chat_gpt.gpton:
            chat_gpt.gpton = False
            chat_gpt.gptuserid = 0
            chat_gpt.gptchatid = 0
            chat_gpt.messages = []
            chat_gpt.timer.cancel()
            await bot.bot.send_message(msg.chat.id,'Завершаю сессию с GPT-3.5-turbo')
            await bot.bot.send_message(msg.chat.id, 'История общения обнулена')
        else:
            await bot.bot.send_message(msg.chat.id, 'Отсуствует сессия для завершения')
    else:
        await bot.bot.send_message(msg.chat.id, 'Я вас не знаю, не пишите мне. Добавьте себя в список допущенных id, вот ваш id ' + str(msg.chat.id))

@bot.dp.message_handler(commands=['demot'])
async def dem(msg: types.Message):
    if msg.chat.id in bot.allowid:
        bot.checkchatpath(msg.chat.id)
        bot.checkpics()
        try:
            with open(bot.chat_path, encoding="utf8") as file:
                txt = file.read().split(",")
            generator = mc.PhraseGenerator(samples=txt)
            message = generator.generate_phrase()
            if len(message) < 4:
                raise Exception
            r = bot.pics[random.randint(0,len(bot.pics))-1]
            photo_editor.add_text(message,r,bot.chat_paste_path)
            col = int(r[0]) + 1
            r = r.replace(r[0], str(col))

            await bot.bot.send_photo(msg.chat.id, photo=open(bot.chat_paste_path + r, 'rb'))
            try:
                bot.checkpics()
                for file in bot.pics:
                    if int(file[0]) >= 4:
                        os.remove(bot.chat_paste_path + file)
            except Exception as e:
                print(e)
        except Exception as e:
            print(e)
            await bot.bot.send_message(msg.chat.id, 'Ошибка, попробуй еще раз')
    else:
        await bot.bot.send_message(msg.chat.id, 'Я вас не знаю, не пишите мне. Добавьте себя в список допущенных id, вот ваш id ' + str(msg.chat.id))

@bot.dp.message_handler(commands=['setchance'])
async def set_chance(msg: types.Message):
    if msg.chat.id in bot.allowid:
        arguments = msg.get_args()
        if arguments.isdigit():
            bot.chance = int(arguments)
            await bot.bot.send_message(msg.chat.id, "Шанс ответа изменен на " + arguments)
        else:
            await bot.bot.send_message(msg.chat.id, "Неправильный аргумент")
    else:
        await bot.bot.send_message(msg.chat.id, 'Я вас не знаю, не пишите мне. Добавьте себя в список допущенных id, вот ваш id ' + str(msg.chat.id))

@bot.dp.message_handler()
async def echo_message(msg: types.Message):
    if not msg['from'].is_bot and msg.text != "" and msg.chat.id in bot.allowid:
        if (chat_gpt.gpton and msg.from_user.id == chat_gpt.gptuserid and msg.chat.id == chat_gpt.gptchatid):
            try:
                content = msg.text
                chat_gpt.messages.append({"role": "user", "content": content})
                completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=chat_gpt.messages
                )
                chat_response = completion.choices[0].message.content
                chat_gpt.messages.append({"role": "assistant", "content": chat_response})
                chat_gpt.timer.cancel()
                chat_gpt.timer = asyncio.create_task(timer_callback(300,msg))
                await bot.bot.send_message(msg.chat.id, chat_response)

            except (openai.error.APIConnectionError,openai.error.APIError):
                await bot.bot.send_message(msg.chat.id,'Ошибка доступа к сервисам OpenAI, повторите запрос или попробуйте позже')
            except openai.error.AuthenticationError:
                await bot.bot.send_message(msg.chat.id,'Проблемы с токеном, попробуйте еще раз, если ничего не изменится замените токен ChatGPT')
            except (openai.error.RateLimitError, openai.error.InvalidRequestError):
                await bot.bot.send_message(msg.chat.id,'Лимит токенов достигнут, оптимизируйте свои запросы. Перезапустите ChatGPT')
            except Exception as e:
                print(e)
                await bot.bot.send_message(msg.chat.id,'Неизвестная ошибка. Перезапустите ChatGPT')
        else:
            bot.checkchatpath(msg.chat.id)
            bot.checkpics()

            with open(bot.chat_path, encoding="utf8") as file:
                txt = file.read().split(",")
            if not(msg.text.lower() in txt):
                with open(bot.chat_path, "a", encoding="utf8") as f:
                    f.write(msg.text + ",")
            with open(bot.stickers_path, encoding="utf8") as file:
                stick = file.read().split(",")
            r = random.choices(['yes', 'no'], weights=[bot.chance,100 - bot.chance])
            if len(txt) >= 4 and r == ['yes']:
                answ = random.choices([0,1,2],weights=[20,20,60])
                if answ == [0]:
                    try:
                        await bot.bot.send_sticker(msg.chat.id,sticker=stick[random.randint(0,len(stick))])
                    except:
                        pass
                elif answ == [1]:
                    try:
                        with open(bot.chat_path, encoding="utf8") as file:
                            txt = file.read().split(",")
                        generator = mc.PhraseGenerator(samples=txt)
                        message = generator.generate_phrase()
                        r = bot.pics[random.randint(0, len(bot.pics)) - 1]
                        photo_editor.add_text(message, r, bot.chat_paste_path)
                        col = int(r[0]) + 1
                        r = r.replace(r[0], str(col))

                        await bot.bot.send_photo(msg.chat.id, photo=open(bot.chat_paste_path + r, 'rb'))
                        try:
                            bot.checkpics()
                            for file in bot.pics:
                                if int(file[0]) >= 4:
                                    os.remove(bot.chat_paste_path + file)
                        except Exception as e:
                            print(e)
                    except Exception as e:
                        print(e)
                else:
                    generator = mc.PhraseGenerator(samples=txt)
                    message = generator.generate_phrase()
                    await msg.reply(message.lower())

    else:
        await bot.bot.send_message(msg.chat.id, 'Я вас не знаю, не пишите мне. Добавьте себя в список допущенных id, вот ваш id ' + str(msg.chat.id))

@bot.dp.message_handler(content_types=["sticker"])
async def echo_message(msg: types.Message):
    bot.checkchatpath(msg.chat.id)
    with open(bot.stickers_path, encoding="utf8") as file:
        stick = file.read().split(",")
    file_info = str(msg.sticker.file_id)
    if not(file_info in stick):
        with open(bot.stickers_path,"a", encoding="utf8") as f:
            f.write(file_info + ",")

@bot.dp.message_handler(content_types=['photo'])
async def photo(msg: types.Message):
    bot.checkchatpath(msg.chat.id)
    await msg.photo[-1].download(destination_file=bot.chat_paste_path + '0_' + str(random.randint(1,1000)) +'.jpg')

executor.start_polling(bot.dp)
