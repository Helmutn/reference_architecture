# This file was reconstructed from .pyc bytecode
# Original source was lost during git history rewrite
# Please restore from backup if available
from ui.tabs.base_tab import BaseTab
from ui.widgets.primary_widgets import PrimaryLabel
class FinanceTab(BaseTab):
    """Finance calculator and loan management tab."""
    def __init__(self, parent, controller, event_bus):
        """Initialize FinanceTab."""
        super().__init__(parent, event_bus)
        self.controller = controller
        PrimaryLabel(self, text="Finance Module").pack(pady=20)
