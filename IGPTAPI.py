import openai
import from tokens import openai_api_token

class gptEntity:
    def __init__(self):
        openai.api_key = openai_api_token
        self.messages = []
        self.gpton = False
        self.gptuserid = 0
        self.gptchatid = 0
        self.timer = None
