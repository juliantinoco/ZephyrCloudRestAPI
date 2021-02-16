from enum import Enum

import json


class Status(Enum):
    PASS = 1
    FAIL = 2
    WIP = 3
    BLOCKED = 4
    UNEXECUTED = 5


def is_json(data):
    try:
        json.loads(data)
    except ValueError:
        return False
    return True
