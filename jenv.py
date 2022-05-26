import json


def getenv(key):
    try:
        file = open("jenv.json", "r")
        data = json.load(file)
        return data[key]
    except (json.JSONDecodeError, KeyError, FileNotFoundError):
        return None
