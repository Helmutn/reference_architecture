from tkinter import ttk
from ui.widgets.primary_button import PrimaryButton


class Header(ttk.Frame):

    def __init__(
        self,
        parent,
        controller
    ):

        super().__init__(parent)

        self.controller = controller

        ttk.Label(
            self,
            text="IP:"
        ).pack(side="left")

        self.ip_entry = ttk.Entry(
            self,
            width=20
        )

        self.ip_entry.pack(
            side="left",
            padx=5
        )

        PrimaryButton(
            self,
            text="Power ON",
            command=self.on_power_on
        ).pack(side="left")

    def on_power_on(self):

        ip = self.ip_entry.get()

        self.controller.power_on(ip)