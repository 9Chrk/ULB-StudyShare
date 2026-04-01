import csv


def csv_to_dict(file_path) -> list[dict[str, str]]:
    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        data = csv.DictReader(csvfile)
        return [row for row in data]
