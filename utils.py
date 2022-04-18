import re

import paramiko

from memory import SHORT_TERM_HISTORY, HISTORY, MOUTH_DEVICES


def check_rgx(rgx, sentence):
    match = re.match(rgx, sentence)
    if match:
        return match.groups()
    return match


def check_sentence(sentence, all_commands):
    i = 0
    for rgx_command in all_commands:
        values = check_rgx(rgx_command[0], sentence)
        if (
                values is not None and not isinstance(values, tuple)) or (
                isinstance(values, tuple) and values[0] is not None):
            HISTORY.append(i)
            rgx_command[1](language='fr').run(sentence, rgx_command[0], *values)
            return True
        i += 1


def add_short_term_memory(data):
    SHORT_TERM_HISTORY.append(data)


def reset_short_term_memory():
    SHORT_TERM_HISTORY.clear()


def speak(sentence, device_name='living'):
    device = MOUTH_DEVICES[device_name]
    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(device['host'], username=device['username'], password=device['password'])
    _stdin, stdout, _stdrr = client.exec_command(f'''{device['exe']} -l fr "{sentence}" | mpg123 -''')
    stdout.read()
    client.close()