import settings
from exceptions import CloseConversationException
from memory import SHORT_TERM_HISTORY, set_repeat
from settings import ALL_COMMANDS
from utils import check_rgx, check_sentence, add_short_term_memory, reset_short_term_memory, speak


class BaseVoiceCommand:

    def __init__(self, language='fr'):
        self.language = language
        self.again = False
        # self.engine = pyttsx3.init()
        # self.set_voice(language, self.engine)
        self.priority = 0
        self.bot_key = settings.BOT_KEY

    def set_voice(self, language, engine):
        for voice in engine.getProperty('voices'):
            if language in voice.languages:
                engine.setProperty('voice', voice.id)
                return True

    def list_context_rgx(self):
        return {}

    def context_rgx(self):
        rgx = self.list_context_rgx()
        return rgx[self.language] if self.language in rgx else []

    def get_priority(self):
        return self.priority

    def bot_talk(self, sentence):
        speak(sentence)

    def list_rgx(self):
        raise NotImplementedError

    def get_rgx(self):
        rgx = self.list_rgx()
        try:
            return rgx[self.language]
        except KeyError:
            return []

    def process(self, sentence, process, *args):
        raise NotImplementedError

    def pre_process(self, sentence, *args):
        check_sentence(sentence, [cmd for cmd in ALL_COMMANDS if cmd[2] > self.get_priority()])

    def post_process(self, sentence, rgx, *args):
        set_repeat(self.again)
        if self.again:
            add_short_term_memory((sentence, rgx, *args))
        else:
            reset_short_term_memory()

    def find_rgx(self, sentence):
        self.pre_process(sentence)
        for rgx in self.get_rgx() + self.context_rgx():
            values = check_rgx(rgx, sentence)
            if values:
                return self.run(sentence, rgx, *values)

    def run(self, sentence, rgx, *args):
        self.process(sentence, rgx, *args)
        self.post_process(sentence, rgx, *args)
        return sentence, *args

    @staticmethod
    def get_history():
        return SHORT_TERM_HISTORY

