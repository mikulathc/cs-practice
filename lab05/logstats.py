def parse_event(line: str) -> dict:
    line = line.strip()
    if not line:
        raise ValueError("Empty line")

    parts = line.split(maxsplit=2)
    if len(parts) != 3:
        raise ValueError("Invalid format")

    time_str, level, message = parts
    valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR"}
    if level not in valid_levels:
        raise ValueError(f"Unknown level: {level}")

    return {"time": time_str, "level": level, "message": message}


def count_levels(lines) -> dict:
    counts = {}
    for line in lines:
        raw_line = line.rstrip("\n")
        if not raw_line.strip():
            continue

        try:
            event = parse_event(raw_line)
            level = event["level"]
        except ValueError:
            level = "BROKEN"

        counts[level] = counts.get(level, 0) + 1

    return {level: cnt for level, cnt in counts.items() if cnt > 0}


def top_errors(lines, n: int) -> list[list]:
    from collections import Counter
    error_messages = []
    for line in lines:
        raw_line = line.rstrip("\n")
        if not raw_line.strip():
            continue
        try:
            event = parse_event(raw_line)
            if event["level"] == "ERROR":
                error_messages.append(event["message"])
        except ValueError:
            pass

    counter = Counter(error_messages)
    sorted_items = sorted(counter.items(), key=lambda x: (-x[1], x[0]))
    return [[msg, count] for msg, count in sorted_items[:n]]


def format_report(counts: dict, errors: list[list]) -> str:
    lines = ["Отчёт по журналу", ""]

    for level in sorted(counts.keys()):
        lines.append(f"{level}: {counts[level]}")

    lines.append("")
    lines.append("Частые ошибки:")

    for msg, count in errors:
        lines.append(f"- {msg} — {count}")

    return "\n".join(lines) + "\n"

