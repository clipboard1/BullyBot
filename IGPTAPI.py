import openai
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

    def _GenerateAnswer(self, question):
        self._AddContentAsUser(question)
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages)
        openai_response = completion.choices[0].message.content
        self._AddContentAsAssistant(openai_response)
        return openai_response
