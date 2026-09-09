import FreeSimpleGUI as sg
from services.income_service import create_income
from services.category_service import get_all_categories
from interfaces.gui_components import create_window, window_title, primary_button, cancel_button, element_label, error_label, input_text, input_dropdown
from interfaces.incomes_partial import refresh_incomes_table

def show_create_income_window():
    # Declare the elements
    categories = get_all_categories()
    category_map = {c.category_name: c.id_category for c in categories}

    layout = [
        [window_title("Create New Income", "Track all your incomes")],
        [sg.Text("")],
        [element_label("Income title"), input_text(key="-INCOME_TITLE-")],
        [element_label("Amount"), input_text(key="-AMOUNT-")],
        [element_label("Category"), input_dropdown("-CATEGORY-", list(category_map.keys()))],
        [error_label()],
        [primary_button("Create Income", key="-CREATE-"), cancel_button("Cancel")],
    ]

    # Create Window
    window = create_window("Create Income", layout, resizable=True, location=(600, 100))

    # Event loop to process "events" and get the inputs "values"
    while True:
        event, values = window.read()

        if event == "-CREATE-":
            selected_category = values["-CATEGORY-"]
            id_category = ""
            if selected_category:
                id_category = category_map[selected_category]
            try:
                create_income(values["-INCOME_TITLE-"], values["-AMOUNT-"], id_category)
                break
            except (TypeError, ValueError) as e:
                window["-ERROR-"].update(str(e))

        # Close window event
        if event == sg.WIN_CLOSED or event == "Cancel":
            break
    window.close() 
