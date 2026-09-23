import csv
import json
import os
import shutil

from models import Computer


DATA_FOLDER = "data"
JSON_FILE = os.path.join(DATA_FOLDER, "computers.json")
CSV_FILE = os.path.join(DATA_FOLDER, "computers.csv")
BACKUP_FILE = os.path.join(DATA_FOLDER, "computers_backup.json")


def create_data_folder():
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)


def save_json(computers):
    create_data_folder()

    if os.path.exists(JSON_FILE):
        shutil.copy(JSON_FILE, BACKUP_FILE)

    data = []

    for computer in computers:
        data.append(computer.to_dict())

    with open(JSON_FILE, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4
        )


def load_json():
    create_data_folder()

    if not os.path.exists(JSON_FILE):
        return []

    try:
        with open(JSON_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        computers = []

        for item in data:
            computers.append(Computer.from_dict(item))

        return computers

    except (json.JSONDecodeError, KeyError, TypeError, ValueError):
        print("Ошибка: файл JSON содержит некорректные данные.")
        return []


def export_csv(computers):
    create_data_folder()

    with open(
        CSV_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Название",
            "Процессор",
            "RAM",
            "Накопитель",
            "Цена"
        ])

        for computer in computers:
            writer.writerow([
                computer.name,
                computer.processor,
                computer.ram,
                computer.storage,
                computer.price
            ])