import json

with open("info.json") as f:
    data = json.load(f)
config = {
    'units': data
}
#print(config)
