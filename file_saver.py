import csv
import json
from dataclasses import field
from idlelib.iomenu import encoding


class FileSaver:
    @staticmethod
    def save_csv(path: str, data: list[dict]):
        field_names = data[0].keys()
        with open(f'{path}', 'w', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(data)

    @staticmethod
    def save_json(path: str, data: list[dict]):
        with open(f'{path}', 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, indent=2, ensure_ascii=False)
