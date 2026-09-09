import FreeSimpleGUI as sg


# Colors
PRIMARY = "#2E86AB"
SUCCESS = "#28A745"
NEUTRAL = "#6C757D"
TEXT_MUTED = "#9BA8B4"
TEXT_LIGHT = "#E8E8E8"
DANGER = "#DC3545"
BACKGROUND = "#1E2A38"
INPUT_BG = "#34455A"
SURFACE = "#2A3847"

# Fonts
FONT_FAMILY = "Any"
FONT_TITLE = (FONT_FAMILY, 18, "bold")
FONT_SUBTITLE = (FONT_FAMILY, 10)
FONT_LABEL = (FONT_FAMILY, 11, "bold")
FONT_BUTTON = (FONT_FAMILY, 11, "bold")

def apply_theme():
    sg.theme("DarkBlue3")
    sg.set_options(
        background_color=BACKGROUND,
        text_element_background_color=BACKGROUND,
        element_background_color=BACKGROUND,
        input_elements_background_color=INPUT_BG,
        input_text_color=TEXT_LIGHT,
        text_color=TEXT_LIGHT,
        font=(FONT_FAMILY, 11),
        element_padding=(5, 5)
    )

def create_window(title, layout, resizable=False, location=(600, 100)):
    window = sg.Window(
        title,
        layout,
        background_color=BACKGROUND,
        element_justification="center",
        margins=(30, 25),
        resizable=resizable,
        finalize=True,
        no_titlebar=False,
        grab_anywhere=False,
        location=location
    )


    for element in window.element_list():
        if isinstance(element, sg.Button):
            element.set_cursor("hand2")
    return window


def window_title(text, subtitle=None):
    rows = [
        [sg.Text(text, font=FONT_TITLE, text_color=PRIMARY, pad=((0, 0), (10, 2)))]
    ]
    if subtitle:
        rows.append(
            [sg.Text(subtitle, font=FONT_SUBTITLE, text_color=TEXT_MUTED, pad=((0, 0), (0, 8)))]
        )
    rows.append([sg.HorizontalSeparator(color=PRIMARY)])
    return sg.Column(rows, expand_x=True, element_justification="left")

def primary_button(text, key=None):
    return sg.Button(
        text, 
        key=key or text,
        button_color=("white", PRIMARY),
        font=("Any", 11, "bold"),
        border_width=0
    )

def cancel_button(text, key=None):
    return sg.Button(
        text, 
        key=key or text,
        button_color=("white", NEUTRAL),
        font=("Any", 11, "bold"),
        border_width=0
    )

def element_label(text):
    return sg.Text(
        text, 
        size=(15, 1), 
        font=("Segoe UI", 11, "bold"),
        text_color=TEXT_LIGHT,
        pad=((0, 10), (8, 8))
        )

def error_label(key="-ERROR-"):
    return sg.Text(
        "", key=key, text_color=DANGER, font=(FONT_FAMILY, 10), size=(40, 1)
    )

def input_text(key):
    return sg.Input(
        key=key,
        font=(FONT_FAMILY, 11),
        background_color=INPUT_BG,
        text_color=TEXT_LIGHT,
        border_width=0,
        pad=((0, 0), (8, 8)),
        size=(30, 1)
        )

def input_dropdown(key, values, default_value=None):
    return sg.Combo(
        values,
        default_value=default_value,
        key=key,
        font=(FONT_FAMILY, 11),
        background_color=INPUT_BG,
        text_color=TEXT_LIGHT,
        button_background_color=PRIMARY,
        button_arrow_color=TEXT_LIGHT,
        readonly=True,
        pad=((0, 0), (8, 8)),
        size=(28, 1)
    )

def table(values, headings, table_key, num_rows=5, col_widths=None):
    return sg.Table( 
        values=values, 
        headings=headings, 
        key=table_key, 
        num_rows=num_rows, 
        col_widths=col_widths,
        auto_size_columns=col_widths is None,
        justification="left", 
        font=(FONT_FAMILY, 10), 
        header_font=(FONT_FAMILY, 10, "bold"), 
        background_color=SURFACE, 
        text_color=TEXT_LIGHT, 
        header_background_color=PRIMARY, 
        header_text_color=TEXT_LIGHT, 
        alternating_row_color=BACKGROUND, 
        selected_row_colors=(TEXT_LIGHT, PRIMARY), 
        expand_x=True, 
        expand_y=True,
        hide_vertical_scroll=False, 
        border_width=0,
        row_height=28,
        pad=((0, 0), (10, 10)) 
        )