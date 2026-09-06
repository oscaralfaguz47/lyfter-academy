import FreeSimpleGUI as sg
from interfaces.create_category_window import show_create_category_window

def show_main_window():
    # Declare the elements
    layout = [
        [sg.Text(" WELCOME TO THE PERSONAL FINANCE APP", font=("Helvetica", 14, "bold"))],
        [sg.Text("")],
        [sg.Button("Add New Category")]
    ]

    # Create Window
    window = sg.Window("HOME", layout, location=(400, 200))


    # Event loop to process "events" and get the inputs "values"
    while True:
        event, values = window.read()
        if event == "Add New Category":
            show_create_category_window()


        # Close window event
        if event == sg.WIN_CLOSED:
            break
    window.close() 

