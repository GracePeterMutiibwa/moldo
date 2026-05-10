def to_int(value):
    return int(float(str(value).strip()))

def to_float(value):
    return float(str(value).strip())

def to_str(value):
    return str(value)

def to_bool(value):
    if isinstance(value, str):
        return value.strip().lower() not in ("", "0", "false", "no")
    return bool(value)
