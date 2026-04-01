import json


def json_to_dict(file_path) -> list[dict[str, str]] | list[dict[str, list]]:
    with open(file_path, mode='r', encoding='utf-8') as jsonfile: 
        data = json.load(jsonfile)
        return data[list(data.keys())[0]]
