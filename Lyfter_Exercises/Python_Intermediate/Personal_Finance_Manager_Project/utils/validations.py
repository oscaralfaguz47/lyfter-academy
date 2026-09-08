def validate_if_input_empty(argument_to_validate, field_name):
    if not argument_to_validate.strip():
        raise ValueError(f"The {field_name} cannot be empty")

def validate_only_numeric(argument_to_validate, field_name):
    try:
        return float(argument_to_validate)
    except ValueError:
        raise ValueError (f"The {field_name} must be numeric only")
