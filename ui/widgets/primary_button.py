from tkinter import ttk


class PrimaryButton(ttk.Button):

    def __init__(self, parent, **kwargs):

        super().__init__(
            parent,
            style="Primary.TButton",
            **kwargs
        )