from abc import ABC

class BankAccount(ABC):
    def __init__(self, balance):
        self.balance = balance

    def add_money(self, amount_to_add):
        self.balance += amount_to_add
        print(f"You added: {amount_to_add}, now you have: {self.balance}")

    def withdraw_money(self, amount_to_withdraw):
        if self.balance < amount_to_withdraw:
            raise ValueError(f"The balance is {self.balance} and you are trying to withdraw: {amount_to_withdraw}")
        self.balance -= amount_to_withdraw
        print(f"You withdrew: {amount_to_withdraw}, now you have a balance of: {self.balance}")

class SavingsAccount(BankAccount):
    def __init__(self, balance, min_balance):
        super().__init__(balance) 
        self.min_balance = min_balance

    def withdraw_money(self, amount_to_withdraw):
        if self.balance - amount_to_withdraw < self.min_balance:
            raise ValueError(f"This withdrawal would leave the balance below the minimum of {self.min_balance}")
        return super().withdraw_money(amount_to_withdraw)


saving_account1 = SavingsAccount(500, 100)
for amount in [50, 300, 100, 20]:
    try:
        saving_account1.withdraw_money(amount)
    except ValueError as e:
        print(e)
saving_account1.add_money(1000)