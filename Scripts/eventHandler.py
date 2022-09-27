import PySimpleGUI as sg
import requestSender
import os


def handleEvents(window):
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        elif event == "Go":
            responce, name = requestSender.sendRequest(values)
            os.makedirs(os.getcwd() + "/OK", exist_ok=True)
    window.close()
