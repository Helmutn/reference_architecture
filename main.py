# from tkinter import *

import ttkbootstrap as tb

from config.theme import apply_theme
from infrastructure.container import Container
from ui.main_window import MainWindow


def main():

    # root = tk.Tk()
    root = tb.Window(themename="pulse")

    root.title("Device Controller")

    root.geometry("900x700")

    apply_theme()

    container = Container()

    MainWindow(
        root,
        container.controller,
        container.event_bus
    )

    container.thread_manager.start(container.monitoring_service.start)

    root.mainloop()


if __name__ == "__main__":
    main()