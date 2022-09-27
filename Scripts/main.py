import requests
import PySimpleGUI as sg
import layouts
import eventHandler
import os.path


def main():
    window: sg.Window = layouts.layLayouts()
    eventHandler.handleEvents(window)


if __name__ == "__main__":
    main()
