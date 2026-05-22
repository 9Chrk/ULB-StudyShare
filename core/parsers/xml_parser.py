"""Fonctions utilitaires pour parser des fichiers XML."""

import xml.etree.ElementTree as xml


def xml_to_dict(file_path: str) -> list[dict]:
    """Lit un fichier XML et retourne une liste de dictionnaires imbriqués."""
    tree = xml.parse(file_path)
    root = tree.getroot()
    data = []

    # On parcourt chaque noeud racine et on le convertit en structure Python.
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

    # Regrouper les enfants par tag pour distinguer champs simples et listes.
    children_by_tag = {}
    for child in element:
        if child.tag not in children_by_tag:
            children_by_tag[child.tag] = []
        children_by_tag[child.tag].append(child)

    # Traiter chaque groupe d'enfants
    for tag_name, elements in children_by_tag.items():
        if len(elements) == 1:
            # Un seul enfant: on le garde comme valeur scalaire ou objet imbriqué.
            child = elements[0]
            if list(child):  # Si a ses propres sous-éléments
                # On descend récursivement pour conserver toute l'arborescence.
                result[tag_name] = _parse_element(child)
            else:
                result[tag_name] = child.text
        else:
            # Plusieurs enfants identiques: on les normalise en liste Python.
            result[tag_name] = []
            for child in elements:
                if list(child):
                    # Même règle pour les listes: chaque élément peut lui-même être imbriqué.
                    result[tag_name].append(_parse_element(child))
                else:
                    result[tag_name].append(child.text)

    return result
