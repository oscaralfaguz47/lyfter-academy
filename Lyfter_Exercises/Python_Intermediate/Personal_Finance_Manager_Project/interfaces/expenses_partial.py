import FreeSimpleGUI as sg
from services.expense_service import get_all_expenses

from interfaces.gui_components import (
    primary_button, element_label, table, BACKGROUND
)

TABLE_KEY = "-EXPENSES_TABLE-"
ADD_BUTTON_KEY = "-ADD_EXPENSE-"
HEADINGS = ["Title", "Amount", "Category"]

def get_expense_rows():
    return [
        [e.transaction_title, e.amount, e.category_name] for e in get_all_expenses()
    ]

def build_expense_section():
    rows = get_expense_rows()
    return sg.Column( 
        [ [element_label("Expenses"), 
           sg.Push(), 
           primary_button("+ Add Expense", key=ADD_BUTTON_KEY)], 
           [table(rows, HEADINGS, TABLE_KEY, len(rows))],
           ], 
        background_color=BACKGROUND,
        expand_x=True
        )

def refresh_expenses_table(window):
    window[TABLE_KEY].update(values=get_expense_rows())