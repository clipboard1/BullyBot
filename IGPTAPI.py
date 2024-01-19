import openai
import openai.error
from tokens import openai_api_token
class openAIEntity:
    def __init__(self):
        
        openai.api_key = openai_api_token
        self.messages = []
        self.isBusy = False
        self.user_id = 0
        self.chat_id = 0
    
    def _AddContentAsUser(self, content):
        self.messages.append({"role": "user", "content": content})

    def _AddContentAsAssistant(self, content):
        self.messages.append({"role": "assistant", "content": content})

    def _SecureAIForAPerson(self, chat_id, user_id):
        self.isBusy = True
        self.chatid = chat_id
        self.user_id = user_id

    def _CloseAISession(self):
        self.isBusy = False
        self.chat_id = 0
        self.user_id = 0
        self.messages = []

    def CanUserUseGPT(self, id):
        return id == self.user_id

    @staticmethod
    def _HandlerOpenAIError(openaiError: Exception):
        errorsCodesAndAnswers = {
            openai.error.APIConnectionError: "Ошибка доступа к сервисам OpenAI, повторите запрос или попробуйте позже",
            openai.error.APIError: "Ошибка доступа к сервисам OpenAI, повторите запрос или попробуйте позже",
            openai.error.AuthenticationError: "Проблемы с токеном, попробуйте еще раз, если ничего не изменится замените токен доступа к сервисам OpenAI",
            openai.error.RateLimitError: "Лимит токенов достигнут, оптимизируйте свои запросы. Перезапустите ChatGPT",
            openai.error.InvalidRequestError: "Лимит токенов достигнут, оптимизируйте свои запросы. Перезапустите ChatGPT",
            Exception: "Неизвестная ошибка. Перезапустите ChatGPT"    
        }
        return errorsCodesAndAnswers[openaiError]

    def _GenerateAnswer(self, question):
        try:
            self._AddContentAsUser(question)
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.messages)
            openai_response = completion.choices[0].message.content
            self._AddContentAsAssistant(openai_response)
            return openai_response
        except Exception as generateAnswerException:
            return self._HandlerOpenAIError(type(generateAnswerException))