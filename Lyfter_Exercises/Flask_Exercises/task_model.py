import uuid

class TaskValidationError(ValueError):
    def __init__(self, errors):
        super().__init__("Invalid task data")
        # {"field": "message"}
        self.errors = errors

class Task:
    FILE_NAME = "tasks_data.json"
    VALID_STATUSES = ("Pending", "In Progress", "Done")
    
    def __init__(self, title, description, status="Pending", *, id=None):
        errors = {}
        if not isinstance(title, str) or not title.strip():
            errors["title"] = "The title is required."
        if not isinstance(description, str) or not description.strip():
            errors["description"] = "The description is required."
        if not isinstance(status, str) or status.strip() not in self.VALID_STATUSES:
            errors["status"] = "The status must be (Pending, In Progress or Done) only." 

        if errors:
            raise TaskValidationError(errors)
        
        self.id = id or uuid.uuid4()
        self.title = title.strip()
        self.description = description.strip()
        self.status = status.strip()

    def to_dict(self):
        return {
            "id": str(self.id),
            "title": self.title,
            "description": self.description,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, row):
        return cls(
            id=row["id"],
            title=row["title"],
            description=row["description"],
            status=row["status"]
        )
        