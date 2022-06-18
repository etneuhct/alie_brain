import os

ENV = os.getenv('ENV', 'dev')
if ENV.lower() == 'prod':
    pass
else:
    pass

ALL_COMMANDS = []

BOT_KEY = "151dS"

BOT_IDENTITY_URL = "http://api.alie.home/api/bot/"
BOT_MOUTH_DEVICES_URL = "http://api.alie.home/api/mouth/"
BOT_JOKE_URL = f"http://api.joke.home/joke/"
DUMBBELL_URL = f"http://api.fitness.home/dumbbell/"
ABDO_URL = f"http://api.fitness.home/abdo/"

