from abc import ABC, abstractmethod
from datetime import datetime
import uuid
from utils.validations import validate_if_input_empty, validate_only_numeric

class Transaction(ABC):
    def __init__(self, transaction_title, amount, id_category, id_transaction=None, creation_date=None):
        validate_if_input_empty(transaction_title, "Title")
        validate_if_input_empty(amount, "Amount")
        validate_only_numeric(amount, "Amount")
        validate_if_input_empty(id_category, "Category")
        self.id_transaction = id_transaction or str(uuid.uuid4())
        self.creation_date = creation_date or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transaction_title = transaction_title
        self.amount = amount
        self.id_category = id_category

    @abstractmethod
    def to_dict(self):
       pass

    @classmethod
    @abstractmethod
    def from_dict(cls, row):
        pass