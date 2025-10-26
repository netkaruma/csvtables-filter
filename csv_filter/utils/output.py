import csv
from typing import List
from tabulate import tabulate


class OutputHandler:
    @staticmethod
    def to_table(data: List[List[str]], headers: List[str], tablefmt: str = 'grid') -> str:
        """Форматирует данные в таблицу"""
        return tabulate(data, headers=headers, tablefmt=tablefmt)

    @staticmethod
    def to_csv(data: List[List[str]], headers: List[str], filename: str):
        """Сохраняет данные в CSV файл"""
        with open(filename, 'w', encoding='UTF-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(data)

    @staticmethod
    def write_output(content: str, filename: str = None):
        """Записывает вывод в файл или консоль"""
        if filename:
            with open(filename, 'w', encoding='UTF-8') as file:
                file.write(content)
            print(f"Данные сохранены в {filename}")
        else:
            print(content)