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


def xml_to_dict(file_path) -> list[dict]:
    tree = xml.parse(file_path)
    root = tree.getroot()
    data = []

    for element in root:
        data.append(_parse_element(element))

    return data


# ---------- FONCTION AUXILIAIRE POUR XML ---------
# ⚠️ ATTENTION : CETTE SECTION EST GÉNÉRÉ PAR IA

def _parse_element(element) -> dict:
    """Fonction auxiliaire pour parser un élément XML récursivement"""
    result = {}
    
    # Capturer les attributs
    if element.attrib:
        result.update(element.attrib)
    
    # Grouper les enfants par tag pour détecter les listes
    children_by_tag = {}
    for child in element:
        if child.tag not in children_by_tag:
            children_by_tag[child.tag] = []
        children_by_tag[child.tag].append(child)
    
    # Traiter chaque groupe d'enfants
    for tag_name, elements in children_by_tag.items():
        if len(elements) == 1:
            # Un seul élément
            child = elements[0]
            if list(child):  # Si a ses propres sous-éléments
                result[tag_name] = _parse_element(child)
            else:
                result[tag_name] = child.text
        else:
            # Plusieurs éléments avec le même tag = liste
            result[tag_name] = []
            for child in elements:
                if list(child):
                    result[tag_name].append(_parse_element(child))
                else:
                    result[tag_name].append(child.text)
    
    return result
