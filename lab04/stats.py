from datetime import datetime

def parse_record(record: str):
    parts = record.split(';')
    
    # Строго 3 части
    if len(parts) != 3:
        raise ValueError("Invalid format")
    
    city = parts[0].strip()
    temp_str = parts[1].strip().replace(',', '.')
    date_str = parts[2].strip()
    
    # Защита: город не может быть пустым
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
            # Пропускаем всё, что не удалось распарсить
            continue
    return result

def average_by_city(records: list):
    sums = {}
    counts = {}
    
    for rec in records:
        # ГЛАВНОЕ: если нет правильного ключа "temperature" — пропускаем запись
        if "temperature" not in rec:
            continue
            
        city = rec["city"]
        temp = rec["temperature"]
        
        sums[city] = sums.get(city, 0) + temp
        counts[city] = counts.get(city, 0) + 1
    
    if not sums:
        return {}
        
    return {city: sums[city] / counts[city] for city in sums}

def warmest_city(records: list):
    if not records:
        return None
    
    averages

