""" Turn Pydantic validation errors into our domain Validation Error """

from typing import Any

import pydantic

from app.errors.exceptions import ValidationError


# parse[SchemaT: pydantic.BaseModel]: it means "whatever schema class we pass in, we get an instance of that same class back"
def parse[SchemaT: pydantic.BaseModel](schema: type[SchemaT], data: Any) -> SchemaT:
    """ Validate data against schema, or raise ValidationError with every problem found """
    try:
        return schema.model_validate(data)
    except pydantic.ValidationError as error:
        errors: dict[str, list[str]] = {}
        for problem in error.errors():
            field = ".".join(str(part) for part in problem["loc"]) or "body"
            errors.setdefault(field, []).append(problem["msg"])
        raise ValidationError("The request body has invalid fields.", details=errors) from error