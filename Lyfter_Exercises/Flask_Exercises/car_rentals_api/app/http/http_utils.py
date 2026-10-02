from flask import request

from errors import APIError, ValidationError

# ---------- BODY ----------
def get__json_body():
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

    def raise_if_errors(self):
        if self.errors:
            raise ValidationError("Invalid query params.", self.errors)
