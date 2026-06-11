import tkinter as tk


def create_app():
    root = tk.Tk()
    root.title("GUI Product shop")
    root.geometry("700x600+200+200")

    return root

app = create_app()