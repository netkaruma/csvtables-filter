import re
from typing import Tuple, Optional


class Validator:
    @staticmethod
    def validate_aggregate_condition(condition: str) -> Tuple[str, str]:
        """Проверяет корректность условия агрегации"""
        match = re.fullmatch(r"^([a-zA-Z_]\w*)=(min|max|avg|sum)$", condition)
        if not match:
            raise ValueError(f"Некорректный формат условия агрегации: {condition}")
        return match.groups()

    @staticmethod
    def validate_filter_condition(condition: str) -> Tuple[str, str, str]:
        """Проверяет корректность условия фильтрации"""
        match = re.fullmatch(r"^([a-zA-Z_]\w*)([=><])(.+)$", condition)
        if not match:
            raise ValueError(f"Некорректный формат условия фильтрации: {condition}")
        return match.groups()

    @staticmethod
    def parse_value(value: str):
        """Парсит строковое значение в число если возможно"""
        try:
            return float(value) if '.' in value else int(value)
        except ValueError:
            return value