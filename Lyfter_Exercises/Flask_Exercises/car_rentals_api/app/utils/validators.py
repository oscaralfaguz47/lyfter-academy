from datetime import date, datetime
import re

_DATE_PATTERN = re.compile(r"\d{4}-\d{2}-\d{2}", re.ASCII)

def check_str(value, *, min_length=1, max_length=100, pattern=None, multiline=False):
    text = value.replace("\r\n", "\n").replace("\n", "") if multiline else value
    if not text.isprintable():
        return "Contains invalid characters."
    if len(value) < min_length:
        return f"Must have at least {min_length} characters."
    if len(value) > max_length:
        return f"Must have at most {max_length} characters."
    if pattern is not None and not re.fullmatch(pattern, value):
        return "Has an invalid format."
    return None

def clean_str(value, name, errors, *, required=True, strip=True, **rules):
    if value is None:
        if required:
            errors[name] = "This field is required."
        return None
    if not isinstance(value, str):
        errors[name] = "Must be a string."
        return None
    if strip:
        value = value.strip()
    error = check_str(value, **rules)
    if error:
        errors[name] = error
        return None
    return value

def clean_date(value, name, errors, *, required=True, min_date=None, max_date=None):
    if value is None:
        if required:
            errors[value] = "This field is required."
        return None

    if isinstance(value, date) and not isinstance(value, datetime):
        parsed = value # Is already a date
    elif isinstance(value, str) and _DATE_PATTERN.fullmatch(value.strip()):
        try:
            parsed = date.fromisoformat(value.strip())
        except ValueError: # Impossible date
            errors[name] = "Is not a valid date."
            return None
    else:
        errors[name] = "Must be a date in YYYY-MM-DD format."
        return None

    if min_date is not None and parsed < min_date:
        errors[name] = f"Must be on or after {min_date.isoformat()}."
    elif max_date is not None and parsed > max_date:
        errors[name] = f"Must be on or before {max_date.isoformat()}."
    else:
        return parsed
    return None

def clean_bool(value, name, errors, *, required=True, default=None):
    if value is None:
        if required:
            errors[name] = "This field is required."
        return default
    if not isinstance(value, bool):
        errors[name]= "Must be true or false."
        return default
    return value

def clean_int(value, name, errors, *, required=True, min_value=None, max_value=None):
    if value is None:
        if required:
            errors[name] = "This field is required."
        return None
    if isinstance(value, bool) or not isinstance(value, int):
        errors[name] = "Must be an integer."
        return None
    if min_value is not None and value < min_value:
        errors[name] = f"Must be at least {min_value}."
        return None
    if max_value is not None and value > max_value:
        errors[name] = f"Must be at most {max_value}."
        return None
    return value