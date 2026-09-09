import FreeSimpleGUI as sg
from services.income_service import get_all_incomes

from interfaces.gui_components import (
    primary_button, element_label, table, BACKGROUND
)

TABLE_KEY = "-INCOMES_TABLE-"
ADD_INCOME_BUTTON_KEY = "-ADD_INCOME-"
HEADINGS = ["Title", "Amount", "Category"]

def get_income_rows():
    return [
        [e.transaction_title, e.amount, e.category_name] for e in get_all_incomes()
    ]

def build_income_section():
    rows = get_income_rows()
    return sg.Column( 
        [ [element_label("INCOMES"), 
           sg.Push(), 
           primary_button("+ Add Income", key=ADD_INCOME_BUTTON_KEY)], 
           [table(rows, HEADINGS, TABLE_KEY, 5, col_widths=[25, 12, 18])],
           ], 
        background_color=BACKGROUND,
        expand_x=True,
        expand_y=True
        )

def refresh_incomes_table(window):
    window[TABLE_KEY].update(values=get_income_rows())