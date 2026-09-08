from models.transaction import Transaction

class Income(Transaction):
    def __init__(self, income_title, amount, id_category):
        super().__init__(income_title, amount, id_category)
    pass