from flask import request
from app.http.errors import APIError, ValidationError
from app.utils.validators import clean_str, clean_date



# ---------- BODY ----------
def get_json_body():
    if not request.is_json:
        raise APIError("Content-Type must be application/json.")
    data = request.get_json(silent=True)
    if data is None:
        raise APIError("Body is not a valid JSON.")
    if not isinstance(data, dict):
        raise ValidationError("Body must be a JSON object.")
    return data

# ---------- QUERY STRING ----------
class QueryParams:
    def __init__(self, allowed):
        self._args = request.args
        self.errors = {}
        for name in set(self._args.keys()) - set(allowed): # Here we take the arguments from the user and we compare them with the allowed ones
            self.errors[name] = "Unknown query param."

    # For params in the url, return a single and not repeated param, or None if missing
    def _raw(self, name, required):
        values = self._args.getlist(name)
        if not values:
            if required:
                self.errors[name] = "This query param is required."
            return None
        if len(values) > 1:
            self.errors[name] = f"Must be sent only once, you sent {len(values)}."
            return None
        return values[0]

    def get_str(self, name, *, required=False, default=None, **rules):
        raw = self._raw(name, required)
        if raw is None:
            return default
        value = clean_str(raw, name, self.errors, **rules)
        return default if value is None else value

    def get_int(self, name, *, required=False, default=None):
        raw = self._raw(name, required)
        if raw is None:
            return default
        try:
            value = int(raw)
        except ValueError:
            self.errors[name] = "Must be an integer."
            return default
        return value

    def get_date(self, name, *, required=False, default=None, **rules):
        raw = self._raw(name, required)
        if raw is None:
            return default
        value = clean_date(raw, name, self.errors, **rules)
        return default if value is None else value

    def get_bool(self, name, *, required=False, default=None):
        raw = self._raw(name, required)
        if raw is None:
            return default
        value = raw.strip().lower()
        if value in {"true","1"}:
            return True
        if value in {"false", "0"}:
            return False
        self.errors[name] = "Must be true or false."
        return default

    def raise_if_errors(self):
        if self.errors:
            raise ValidationError("Invalid query params.", self.errors)
