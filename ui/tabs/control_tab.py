from ui.widgets.primary_widgets import PrimaryLabel
from ui.tabs.base_tab import BaseTab


class ControlTab(BaseTab):
    def __init__(self, parent, controller, event_bus):
        super().__init__(parent, event_bus)

        PrimaryLabel(self, text="Gerätesteuerung").pack(pady=20)