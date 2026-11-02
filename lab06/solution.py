def count_by_extension(paths):
    result = {}
    for path in paths:
        name = path.split("/")[-1]
        if "." in name:
            ext = name.rsplit(".", 1)[1].lower()
        else:
            ext = ""
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

