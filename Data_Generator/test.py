import json

with open('jsons/2021/2021-11-20/Scrapped.json') as json_file:
    data = json.load(json_file)
    print(type(data))
    print(data)
    print(data["Header"])
    