from ui.widgets.primary_widgets import PrimaryFrame


class BaseTab(PrimaryFrame):
    def __init__(self, parent, controller, event_bus):
        super().__init__(parent)

        self.controller = controller
        self.event_bus = event_bus