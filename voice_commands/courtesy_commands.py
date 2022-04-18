from voice_commands.base_command import BaseVoiceCommand


class CourtesyCommand(BaseVoiceCommand):

    def list_rgx(self):
        return {
            'fr': [
                '(bonjour|au revoir|comment ça va|merci|je vais bien)*'
            ]
        }

    def process(self, sentence, rgx,  *args):
        word = args[0]
        if word in ['bonjour']:
            self.bot_talk('bonjour')
            self.again = False
        elif word in ['au revoir']:
            self.bot_talk('au revoir')
            self.again = False
        elif word in ['comment ça va']:
            self.bot_talk('Je vais bien merci et toi ?')
            self.again = True
        elif word in ['merci']:
            self.bot_talk('De rien !')
            self.again = False
        elif word in ['je vais bien']:
            self.bot_talk('Parfait alors !')
            self.again = False
