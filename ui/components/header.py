import tkinter as tk

from ui.widgets.primary_widgets import PrimaryCombobox
from ui.widgets.primary_widgets import (PrimaryButton, PrimaryFrame, PrimaryEntry,
                                        PrimaryLabel)


class Header(PrimaryFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, height=50)

        self.controller = controller

        PrimaryLabel(self, text="Select model:").pack(side="left")

        self.selected_model = tk.StringVar()
        self.combobox = PrimaryCombobox(self, textvariable=self.selected_model)
        self.combobox['values'] = ["Data model", "Device model"]
        self.combobox['state'] = 'readonly'
        self.combobox.current(0)
        self.combobox.bind('<<ComboboxSelected>>', self.on_combobox_changed)
        self.combobox.pack(side="left")

        self.address_label = PrimaryLabel(self, text="URL:")
        self.address_label.pack(side="left")

        self.entry_field = PrimaryEntry(self, width=20)
        self.entry_field.pack(side="left", padx=5)

        self.btn_power = PrimaryButton(self, command=self.on_power)
        self.btn_power.config(text="Power ON", style="Green.TButton")
        self.btn_power.pack(side="left")

    def on_power(self):
        ip = self.entry_field.get()
        if self.btn_power['text'] == "Power ON":
            self.controller.power_on(ip)
            self.btn_power.config(text="Power OFF", style="Red.TButton")
        else:
            self.controller.power_off(ip)
            self.btn_power.config(text="Power ON", style="Green.TButton")

    def on_combobox_changed(self, event):
        if self.selected_model.get() == "Data model":
            self.address_label.config(text="URL:")
        else:
            self.address_label.config(text="IP address:")
        print(self.selected_model.get())