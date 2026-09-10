from models.transaction import Transaction

class Expense(Transaction):
        FILE_NAME = "expenses_data.csv"
        FIELD_NAMES = [
                "id_expense",
                "expense_title",
                "amount",
                "id_category",
                "creation_date"
                ]
        
        def __init__(self, expense_title, amount, id_category, id_expense=None, creation_date=None):
                super().__init__(expense_title, amount, id_category, id_expense, creation_date)

        def to_dict(self):
                return {
                        "id_expense": self.id_transaction,
                        "expense_title": self.transaction_title,
                        "amount": self.amount,
                        "creation_date": self.creation_date,
                        "id_category": self.id_category
                        }
        @classmethod
        def from_dict(cls, row):
                return cls(
                        id_expense=row["id_expense"],
                        expense_title=row["expense_title"],
                        amount=row["amount"],
                        creation_date=row["creation_date"],
                        id_category=row["id_category"]
                )