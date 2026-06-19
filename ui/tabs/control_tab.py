from tkinter import ttk
from ui.tabs.base_tab import BaseTab


class ControlTab(BaseTab):

    def __init__(
        self,
        parent,
        controller,
        event_bus
    ):

        super().__init__(
            parent,
            controller,
            event_bus
        )

        ttk.Label(
            self,
            text="Gerätesteuerung"
        ).pack(pady=20)