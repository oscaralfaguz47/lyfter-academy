import uuid

class TaskValidationError(ValueError):
    def __init__(self, errors):
        super().__init__("Invalid task data")
        # {"field": "message"}
        self.errors = errors

class Task:
    FIELD_NAMES = [
        "id",
        "title",
        "description",
        "status"
    ]
    def __init__(self, title, description):
        errors = {}
        if not isinstance(title, str) or not title.strip():
            errors["title"] = "The title is required."
        if not isinstance(description, str) or not description.strip():
            errors["description"] = "The description is required."
        if errors:
            raise TaskValidationError(errors)
        
        self.id = uuid.uuid4()
        self.title = title
        self.description = description
        self.status = "Pending"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status
        }