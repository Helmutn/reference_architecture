# This file was reconstructed from .pyc bytecode
# Original source was lost during git history rewrite
# Please restore from backup if available
from ui.tabs.base_tab import BaseTab
from ui.widgets.primary_widgets import PrimaryLabel
class ImmoLoanTab(BaseTab):
    """Immobiliendarlehen (real estate loan) calculator tab."""
    def __init__(self, parent, controller, event_bus):
        """Initialize ImmoLoanTab."""
        super().__init__(parent, event_bus)
        self.controller = controller
        PrimaryLabel(self, text="Immobiliendarlehen Rechner").pack(pady=20)
