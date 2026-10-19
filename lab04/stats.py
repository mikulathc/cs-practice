from datetime import datetime

def parse_record(record: str):
    parts = record.split(';')
    
    # Должно быть ровно 3 части
    if len(parts) != 3:
        raise ValueError("Invalid format")
    
    city = parts[0].strip()
    temp_str = parts[1].strip().replace(',', '.')
    date_str = parts[2].strip()
    
    # Город не может быть пустым (защита от ";24.5;...")
    if not city:
        raise ValueError("City cannot be empty")
    
    try:
        temperature = float(temp_str)
    except ValueError:
        raise ValueError("Invalid temperature")
    
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Invalid date")
    
    return {"city": city, "temperature": temperature, "date": date_str}

def read_valid(records: list):
    result = []
    for r in records:
        try:
            result.append(parse_record(r))
        except Exception:
            # Любые ошибки (неверный формат, пустая строка и т.п.) — просто пропускаем
            continue
    return result

def average_by_city(records: list):
    sums = {}
    counts = {}
    
    for rec in records:
        city = rec["city"]
        temp = rec["temperature"]
        
        sums[city] = sums.get(city, 0) + temp
        counts[city] = counts.get(city, 0) + 1
    
    return {city: sums[city] / counts[city] for city in sums}

def warmest_city(records: list):
    if not records:
        return None
    
    averages = average_by_city(records)
    if not averages:
        return None
    
    # x[1] — температура, [0] — название города
    return max(averages.items(), key=lambda x: x[1])[0]
