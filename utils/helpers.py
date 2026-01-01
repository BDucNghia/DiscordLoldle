def convert_to_year(date_str):
    try:
        return int(date_str.split("-")[0])
    except Exception:
        return None

def to_string(value):
    if isinstance(value, list):
        return " | ".join(value)
    return str(value)
