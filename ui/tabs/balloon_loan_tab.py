# This file was reconstructed from .pyc bytecode
# Original source was lost during git history rewrite
# Please restore from backup if available
from ui.tabs.base_tab import BaseTab
from ui.widgets.primary_widgets import PrimaryLabel
class BalloonLoanTab(BaseTab):
    """Balloon loan calculator tab."""
    def __init__(self, parent, controller, event_bus):
        """Initialize BalloonLoanTab."""
        super().__init__(parent, event_bus)
        self.controller = controller
        PrimaryLabel(self, text="Ballon-Darlehen Rechner").pack(pady=20)
