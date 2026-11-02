def count_by_extension(paths):
    result = {}
    for path in paths:
        name = path.split("/")[-1]

        last_dot = name.rfind(".")

        if last_dot == -1:
            # Точки вообще нет
            ext = ""
        elif last_dot == 0:
            # Файл начинается с точки и других точек нет (.gitignore)
            ext = ""
        else:
            # Есть точка не в начале — берём часть после последней точки
            ext = name[last_dot + 1:].lower()

        result[ext] = result.get(ext, 0) + 1

    return result



def deepest_path(paths):
    if not paths:
        return ""

    def depth(p):
        return p.count("/")

    best_path = paths[0]
    best_depth = depth(best_path)

    for p in paths[1:]:
        d = depth(p)
        if d > best_depth:
            best_depth = d
            best_path = p
        elif d == best_depth and p < best_path:
            best_path = p

    return best_path

def human_size(n_bytes):
    units = ["Б", "КБ", "МБ", "ГБ", "ТБ"]
    size = n_bytes
    unit_index = 0

    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1

    unit = units[unit_index]
    if unit == "Б":
        return f"{int(size)} {unit}"
    else:
        return f"{size:.1f} {unit}"

