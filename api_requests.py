import datetime

import requests

import settings


def get_bot_identity():
    url = settings.BOT_IDENTITY_URL
    response = requests.get(f"{url}{settings.BOT_KEY}")
    status = response.status_code
    if status == 200:
        data = response.json()
        return data
    else:
        return


def set_bot_identity(data):
    url = settings.BOT_IDENTITY_URL
    response = requests.post(f"{url}", json={**data, 'key': settings.BOT_KEY})
    status = response.status_code
    if status == 201:
        data = response.json()
        return data
    else:
        return


def get_mouth_devices():
    url = settings.BOT_MOUTH_DEVICES_URL
    response = requests.get(url)
    return response.json()


def get_joke_stats():
    url = f"{settings.BOT_JOKE_URL}stats"
    response = requests.get(url)
    return response.json()


def get_random_joke():
    url = f"{settings.BOT_JOKE_URL}random"
    response = requests.get(url)
    return response.json()


def bulk_create_dumbbell(start, count, frequency):
    url = f"{settings.DUMBBELL_URL}bulk/"

    result = []
    for i in range(count):
        start = start - datetime.timedelta(seconds=frequency)
        result.append({'date': start.strftime('%Y-%m-%dT%H:%M:%S')})
    response = requests.post(url, json=result)
    return response.status_code


def bulk_create_abdo(start, count, frequency):
    url = f"{settings.ABDO_URL}bulk/"
    result = []
    for i in range(count):
        start = start - datetime.timedelta(seconds=frequency)
        result.append({'date': start.strftime('%Y-%m-%dT%H:%M:%S')})
    response = requests.post(url, json=result)
    return response.status_code
