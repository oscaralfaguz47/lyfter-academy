import logging
logger = logging.getLogger(__name__)

from errors import ValidationError, NotFoundError
from task_model import Task, TaskValidationError
from storage_service import save_data_to_json, get_record_by_id, update_record_in_json, delete_record_from_json, get_data_from_json

def create_task(task_data):
    if not isinstance(task_data, dict):
        raise ValidationError("Body must be a JSON object.")
    
    try:
        task = Task(
            task_data.get("title"),
            task_data.get("description"),
            task_data.get("status")
        )
        save_data_to_json(task, Task.FILE_NAME)
    except TaskValidationError as error:
        raise ValidationError("Task data is invalid.", error.errors) from error
    logger.info("Task %s created", task.id)
    return task

def update_task(task_id, task_data):
    if not isinstance(task_data, dict):
        raise ValidationError("Body must be a JSON object")
    
    existing_task = get_task(task_id) # It raises a NotFoundError 404 if not exist

    try:
        task_to_update = Task(
            task_data.get("title", existing_task.title),
            task_data.get("description", existing_task.description),
            status=task_data.get("status", existing_task.status),
            id=existing_task.id,
        )

    except TaskValidationError as error:
        raise ValidationError("Task data is invalid.", error.errors) from error
    
    update_record_in_json(Task.FILE_NAME, task_to_update)
    logger.info("Task %s updated", task_to_update.id)
    return task_to_update

def get_task(task_id):
    task = get_record_by_id(Task.FILE_NAME, Task, task_id)
    if task is None:
        raise NotFoundError(f"Task {task_id} does not exist.")
    return task

def get_tasks(status=None):
    if status is not None:
        status = status.strip()
        if status not in Task.VALID_STATUSES:
            raise ValidationError("Invalid query params.",{"status":f"The provided status ({status}) is not valid, try with (Pending, In Progress or Done)"})
    
    tasks = get_data_from_json(Task.FILE_NAME, Task)
    if status is not None:
        tasks = [task for task in tasks if task.status == status]
    return tasks

def delete_task(task_id):
    existing_task = get_task(task_id) # It raises 404 Not found if the task doesn't exist
    delete_record_from_json(Task.FILE_NAME, task_id)
    return existing_task

