from api_requests import get_mouth_devices

HISTORY = []
SHORT_TERM_HISTORY = []
REPEAT = False

def set_repeat(value):
    globals()['REPEAT'] = value

def get_repeat():
    return REPEAT

MOUTH_DEVICES = {element['room']: element for element in get_mouth_devices()}
