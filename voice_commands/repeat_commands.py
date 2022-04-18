from exceptions import CloseConversationException
from voice_commands.base_command import BaseVoiceCommand
from memory import HISTORY, SHORT_TERM_HISTORY


class RepeatCommands(BaseVoiceCommand):

    def list_rgx(self):
        return {
            'fr': [
                '(répète) ce que je dis*'
            ]
        }

    def list_context_rgx(self):
        return {
            "fr": ['(.*)']
        }

    def process(self, sentence, *args):
        if len(self.get_history()) == 0:
            self.bot_talk('Ok ! Je vais répéter ce que tu dis.')
        else:
            self.bot_talk(sentence)
        self.again = True
