from ui.widgets.primary_widgets import PrimaryFrame


class BaseTab(PrimaryFrame):
    def __init__(self, parent, event_bus):
        super().__init__(parent)

        self.event_bus = event_bus

    def print_logger(self, message):
        self.event_bus.emit("log", message)