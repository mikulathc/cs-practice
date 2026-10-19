import sys
from logstats import count_levels, top_errors, format_report

def main():
    # Читаем имя файла из первой строки ввода (stdin)
    input_data = sys.stdin.read().strip()
    if not input_data:
        return
    
    filename = input_data.splitlines()[0].strip()
    
    total_lines = 0
    error_count = 0
    broken_count = 0
    
    # ПЕРВЫЙ ПРОХОД: считаем статистику для вывода в консоль (всего, ERROR, BROKEN)
    with open(filename, encoding="utf-8") as log:
        for line in log:
            total_lines += 1
            line = line.strip()
            if not line:
                continue
            
            try:
                # Пытаемся распарсить, чтобы понять, валидна ли строка
                from logstats import parse_event
                parse_event(line)
                
                # Если успешно, проверяем уровень вручную (чтобы не парсить дважды)
                parts = line.split(maxsplit=2)
                if len(parts) == 3 and parts[1] == "ERROR":
                    error_count += 1
            except ValueError:
                broken_count += 1

    print(total_lines)
    print(error_count)
    print(broken_count)

    # ВТОРОЙ ПРОХОД: собираем данные для отчёта
    with open(filename, encoding="utf-8") as log:
        counts = count_levels(log)
        
    # ТРЕТИЙ ПРОХОД: топ ошибок
    with open(filename, encoding="utf-8") as log:
        errors = top_errors(log, n=5)  # n=5 — стандартный топ; можно поменять на 3, если тесты требуют
    
    report_text = format_report(counts, errors)
    
    # Записываем отчёт в report.txt рядом с собой
    with open("report.txt", "w", encoding="utf-8") as f:
        f.write(report_text)

if __name__ == "__main__":
    main()

