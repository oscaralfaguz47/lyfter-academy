from models.income import Income
from services.file_storage_service import save_data_to_csv, get_data_from_csv
from services.category_service import get_all_categories

def create_income(income_title, amount, id_category):
    new_income = Income(income_title, amount, id_category)

    save_data_to_csv(new_income, Income.FILE_NAME, Income.FIELD_NAMES)
    return new_income

def get_all_incomes():
    category_names = {c.id_category: c.category_name for c in get_all_categories()}
    incomes = get_data_from_csv(Income.FILE_NAME, Income)

    for income in incomes:
        income.category_name = category_names.get(income.id_category, "Unknown")

    return incomes