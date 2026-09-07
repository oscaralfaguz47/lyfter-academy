### PERSONAL FINANCES PROJECT

## Interfaces
    # main_window.py ✅
        - Button "Add New Category" ✅
            # create_category_window.py ✅
                - Input "Category Name" ✅
                - Button "Create Category" ✅
                - Validation "Avoid creating multiple categories with the same name" ✅
                - Validation "Avoid creating categories with empty names" ✅
        - "expense_partial.py" 
            - Table "Expenses"
            - Button "Add New Expense"
                # create_expense_window.py
                    - Input "Expense title"
                    - Input "Expense Amount"
                    - Select "Category"
                    - Validation "Avoid creating expenses without category"
        - "income_partial.py"
            - Table "Incomes"
            - Button "Add New Income"
                # create_income_window.py
                    - Input "Income title"
                    - Input "Income Amount"
                    - Select "Category"
                    - Validation "Avoid creating incomes without category" 
    # gui_components.py

## Data
    - categories_data.csv -> columns: id_category, category_name and creation_date" ✅
    - incomes_data.csv -> columns: id_income, income_title, amount, id_category, creation_date"
    - expenses_data.csv -> columns: id_expense, expense_title, amount, id_category, creation_date"

## Models
    # Classes
        - category.py: variables -> id_category, category_name, creation_date. methods -> to_dict(), from_dict() ✅
        - transaction.py: variables -> id, transaction_title, amount, creation_date. abstract methods -> to_dict(), from_dict()
        - expense.py: variables -> id_expense, expense_title, expense_amount, id_category
        - income.py: variables -> id_income, income_title, income_amount, id_category
## Services
    - category_service.py -> methods: create_category(), get_all_categories() ✅
    - file_storage_service.py -> methods: save_data_to_csv(), get_data_from_csv() ✅
    - expense_service.py -> methods: create_expense(), get_all_expenses()
    - income_service.py -> create_income(), get_all_incomes()
## Utils
    - validations.py ✅

## Tests
    - test_category_services.py ✅
    - test_expense_service.py
    - test_income_services.py
    - test_file_storage.py