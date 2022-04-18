import datetime

from api_requests import bulk_create_dumbbell, bulk_create_abdo
from voice_commands.base_command import BaseVoiceCommand


class SportCommand(BaseVoiceCommand):

    def list_rgx(self):
        return {
            'fr': [
                '([0-9]*) (abdos|haltères) chaque ([0-9]*) ([a-zA-Z]*)'
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
            self.bot_talk('Très bien, je fais ça')

            count, category, frequency, _ = args
            date = datetime.datetime.now()
            record_activity = self.record(category)
            response_status = record_activity(date, int(count), int(frequency))

            if response_status == 200:
                self.bot_talk("C'est fait")
            else:
                self.bot_talk('Sanapassarapa')
            self.again = False

    @staticmethod
    def record(category):
        return {
            'abdos': bulk_create_abdo,
            'haltères': bulk_create_dumbbell
        }[category]
