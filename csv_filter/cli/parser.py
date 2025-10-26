import argparse


class CLIParser:
    @staticmethod
    def create_parser():
        """Создает парсер аргументов командной строки"""
        parser = argparse.ArgumentParser(description='Фильтрация CSV файлов')
        parser.add_argument('--file', required=True, help='Путь к CSV файлу')
        parser.add_argument('--where', help='Условие фильтрации (формат: "поле=значение")')
        parser.add_argument('--aggregate', help='Условие агрегации (формат: "поле=оператор")')
        parser.add_argument('--output', help='Файл для вывода результатов')
        parser.add_argument('--tablefmt', default='grid', 
                           help='Формат таблицы (grid, simple, fancy_grid, github и др.)')
        return parser

    @staticmethod
    def validate_args(args):
        """Проверяет корректность аргументов"""
        if args.where and args.aggregate:
            raise ValueError("Нельзя использовать --where и --aggregate одновременно")