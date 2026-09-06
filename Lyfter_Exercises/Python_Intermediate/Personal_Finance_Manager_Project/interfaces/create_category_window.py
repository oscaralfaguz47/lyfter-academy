import FreeSimpleGUI as sg
from services.category_services import create_category

def show_create_category_window():
    # Declare the elements
    layout = [
        [sg.Text("Create New Category", font=("Helvetica", 14, "bold"))],
        [sg.Text("")],
        [sg.Text("Category Name", size=(15, 1), font=("bold")), sg.Input(key="-CATEGORY_NAME-")],
        [sg.Text("", key="-ERROR-", text_color="red")],
        [sg.Button("Create Category")]
    ]

    # Create Window
    window = sg.Window("Create Category", layout, location=(400, 200))

    # Event loop to process "events" and get the inputs "values"
    while True:
        event, values = window.read()

        if event == "Create Category":
            try:
                create_category(values["-CATEGORY_NAME-"])
                window.close()
                sg.popup("Changes saved", location=(400, 200))
            except TypeError as e:
                window["-ERROR-"].update(e)
            except ValueError as e:
                window["-ERROR-"].update(e)

        # Close window event
        if event == sg.WIN_CLOSED:
            break
    window.close() 
