from api_requests import get_random_joke
from voice_commands.base_command import BaseVoiceCommand


class JokeCommand(BaseVoiceCommand):

    def list_rgx(self):
        return {
            'fr': [
                '(raconte-moi une blague)*'
            ]
        }

    def process(self, sentence, rgx, *args):
        if self.language == 'fr':
            self.fr_process(sentence, rgx, *args)

    def fr_process(self, sentence, rgx, *args):
        try:
            index = self.get_rgx().index(rgx)
        except ValueError:
            index = None
        if index == 0:
            self.get_joke()
            self.again = False

    def get_joke(self):
        joke = get_random_joke()
        sentence = joke['joke']
        if joke['answer']:
            sentence = f'{sentence} {joke["answer"]}'
        self.bot_talk(sentence)
