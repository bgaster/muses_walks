import json


def load_JSON(path: str):
    """Load a JSON file, in UFT-8-SIG, and return its dict representation"""
    with open(path, "r", encoding='utf-8-sig') as read_file:
        data = json.load(read_file)
    return data