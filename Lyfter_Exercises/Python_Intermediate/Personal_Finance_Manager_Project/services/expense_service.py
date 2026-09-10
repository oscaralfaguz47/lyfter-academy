from models.expense import Expense
from services.file_storage_service import save_data_to_csv, get_data_from_csv
from services.category_service import get_all_categories

def create_expense(expense_title, amount, id_category):
    new_expense = Expense(expense_title, amount, id_category)

    save_data_to_csv(new_expense, Expense.FILE_NAME, Expense.FIELD_NAMES)
    return new_expense

def get_all_expenses():
    category_names = {c.id_category: c.category_name for c in get_all_categories()}
    expenses = get_data_from_csv(Expense.FILE_NAME, Expense)

    for expense in expenses:
        expense.category_name = category_names.get(expense.id_category, "Unknown")

    return expenses