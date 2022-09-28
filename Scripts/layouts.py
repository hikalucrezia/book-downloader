import random
import PySimpleGUI as sg
import os.path

# First the window layout in 2 columns


def layLayouts() -> sg.Window:
    sg.theme("LightBlue")

    post_requests_column = [
        [sg.Text("Request headers:")],
        [sg.Multiline(size=(100, 20), key="-headers")],
        [
            sg.Text("Folder name:"),
            sg.InputText(default_text=str(random.randint(100000,
                                                         999999)), size=(60, 1), key="-foldername")
        ],
        [
            sg.Text("Pages: From"),
            sg.InputText(default_text="1", size=(10, 1), key="-firstpage"),
            sg.Text("To"),
            sg.InputText(default_text="2", size=(10, 1), key="-finalpage")
        ],
    ]

    image_viewer_column = [
        [sg.Image(key="-image", enable_events=True, expand_x=False, expand_y=False, size=(400, 300))],
    ]

    layout = [
        [
            sg.Column(post_requests_column),
            sg.VSeperator(),
            sg.Column(image_viewer_column),
        ],
        [
            sg.ProgressBar(max_value=1, orientation='h', size=(40, 10), key='progress'),
            sg.Button(button_text="Go"),
        ]
    ]

    window = sg.Window("Maruzen Book Downloader", layout)
    return window
