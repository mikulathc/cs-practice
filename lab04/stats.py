def parse_record(line: str) -> dict:
    parts = line.split(";")
    if len(parts) != 3:
        raise ValueError("Строка должна содержать ровно три поля.")
    
    city, temp_str, date = parts
    
    if not city.strip() or not date.strip():
        raise ValueError("Город и дата не могут быть пустыми.")
    
    try:
        temp = float(temp_str)
    except ValueError:
        raise ValueError(f"Температура должна быть числом, получено: '{temp_str}'.")
    
    return {
        "city": city.strip(),
        "temp": temp,
        "date": date.strip()
    }


def read_valid(lines: list[str]) -> list[dict]:
    valid_records = []
    for line in lines:
        if not line.strip():
            continue
        try:
            record = parse_record(line)
            valid_records.append(record)
        except ValueError:
            # Пропускаем негодные строки
            pass
    return valid_records


def average_by_city(records: list[dict]) -> dict:
    totals = {}
    counts = {}
    for rec in records:
        city = rec["city"]
        temp = rec["temp"]
        totals[city] = totals.get(city, 0) + temp
        counts[city] = counts.get(city, 0) + 1
    
    averages = {}
    for city in totals:
        avg = totals[city] / counts[city]
        averages[city] = round(avg, 1)
    return averages


def warmest_city(records: list[dict]) -> str:
    if not records:
        return ""
    averages = average_by_city(records)
    sorted_cities = sorted(averages.items(), key=lambda x: (-x[1], x[0]))
    return sorted_cities[0][0]












