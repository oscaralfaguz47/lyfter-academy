from datetime import datetime
import uuid
from services.file_storage_service import save_data_to_csv
from utils.validations import validate_if_string_empty

class Category:
    FILE_NAME = "categories_data.csv"
    FIELD_NAMES = [
    "id_category",
    "category_name",
    "creation_date"
    ]

    def __init__(self, category_name, id_category=None, creation_date=None):
        validate_if_string_empty(category_name, "Category Name")
        self.id_category = id_category or str(uuid.uuid4())
        self.creation_date = creation_date or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.category_name = category_name

    def to_dict(self):
        return{
            "id_category": self.id_category,
            "category_name": self.category_name,
            "creation_date": self.creation_date
        }

    @classmethod
    def from_dict(cls, row):
        return cls(
            id_category=row["id_category"],
            category_name=row["category_name"],
            creation_date=row["creation_date"]
        )
    