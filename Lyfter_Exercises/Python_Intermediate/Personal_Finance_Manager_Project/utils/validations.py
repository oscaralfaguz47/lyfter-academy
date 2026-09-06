def validate_if_string_empty(argument_to_validate, field_name):
    if not argument_to_validate.strip():
        raise ValueError(f"The {field_name} cannot be empty")