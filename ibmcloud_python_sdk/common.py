import json

def printJson(data):
    print(json.dumps(json.loads(data), indent=4, sort_keys=True))
