import os
import time
import xml.etree.ElementTree as ET
import csv
from collections import Counter, defaultdict

class Address:
    """
    Класс для хранения информации о здании.
    """
    def __init__(self, city, floors):
        self.city = city
        self.floors = floors

def process_xml_file(file_path):
    """
    Обрабатывает XML-файл, извлекает информацию о зданиях и вызывает функцию для анализа данных.

    :param file_path: путь до XML-файла
    """
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        addresses = [
            Address(item.get('city', '').strip(), int(item.get('floor', '0').strip()))
            for item in root.findall('item')
        ]
        display_statistics(addresses)
    except Exception as e:
        print(f"Ошибка при обработке XML файла: {e}")

def process_csv_file(file_path):
    """
    Обрабатывает CSV-файл, извлекает информацию о зданиях и вызывает функцию для анализа данных.

    :param file_path: путь до CSV-файла
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Пропустить заголовок
            addresses = [
                Address(row[0].strip(), int(row[1].strip()))
                for row in reader
            ]
        display_statistics(addresses)
    except Exception as e:
        print(f"Ошибка при обработке CSV файла: {e}")

def display_statistics(addresses):
    """
    Выводит статистику по зданиям: дублирующиеся записи и количество зданий по этажам для каждого города.

    :param addresses: список объектов Address
    """
    # Поиск дубликатов
    address_counter = Counter((a.city, a.floors) for a in addresses)
    duplicates = {key: count for key, count in address_counter.items() if count > 1}

    print("Дублирующиеся записи:")
    for (city, floors), count in duplicates.items():
        print(f"{city}, {floors} этажей - {count} раз")

    # Статистика по этажам
    city_stats = defaultdict(lambda: Counter())
    for address in addresses:
        city_stats[address.city][address.floors] += 1

    print("Количество зданий по этажам в каждом городе:")
    for city, stats in city_stats.items():
        print(city)
        for floors, count in stats.items():
            print(f"{floors} этажей: {count}")

def main():
    """
    Основная функция программы. Ждёт ввода пути к файлу, определяет его формат и вызывает соответствующую функцию обработки.
    """
    while True:
        input_path = input("Введите путь до файла-справочника или 'exit' для завершения работы: ").strip()

        if input_path.lower() == "exit":
            break

        if os.path.exists(input_path):
            start_time = time.time()

            if input_path.endswith(".xml"):
                process_xml_file(input_path)
            elif input_path.endswith(".csv"):
                process_csv_file(input_path)
            else:
                print("Неподдерживаемый формат файла.")

            elapsed_time = time.time() - start_time
            print(f"Время обработки файла: {elapsed_time:.2f} секунд")
        else:
            print("Файл не найден.")

if __name__ == "__main__":
    main()
