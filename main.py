import sys
from csv_filter import *



def read_csv_file(filepath: str):
    """Читает CSV файл и возвращает заголовки и данные"""
    import csv
    
    with open(filepath, 'r', encoding='UTF-8') as file:
        reader = list(csv.reader(file))
        if not reader:
            raise ValueError("Файл пуст")
        return reader[0], reader[1:]


def main():
    parser = CLIParser.create_parser()
    args = parser.parse_args()

    try:
        CLIParser.validate_args(args)
        
        # Чтение данных
        headers, data = read_csv_file(args.file)
        csv_filter = CSV_Filter(headers, data)

        # Обработка команд
        if args.where:
            filtered_data = csv_filter.filter_by_condition(args.where)
            if filtered_data:
                output_content = OutputHandler.to_table(
                    filtered_data, headers, args.tablefmt
                )
                output_content = "Результаты фильтрации:\n" + output_content
            else:
                output_content = "Нет данных, соответствующих условию"

        elif args.aggregate:
            try:
                result = csv_filter.aggregate_by(args.aggregate)
                output_content = f"Результаты агрегации: {result}"
            except ValueError as e:
                output_content = f"Ошибка агрегации: {e}"

        else:
            output_content = OutputHandler.to_table(data, headers, args.tablefmt)

        # Вывод результатов
        if args.output:
            if args.where and filtered_data:
                OutputHandler.to_csv(filtered_data, headers, args.output)
            elif not args.where and not args.aggregate:
                OutputHandler.to_csv(data, headers, args.output)
            else:
                OutputHandler.write_output(output_content, args.output)
        else:
            OutputHandler.write_output(output_content)

    except FileNotFoundError:
        print(f"Файл {args.file} не найден")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()