from tkinter import ttk


class BaseTab(ttk.Frame):

    def __init__(
        self,
        parent,
        controller,
        event_bus
    ):

        super().__init__(parent)

        self.controller = controller
        self.event_bus = event_bus