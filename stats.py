from datetime import datetime

def parse_record(record: str):
    parts = record.split(';')
    if len(parts) != 3:
        raise ValueError("Invalid format")
    
    city = parts.strip()
    temp_str = parts.strip().replace(',', '.')
    date_str = parts.strip()
    
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
    result = 
    for r in records:
        try:
            result.append(parse_record(r))
        except (ValueError, IndexError):
            continue
    return result


