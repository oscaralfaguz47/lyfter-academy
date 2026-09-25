from errors import ValidationError
from task_model import Task, TaskValidationError
from storage_service import save_data_to_csv

def create_task(task_data):
    if not isinstance(task_data, dict):
        raise ValidationError("Body must be a JSON object.")
    try:
        task = Task(
            task_data.get("title"),
            task_data.get("description")
        )
        save_data_to_csv(task, "tasks_data.csv", task.FIELD_NAMES)
    except TaskValidationError as error:
        raise ValidationError("Task data is invalid.", error.errors) from error
    return task