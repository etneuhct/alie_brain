from fastapi import BackgroundTasks, FastAPI
from pydantic import BaseModel

from exceptions import CloseConversationException
from memory import get_repeat, HISTORY, set_repeat, SHORT_TERM_HISTORY
from settings import ALL_COMMANDS
from utils import check_sentence, speak
from voice_commands.bot_identity_commands import BotIdentityCommand
from voice_commands.courtesy_commands import CourtesyCommand
from voice_commands.interruption_commands import CancelConversationCommands
from voice_commands.joke_commands import JokeCommand
from voice_commands.repeat_commands import RepeatCommands
from voice_commands.sport_commands import SportCommand


def init_command():
    rgx_commands = []
    for command in VOICE_COMMANDS:
        rgx_commands += [
            (rgx, command, command().get_priority()) for rgx in command(language='fr').get_rgx()
        ]
    return rgx_commands


VOICE_COMMANDS = [
    CourtesyCommand,
    CancelConversationCommands,
    RepeatCommands,
    BotIdentityCommand,
    JokeCommand,
    SportCommand
]

ALL_COMMANDS += init_command()

app = FastAPI()

class Message(BaseModel):
    sentence: str

class SpokenMessage(BaseModel):
    sentence: str
    room: str


@app.post("/")
async def on_message(message: Message, background_tasks: BackgroundTasks):
    sentence = message.sentence
    background_tasks.add_task(handle_sentence, sentence)
    return


@app.post("/speak")
async def on_speak(spoken_message: SpokenMessage):
    speak(spoken_message.sentence, spoken_message.room)
    return


async def handle_sentence(sentence):
    try:
        return sentence_analyse(sentence)
    except CloseConversationException:
        set_repeat(False)
        SHORT_TERM_HISTORY.clear()
        return

def sentence_analyse(sentence):
    if sentence:
        if get_repeat():
            last_index = HISTORY[-1]
            last_command = ALL_COMMANDS[last_index][1](language="fr")
            last_command.find_rgx(sentence)
        else:
            check_sentence(sentence, ALL_COMMANDS)
    return
