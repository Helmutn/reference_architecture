import tkinter as tk
from tkinter import ttk


class Footer(ttk.Frame):

    def __init__(
        self,
        parent,
        event_bus
    ):

        super().__init__(parent)

        self.log_box = tk.Text(
            self,
            height=8
        )

        self.log_box.pack(
            fill="both",
            expand=True
        )

        event_bus.subscribe(
            "log",
            self.add_log
        )

    def add_log(self, text):

        self.log_box.insert(
            "end",
            text + "\n"
        )

        self.log_box.see("end")