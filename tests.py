import pytest
from csvtbl_filter import CSV_Filter, main
import csv
from unittest.mock import patch, mock_open


# Тестовые данные для мока файла
def load_test_data_mock():
    """Загружает тестовые данные из tables.csv и возвращает в формате для mock_open"""
    with open('tables.csv', 'r', encoding='utf-8') as f:
        # Читаем все строки файла
        lines = f.readlines()
    # Объединяем строки в одну строку с переносами
    return ''.join(lines)

# Загружаем данные в нужном формате
TEST_DATA = load_test_data_mock()

def load_test_data():
    """Загружает тестовые данные из tables.csv"""
    with open('tables.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        data = list(reader)
    return data[0], data[1:]  # headers, rows

@pytest.fixture
def csv_data():
    """Фикстура с данными из CSV файла"""
    headers, data = load_test_data()
    return CSV_Filter(headers, data)

# Тесты для CSV_Filter
def test_search_number_header(csv_data):
    assert csv_data.search_number_header("name") == 0
    assert csv_data.search_number_header("brand") == 1
    assert csv_data.search_number_header("price") == 2
    assert csv_data.search_number_header("rating") == 3
    assert csv_data.search_number_header("nonexistent") is None

def test_filter_by_condition_string_eq(csv_data):
    result = csv_data.filter_by_condition("brand=apple")
    assert len(result) == 4
    assert all(row[1] == "apple" for row in result)

def test_filter_by_condition_numeric_gt(csv_data):
    result = csv_data.filter_by_condition("price>500")
    assert len(result) == 5
    assert all(float(row[2]) > 500 for row in result)

def test_filter_by_condition_numeric_lt(csv_data):
    result = csv_data.filter_by_condition("rating<4.5")
    assert len(result) == 4
    assert all(float(row[3]) < 4.5 for row in result)

def test_aggregate_min(csv_data):
    assert csv_data.aggregate_by("price=min") == 149

def test_aggregate_max(csv_data):
    assert csv_data.aggregate_by("price=max") == 1199

def test_aggregate_avg(csv_data):
    avg = csv_data.aggregate_by("price=avg")
    assert pytest.approx(avg, 0.01) == 602.1

def test_aggregate_sum(csv_data):
    assert csv_data.aggregate_by("price=sum") == 6020

def test_invalid_condition(csv_data):
    with pytest.raises(ValueError):
        csv_data.filter_by_condition("invalid>condition")

def test_aggregate_non_existent_column(csv_data):
    with pytest.raises(ValueError):
        csv_data.aggregate_by("nonexistent=avg")

def test_empty_filter_results(csv_data):
    result = csv_data.filter_by_condition("brand=nokia")
    assert len(result) == 0

# Тесты для main()
def test_main_with_where_condition(capsys):
    test_args = [
        "script.py",
        "--file", "dummy.csv",
        "--where", "brand=apple",
        "--tablefmt", "grid"
    ]
    
    with patch('sys.argv', test_args), \
         patch('builtins.open', mock_open(read_data=TEST_DATA)):
        main()
    
    captured = capsys.readouterr()
    assert "iphone 15 pro" in captured.out
    assert "apple" in captured.out
    assert "samsung" not in captured.out

def test_main_with_aggregate(capsys):
    test_args = [
        "script.py",
        "--file", "dummy.csv",
        "--aggregate", "price=sum"
    ]
    
    with patch('sys.argv', test_args), \
         patch('builtins.open', mock_open(read_data=TEST_DATA)):
        main()
    
    captured = capsys.readouterr()
    assert "Результаты агрегации" in captured.out
    assert "6020" in captured.out  # Сумма всех цен из TEST_DATA

def test_main_with_output_file():
    """Тест вывода в файл через --output"""
    test_args = [
        "script.py",
        "--file", "dummy.csv",
        "--output", "output.csv"
    ]
    
    # Мокаем открытие файлов
    m = mock_open(read_data=TEST_DATA)
    with patch('sys.argv', test_args), \
         patch('builtins.open', m) as mock_file, \
         patch('csv.writer') as mock_writer:
        main()
    
    # Проверяем, что файл output.csv был открыт для записи
    mock_file.assert_any_call('output.csv', 'w', encoding='UTF-8', newline='')
    
    # Проверяем, что writer был вызван с правильными данными
    assert mock_writer.call_count == 1

def test_main_file_not_found(capsys):
    test_args = [
        "script.py",
        "--file", "nonexistent.csv"
    ]
    
    with patch('sys.argv', test_args), \
         patch('builtins.open', side_effect=FileNotFoundError):
        main()
    
    captured = capsys.readouterr()
    assert "не найден" in captured.out

def test_main_invalid_args(capsys):
    """Тест обработки невалидных аргументов"""
    test_args = [
        "script.py",
        "--file", "dummy.csv",
        "--where", "brand=apple",
        "--aggregate", "price=sum"
    ]
    
    with patch('sys.argv', test_args), \
         patch('builtins.open', mock_open(read_data=TEST_DATA)):
        main()
    
    captured = capsys.readouterr()
    # Проверяем часть сообщения без учета регистра и точного совпадения
    assert "нельзя использовать" in captured.out.lower()
def test_main_empty_file(capsys):
    test_args = [
        "script.py",
        "--file", "empty.csv"
    ]
    
    with patch('sys.argv', test_args), \
         patch('builtins.open', mock_open(read_data="")):
        main()
    
    captured = capsys.readouterr()
    assert "Файл пуст" in captured.out