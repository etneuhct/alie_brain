from exceptions import CloseConversationException, StopProgramException
from voice_commands.base_command import BaseVoiceCommand


class CancelConversationCommands(BaseVoiceCommand):

    def list_rgx(self):
        return {
            'fr': [
                '(stop).*',
                '(ta gueule).*',
                '(ferme ta gueule).*',
                '(extinction des feux).*'
            ]
        }

    def get_priority(self):
        return 99

    def process(self, sentence, rgx, *args):
        if self.language == 'fr':
            self.fr_process(sentence, rgx, *args)

    def fr_process(self, sentence, rgx, *args):
        try:
            index = self.get_rgx().index(rgx)
        except ValueError:
            index = None
        if index in [0, 1, 2]:
            self.bot_talk('Très bien')
            raise CloseConversationException
        else:
            raise StopProgramException
