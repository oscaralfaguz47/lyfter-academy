import FreeSimpleGUI as sg

from interfaces.gui_components import (
    primary_button, element_label, table, BACKGROUND
)

TABLE_KEY = "-EXPENSES_TABLE-"
ADD_BUTTON_KEY = "-ADD_EXPENSE-"
HEADINGS = ["Title", "Amount", "Category"]

def build_expense_section(records_to_display):
    return sg.Column( 
        [ [element_label("Expenses"), 
           sg.Push(), 
           primary_button("+ Add Expense", key=ADD_BUTTON_KEY)], 
           [table(records_to_display, HEADINGS, TABLE_KEY, len(records_to_display))],
           ], 
        background_color=BACKGROUND,
        expand_x=True
        )

