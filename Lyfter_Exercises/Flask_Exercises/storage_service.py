import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

def _get_path(file_name, data_dir):
    return Path(data_dir or DATA_DIR) / file_name

def _read_records(file_path):
    if not file_path.exists() or file_path.stat().st_size == 0:
        return []
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file) # Here we return a JSON document

def _write_records(file_path, records):
    file_path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = file_path.with_suffix(".tmp")
    with open(temp_path, "w", encoding="utf-8") as file:
        json.dump(records, file, ensure_ascii=False, indent=2)
    temp_path.replace(file_path)

def save_data_to_json(record, file_name, data_dir=None):
    file_path = _get_path(file_name, data_dir)
    records = _read_records(file_path)
    records.append(record.to_dict())
    _write_records(file_path, records)

def get_data_from_json(file_name, model_class, data_dir=None):
    file_path = _get_path(file_name, data_dir)
    return [model_class.from_dict(item) for item in _read_records(file_path)]


def get_record_by_id(file_name, model_class, record_id, data_dir=None):
    file_path = _get_path(file_name, data_dir)
    for item in _read_records(file_path):
        if item["id"] == str(record_id):
            return model_class.from_dict(item)
    return None


def update_record_in_json(file_name, updated_record, data_dir=None):
    file_path = _get_path(file_name, data_dir)
    records = _read_records(file_path)
    record_id_to_update = str(updated_record.id)

    for index, item in enumerate(records):
        if item["id"] == record_id_to_update:
            records[index] = updated_record.to_dict()  # We replace the the item in the file
            _write_records(file_path, records)
            return True
    return False

def delete_record_from_json(file_name, record_id, data_dir=None):
    file_path = _get_path(file_name, data_dir)
    records = _read_records(file_path)
    remaining = [item for item in records if item["id"] != str(record_id)]
    if len(remaining) == len(records):
        return False
    _write_records(file_path, remaining)
    return True

