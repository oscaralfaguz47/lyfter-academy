from models.transaction import Transaction

class Income(Transaction):
    FILE_NAME = "incomes_data.csv"
    FIELD_NAMES = [
            "id_income",
            "income_title",
            "amount",
            "id_category",
            "creation_date"
            ]
    
    def __init__(self, income_title, amount, id_category, id_income=None, creation_date=None):
        super().__init__(income_title, amount, id_category, id_income, creation_date)

    def to_dict(self):
        return {
            "id_income": self.id_transaction,
            "income_title": self.transaction_title,
            "amount": self.amount,
            "id_category": self.id_category,
            "creation_date": self.creation_date
        }

    @classmethod
    def from_dict(cls, row):
        return cls(
            id_income=row["id_income"],
            income_title=row["income_title"],
            amount=row["amount"],
            id_category=row["id_category"],
            creation_date=row["creation_date"]
        )