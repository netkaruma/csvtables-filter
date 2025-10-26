from typing import List, Optional
from .validator import Validator


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
        header_name, operation = Validator.validate_aggregate_condition(condition)
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
        header_name, operator, value = Validator.validate_filter_condition(condition)
        col_index = self.search_number_header(header_name)
        
        if col_index is None:
            raise ValueError(f"Заголовок '{header_name}' не найден")

        parsed_value = Validator.parse_value(value)
        is_numeric = isinstance(parsed_value, (int, float))

        result = []
        for row in self.data:
            if col_index >= len(row):
                continue

            cell_value = row[col_index]
            
            try:
                if is_numeric:
                    cell_num = Validator.parse_value(cell_value)
                    if not isinstance(cell_num, (int, float)):
                        continue
                    
                    if operator == ">" and cell_num > parsed_value:
                        result.append(row)
                    elif operator == "<" and cell_num < parsed_value:
                        result.append(row)
                    elif operator == "=" and cell_num == parsed_value:
                        result.append(row)
                else:
                    if operator == "=" and cell_value == parsed_value:
                        result.append(row)
            except (ValueError, TypeError):
                continue

        return result