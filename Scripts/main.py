import PySimpleGUI as sg
import layouts
import eventHandler
import os


def main():
    try:
        window: sg.Window = layouts.layLayouts()
        eventHandler.handleEvents(window)
    except Exception as e:
        with open(os.getcwd()+"/errormessage.txt", 'a') as f:
            print(str(e)+"\n", file=f)
    return


if __name__ == "__main__":
    main()
