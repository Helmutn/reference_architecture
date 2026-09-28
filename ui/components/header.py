import tkinter as tk

from ui.widgets.primary_widgets import PrimaryCombobox
from ui.widgets.primary_widgets import (PrimaryButton, PrimaryFrame, PrimaryEntry, PrimaryLabel)


class Header(PrimaryFrame):
    def __init__(self, parent, controller, event_bus):
        super().__init__(parent, height=50)

        self.controller = controller
        self.event_bus = event_bus
        self.strvar_link = tk.StringVar()

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

        self.entry_field = PrimaryEntry(self, width=20, textvariable=self.strvar_link)
        self.entry_field.pack(side="left", padx=5)
        self.strvar_link.trace_add("write", self.on_entry_changed)

        self.btn_power = PrimaryButton(self, command=self.on_power, state="disabled")
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
        self.event_bus.emit("power_changed", self.btn_power['text'])

    def on_combobox_changed(self, event):
        if self.selected_model.get() == "Data model":
            self.address_label.config(text="URL:")
            self.controller.data_service.set_model_selected(True)
        else:
            self.address_label.config(text="IP address:")
        self.strvar_link.set("")
        self.btn_power.config(state="disabled")
        self.event_bus.emit("model_changed", self.selected_model.get())
        self.event_bus.emit("log", f"{self.selected_model.get()} has been selected")

    def on_entry_changed(self, *args):
        """
        Event handling function to react on change inside the entry field containing url or ip address.
        :param args:
        :return: None
        """
        if self.selected_model.get() == "Data model":
            self.controller.data_service.set_url(self.strvar_link.get())
            self.event_bus.emit("log", "Url has been updated")
        if len(self.strvar_link.get()) > 15:
            self.btn_power.config(state="normal")
        else:
            self.btn_power.config(state="disabled")