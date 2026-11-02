import json


def csv_to_records(text: str) -> list[dict]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return []

    headers = [h.strip() for h in lines[0].split(",")]
    records = []

    for line in lines[1:]:
        values = [v.strip() for v in line.split(",")]
        record = {}
        for i, header in enumerate(headers):
            record[header] = values[i] if i < len(values) else ""
        records.append(record)

    return records


def _to_typed_value(value_str: str):
    s = value_str.strip()
    lower = s.lower()

    if lower in ("true", "yes"):
        return True
    if lower in ("false", "no"):
        return False

    # ГЛАВНОЕ: если есть запятая — сразу возвращаем строку
    if "," in s:
        return s

    try:
        if "." in s:
            return float(s)
        return int(s)
    except ValueError:
        pass

    return s


def parse_settings(lines: list[str]) -> dict:
    result = {}
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]

        if "#" in line:
            line = line[:line.index("#")]

        line = line.strip()
        if not line:
            i += 1
            continue

        if ":" in line and line.rstrip().endswith(":"):
            key = line.rstrip()[:-1].strip()
            items = []
            i += 1
            while i < n:
                next_line = lines[i]
                if "#" in next_line:
                    next_line = next_line[:next_line.index("#")]
                next_line = next_line.strip()
                if next_line.startswith("- "):
                    value = next_line[2:].strip()
                    items.append(_to_typed_value(value))
                    i += 1
                else:
                    break
            result[key] = items
            continue

        if ":" in line:
            key, _, value_raw = line.partition(":")
            key = key.strip()
            value_str = value_raw.strip()
            if value_str:
                result[key] = _to_typed_value(value_str)
            else:
                result[key] = ""
            i += 1
            continue

        i += 1

    return result


def merge_by_key(rows: list[dict], extra: dict, key: str = "id") -> list[dict]:
    merged = []
    for row in rows:
        new_row = dict(row)
        lookup_value = row.get(key)

        if lookup_value is None or lookup_value not in extra:
            merged.append(new_row)
            continue

        info = extra[lookup_value]
        if not isinstance(info, dict):
            merged.append(new_row)
            continue

        for k, v in info.items():
            if k not in new_row:
                new_row[k] = v
        merged.append(new_row)
    return merged


def records_to_json(records: list[dict]) -> str:
    return json.dumps(
        records,
        ensure_ascii=False,
        indent=2,
        sort_keys=True
    )

