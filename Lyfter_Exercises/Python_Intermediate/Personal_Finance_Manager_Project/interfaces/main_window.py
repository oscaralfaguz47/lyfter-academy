import FreeSimpleGUI as sg
from interfaces.create_category_window import show_create_category_window
from interfaces.gui_components import create_window, window_title, primary_button

def show_main_window():
    # Declare the elements
    layout = [
        [window_title(" WELCOME TO THE PERSONAL FINANCE APP", "✓ Monitor your cash flow with our app")],
        [sg.Text("")],
        [primary_button("Add New Category")]
    ]

    # Create Window
    window = create_window("HOME", layout)


    # Event loop to process "events" and get the inputs "values"
    while True:
        event, values = window.read()
        if event == "Add New Category":
            show_create_category_window()


        # Close window event
        if event == sg.WIN_CLOSED:
            break
    window.close() 

