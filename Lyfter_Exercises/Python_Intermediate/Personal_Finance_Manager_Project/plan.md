### PERSONAL FINANCES PROJECT

## Interfaces
    # main_window.py
        - Button "Add New Category"
            # create_category_window.py
                - Input "Category Name"
                - Button "Create Category"
                - Validation "Avoid creating multiple categories with the same name"
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

## Data
    - categories_data.CSV -> columns: id_category, category_name and creation_date"
    - incomes_data.CSV -> columns: id_income, income_title, amount, id_category, creation_date"
    - expenses_data.CSV -> columns: id_expense, expense_title, amount, id_category, creation_date"

## Models
    # Classes
        - Category: variables -> id_category, category_name. methods -> display_categories(), create_category() 
        - Transaction: variables -> id, transaction_title, amount, creation_date. methods -> get_records(), create_record()
        - Expense: variables -> id_expense, expense_title, expense_amount, id_category
        - Income: variables -> id_income, income_title, income_amount, id_category
## Services
    - expense_service.py
    - income_service.py
    - category_service.py
    - file_storage.py
## Utils
    - validations.py

## Tests
    - test_expense_service.py
    - test_income_services.py
    - test_category_services.py
    - test_file_storage.py