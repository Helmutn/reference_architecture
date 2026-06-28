from ui.widgets.primary_widgets import PrimaryLabel
from ui.tabs.base_tab import BaseTab


class MonitoringTab(BaseTab):
    def __init__(self, parent, controller, event_bus):
        super().__init__(parent, controller, event_bus)

        self.label = PrimaryLabel(self, text="UNBEKANNT")
        self.label.pack(pady=20)

        event_bus.subscribe("device_status", self.update_status)

    def update_status(self, status):
        self.label.config(text=status)