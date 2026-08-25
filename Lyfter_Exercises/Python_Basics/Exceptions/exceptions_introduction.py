class InsufficientFundsError(Exception):
    def __init__(self, balance, amount):
        super().__init__(f"Insufficient funds: You tried withdraw: {amount} but you have available: {balance}")

try:
    balance = 100
    amount_to_withdraw = 150
    if amount_to_withdraw > balance:
        raise InsufficientFundsError(balance, amount_to_withdraw)
except InsufficientFundsError as e:
    print(f"Detected error: {e}")