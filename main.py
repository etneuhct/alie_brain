import io

import requests
import speech_recognition as sr
from fastapi import BackgroundTasks, FastAPI
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

from exceptions import CloseConversationException
from memory import get_repeat, HISTORY, set_repeat, SHORT_TERM_HISTORY
from settings import ALL_COMMANDS
from utils import check_sentence
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
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Message(BaseModel):
    sentence: str


class SpokenMessage(BaseModel):
    file_url: str
    room: str


@app.post("/")
async def on_message(message: Message, background_tasks: BackgroundTasks):
    sentence = message.sentence
    background_tasks.add_task(handle_sentence, sentence)
    return


@app.post("/speak")
async def on_speak(spoken_message: SpokenMessage, background_tasks: BackgroundTasks):
    audio_file = download_file(spoken_message.file_url)
    r = sr.Recognizer()
    audio_file = sr.AudioFile(audio_file)
    with audio_file as source:
        audio = r.record(source)
    sentence = r.recognize_google(audio, language='fr-FR')
    background_tasks.add_task(handle_sentence, sentence)
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


def download_file(url):
    data = {
        "allow_redirects": False
    }
    req = requests.get(url, **data)
    return io.BytesIO(req.content)
