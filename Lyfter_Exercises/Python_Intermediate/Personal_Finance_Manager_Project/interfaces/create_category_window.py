import FreeSimpleGUI as sg
from services.category_service import create_category
from interfaces.gui_components import create_window, window_title, primary_button, cancel_button, element_label, error_label, input_text

def show_create_category_window():
    # Declare the elements
    layout = [
        [window_title("Create New Category", "Add a category to organize your transactions (expense/income)")],
        [sg.Text("")],
        [element_label("Category Name"), input_text(key="-CATEGORY_NAME-")],
        [error_label()],
        [primary_button("Create Category", key="-CREATE-"), cancel_button("Cancel")],
    ]

    # Create Window
    window = create_window("Create Category", layout, resizable=True)

    # Event loop to process "events" and get the inputs "values"
    while True:
        event, values = window.read()

        if event == "-CREATE-":
            try:
                create_category(values["-CATEGORY_NAME-"])
                window.close()
            except TypeError as e:
                window["-ERROR-"].update(e)
            except ValueError as e:
                window["-ERROR-"].update(e)

        # Close window event
        if event == sg.WIN_CLOSED or event == "Cancel":
            break
    window.close() 
