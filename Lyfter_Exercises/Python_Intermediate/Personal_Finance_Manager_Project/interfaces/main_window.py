import FreeSimpleGUI as sg
from interfaces.create_category_window import show_create_category_window
from interfaces.create_expense_window import show_create_expense_window
from interfaces.gui_components import create_window, window_title, primary_button
from interfaces.expenses_partial import build_expense_section, refresh_expenses_table, ADD_BUTTON_KEY
from interfaces.incomes_partial import build_income_section, refresh_incomes_table, ADD_INCOME_BUTTON_KEY
from interfaces.create_income_window import show_create_income_window

def show_main_window():
    # Declare the elements
    layout = [
        [window_title(" WELCOME TO THE PERSONAL FINANCE APP", "✓ Monitor your cash flow with our app")],
        [sg.Text("")],
        [primary_button("Add New Category")],
        [sg.Text("")],
        [build_expense_section()],
        [sg.Text("")],
        [build_income_section()]
    ]

    # Create Window
    window = create_window("HOME", layout, resizable=True, location=(600, 100))


    # Event loop to process "events" and get the inputs "values"
    while True:
        event, values = window.read()
        if event == "Add New Category":
            show_create_category_window()
        if event == ADD_BUTTON_KEY:
            show_create_expense_window()
            refresh_expenses_table(window)
        if event == ADD_INCOME_BUTTON_KEY:
            show_create_income_window()
            refresh_incomes_table(window)


        # Close window event
        if event == sg.WIN_CLOSED:
            break
    window.close() 

