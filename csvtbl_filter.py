import argparse
import csv
import re
from typing import List, Optional
from tabulate import tabulate


class CSV_Filter:
    def __init__(self, headers: List[str], data: List[List[str]]):
        if not headers:
            raise ValueError("Заголовки не могут быть пустыми")
        if not data:
            raise ValueError("Данные не могут быть пустыми")
            
        self.headers = headers
        self.data = data

    def search_number_header(self, head_item: str) -> Optional[int]:
        """Возвращает индекс заголовка или None если не найден"""
        try:
            return self.headers.index(head_item)
        except ValueError:
            return None
    
    def aggregate_by(self, condition: str) -> float:
        """Агрегирует данные по условию"""
        match = re.fullmatch(r"^([a-zA-Z]+)=(min|max|avg|sum)$", condition)
        if not match:
            raise ValueError(f"Некорректный формат условия: {condition}")
            
        header_name, operation = match.groups()
        col_index = self.search_number_header(header_name)
        
        if col_index is None:
            raise ValueError(f"Заголовок '{header_name}' не найден")

        values = []
        for row in self.data:
            if col_index >= len(row):
                continue
                
            try:
                cell_value = row[col_index]
                num_value = float(cell_value) if '.' in cell_value else int(cell_value)
                values.append(num_value)
            except (ValueError, TypeError):
                continue
                
        if not values:
            raise ValueError("Нет числовых данных для агрегации")

        if operation == "min":
            return min(values)
        elif operation == "max":
            return max(values)
        elif operation == "avg":
            return sum(values) / len(values)
        elif operation == "sum":
            return sum(values)
                    
    def filter_by_condition(self, condition: str) -> List[List[str]]:
        """Фильтрует данные по условию"""
        match = re.fullmatch(r"^([a-zA-Z]+)([=><])(.+)$", condition)
        if not match:
            raise ValueError(f"Некорректный формат условия: {condition}")

        header_name, operator, value = match.groups()
        col_index = self.search_number_header(header_name)
        
        if col_index is None:
            raise ValueError(f"Заголовок '{header_name}' не найден")

        # Определяем тип значения
        try:
            value = float(value) if '.' in value else int(value)
            is_numeric = True
        except ValueError:
            is_numeric = False

        result = []
        for row in self.data:
            if col_index >= len(row):
                continue

            cell_value = row[col_index]
            
            try:
                if is_numeric:
                    cell_num = float(cell_value) if '.' in cell_value else int(cell_value)
                    
                    if operator == ">" and cell_num > value:
                        result.append(row)
                    elif operator == "<" and cell_num < value:
                        result.append(row)
                    elif operator == "=" and cell_num == value:
                        result.append(row)
                else:
                    if operator == "=" and cell_value == value:
                        result.append(row)
            except (ValueError, TypeError):
                continue

        return result


def main():
    parser = argparse.ArgumentParser(description='Фильтрация CSV файлов')
    parser.add_argument('--file', required=True, help='Путь к CSV файлу')
    parser.add_argument('--where', help='Условие фильтрации (формат: "поле=значение")')
    parser.add_argument('--aggregate', help='Условие агрегации (формат: "поле=оператор")')
    parser.add_argument('--output', help='Файл для вывода результатов')
    parser.add_argument('--tablefmt', default='grid', 
                       help='Формат таблицы (grid, simple, fancy_grid, github и др.)')

    args = parser.parse_args()

    if args.where and args.aggregate:
        print("Ошибка: нельзя использовать --where и --aggregate одновременно")
        return

    try:
        with open(args.file, 'r', encoding='UTF-8') as file:
            reader = list(csv.reader(file))
            if not reader:
                print("Файл пуст")
                return

            headers, data = reader[0], reader[1:]
            obj_CSV = CSV_Filter(headers, data)
            output_content = ""

            if args.where:
                filtered = obj_CSV.filter_by_condition(args.where)
                if filtered:
                    output_content = tabulate(
                        filtered, 
                        headers=obj_CSV.headers, 
                        tablefmt=args.tablefmt
                    )
                    output_content = "Результаты фильтрации:\n" + output_content
                else:
                    output_content = "Нет данных, соответствующих условию"
            
            elif args.aggregate:
                try:
                    aggregated = obj_CSV.aggregate_by(args.aggregate)
                    output_content = f"Результаты агрегации: {aggregated}"
                except ValueError as e:
                    output_content = f"Ошибка агрегации: {e}"
            
            else:
                output_content = tabulate(
                    obj_CSV.data, 
                    headers=obj_CSV.headers, 
                    tablefmt=args.tablefmt
                )

            # Вывод результатов
            if args.output:
                with open(args.output, 'w', encoding='UTF-8', newline='') as out_file:
                    if args.where and not args.aggregate:
                        writer = csv.writer(out_file)
                        writer.writerow(obj_CSV.headers)
                        writer.writerows(obj_CSV.filter_by_condition(args.where))
                    elif not args.where and not args.aggregate:
                        writer = csv.writer(out_file)
                        writer.writerow(obj_CSV.headers)
                        writer.writerows(obj_CSV.data)
                    else:
                        out_file.write(output_content)
                print(f"Данные сохранены в {args.output}")
            else:
                print(output_content)

    except FileNotFoundError:
        print(f"Файл {args.file} не найден")
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()