import tkinter as tk
import requests as rq


def main():
    root = tk.Tk()
    root.title("TEST OK")
    root.geometry("640x480")

    label = tk.Label(root, text="SHIT")

    label.pack()

    button = tk.Button()
    button["text"] = "CLICK ME"
    button["command"] = pri
    button.pack()

    root.mainloop()


def pri():
    print("FUCK YOU")


if __name__ == "__main__":
    main()
