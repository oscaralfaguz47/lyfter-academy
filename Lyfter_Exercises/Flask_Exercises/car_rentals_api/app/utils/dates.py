from datetime import date, datetime

def parse_iso_date(value):
    if isinstance(value, datetime):
        return value.date() # Return the date only
    if isinstance(value, date):
        return value  # If already a date, return the date
    if isinstance(value, str):
        try:
            return date.fromisoformat(value.strip()) # If is a string, try to convert to date
        except ValueError:
            return None
    return None