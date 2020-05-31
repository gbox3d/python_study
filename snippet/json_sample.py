import json

jsonStr = json.dumps({"foo": 1, "bar": 2, "alpha": 3})

print(jsonStr)

_jsonObj = json.loads(jsonStr)

print(_jsonObj['foo'])

