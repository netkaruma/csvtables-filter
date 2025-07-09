# CSV Filter Tool

Python CLI утилита для фильтрации и агрегации CSV файлов.

## Установка
```bash
git clone https://github.com/netkaruma/csvtables-filter.git
cd csvtables-filter
pip install tabulate
```
| Флаг         | Описание                                                  | Пример                   |
|--------------|-----------------------------------------------------------|--------------------------|
| `--file`     | Путь к CSV файлу (обязательно)                            | `--file data.csv`        |
| `--where`    | Условие фильтрации                                        | `--where "age>30"`       |
| `--aggregate`| Агрегация данных (min/max/avg/sum)                        | `--aggregate "price=sum"`|
| `--output`   | Файл для вывода                                           | `--output result.csv`    |
| `--tablefmt` | Формат таблицы (grid, simple, fancy_grid, github)         | `--tablefmt github`      |

# Пример
## Просмотр файла
```bash
python csv_filter.py --file data.csv
```
## Фильтрация
```bash
python csv_filter.py --file data.csv --where "status=active"
```
## Агрегация
```bash
python csv_filter.py --file sales.csv --aggregate "amount=avg"
```
## Сохранение в файл
```bash
python csv_filter.py --file data.csv --where "score>80" --output filtered.csv
```
## Примечание: --where и --aggregate нельзя использовать одновременно
