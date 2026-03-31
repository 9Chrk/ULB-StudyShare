import csv
import json
import xml.etree.ElementTree as xml


def csv_to_dict(file_path) -> list[dict[str, str]]:
    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        data = csv.DictReader(csvfile)
        return [row for row in data]


def json_to_dict(file_path) -> list[dict[str, str]] | list[dict[str, list]]:
    with open(file_path, mode='r', encoding='utf-8') as jsonfile: 
        data = json.load(jsonfile)
        return data[list(data.keys())[0]]


def xml_to_dict(file_path) -> list[dict[str, str]] | list[dict[str, dict]]:
    tree = xml.parse(file_path)
    root = tree.getroot()
    data = []

    for tag in root:
        dict_ = {}
        for sub_tag in tag:
            if list(sub_tag):  # si sous-éléments
                sub_dict = {}
                for sub_sub_tag in sub_tag: # sous-sous-éléments
                    sub_dict[sub_sub_tag.tag] = {final_tag.tag: final_tag.text for final_tag in sub_sub_tag}
                dict_[sub_tag.tag] = sub_dict
            else:
                dict_[sub_tag.tag] = sub_tag.text
        data.append(dict_)

    return data
