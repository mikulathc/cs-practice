from collections import Counter

def parse_event(line: str) -> dict:
    """
    Парсит одну строку журнала.
    Формат: "2026-03-01T09:03:55 ERROR Сообщение с пробелами"
    Возвращает: {"time": ..., "level": ..., "message": ...}
    Если строка неверна -> ValueError
    """
    line = line.strip()
    if not line:
        raise ValueError("Empty line")

    # Разбиваем только на первые 3 части, чтобы пробелы в сообщении не ломали парсинг
    parts = line.split(maxsplit=2)
    
    if len(parts) != 3:
        raise ValueError("Invalid format: expected 3 parts")

    time_str, level, message = parts
    
    valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR"}
    if level not in valid_levels:
        raise ValueError(f"Unknown level: {level}")

    return {"time": time_str, "level": level, "message": message}


def count_levels(lines) -> dict:
    """
    Считает количество строк каждого уровня.
    Испорченные строки считаются под ключом BROKEN.
    lines может быть списком строк или открытым файлом (итерируемым объектом).
    Пустые строки пропускаются.
    """
    counts = {"BROKEN": 0}
    valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR"}

    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        try:
            event = parse_event(line)
            level = event["level"]
            counts[level] = counts.get(level, 0) + 1
        except ValueError:
            counts["BROKEN"] = counts.get("BROKEN", 0) + 1
            
    # Гарантируем наличие всех ключей, даже если их 0 (для красивого отчёта)
    for lvl in valid_levels:
        if lvl not in counts:
            counts[lvl] = 0
            
    return counts


def top_errors(lines, n: int) -> list[list]:
    """
    Возвращает n самых частых сообщений уровня ERROR.
    Результат: список списков [["сообщение", кол-во], ...]
    При равенстве частоты — сортировка по алфавиту (возрастание).
    """
    error_messages = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        try:
            event = parse_event(line)
            if event["level"] == "ERROR":
                error_messages.append(event["message"])
        except ValueError:
            # Испорченные строки игнорируются для статистики ошибок
            continue

    if not error_messages:
        return []

    counter = Counter(error_messages)
    
    # Сортировка: сначала по частоте (убывание), потом по сообщению (алфавит, возрастание)
    sorted_errors = sorted(counter.items(), key=lambda x: (-x[1], x[0]))
    
    result = []
    for msg, count in sorted_errors[:n]:
        result.append([msg, count])
        
    return result


def format_report(counts: dict, errors: list[list]) -> str:
    """
    Формирует текст отчёта.
    Уровни выводятся по алфавиту.
    В конце обязательно перевод строки.
    """
    report_lines = ["Отчёт по журналу", ""]
    
    levels = [lvl for lvl in counts.keys() if lvl != "BROKEN"]
    levels.sort()  # По алфавиту
    
    report_lines.append(f"BROKEN: {counts.get('BROKEN', 0)}")
    
    for lvl in levels:
        report_lines.append(f"{lvl}: {counts[lvl]}")
    
    report_lines.append("")
    report_lines.append("Частые ошибки:")
    
    for msg, count in errors:
        report_lines.append(f"- {msg} — {count}")
    
    return "\n".join(report_lines) + "\n"



