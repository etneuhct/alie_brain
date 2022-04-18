from api_requests import get_bot_identity, set_bot_identity
from voice_commands.base_command import BaseVoiceCommand


class BotIdentityCommand(BaseVoiceCommand):

    def list_rgx(self):
        return {
            'fr': [
                '(et si on passait à ta configuration)*',
                "ton nom est ([a-zA-ZÂÃÄÀÁÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿ]*)",
                "(comment tu t'appelles)"
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
            self.bot_talk('Très bien')
            self.again = False
        elif index in [1]:
            name = args[0]
            self.set_name(name)
            self.again = False

        elif index in [2]:
            self.get_name()
            self.again = False

    def set_name(self, name):
        set_bot_identity({'name': name})
        self.bot_talk(f'Très bien. Je m\'appelle {name}')

    def get_name(self):
        identity = get_bot_identity()
        try:
            name = identity['name']
        except TypeError:
            pass
        else:
            if name:
                self.bot_talk(f"Je m'appelle {name}")
                return

        self.bot_talk("Je n'ai présentement pas de nom.")