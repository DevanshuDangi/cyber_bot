import json
def dumps(obj):
    try:
        return json.dumps(obj)
    except Exception:
        return '{}'

def loads(s):
    try:
        return json.loads(s or '{}')
    except Exception:
        return {}
