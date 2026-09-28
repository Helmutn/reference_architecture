
from ui.tabs.base_tab import BaseTab
from ui.tabs.immo_loan_tab import ImmoLoanTab
from ui.tabs.annuity_loan_tab import AnnuityLoanTab
from ui.tabs.balloon_loan_tab import BalloonLoanTab
from ui.widgets.primary_widgets import PrimaryLabel, PrimaryNotebook

class FinanceTab(BaseTab):
    """Finance calculator and loan management tab."""
    def __init__(self, parent, controller, event_bus):
        """Initialize FinanceTab."""
        super().__init__(parent, event_bus)
        self.controller = controller

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Sub-Notebook erstellen
        self.sub_notebook = PrimaryNotebook(self)
        # Wenn das übergeordnete Fenster grid nutzt, verwende hier ebenfalls grid:
        self.sub_notebook.grid(row=0, column=0, sticky="nsew")

        # Immo Rechner hinzufügen
        self.immo_loan_tab = ImmoLoanTab(self.sub_notebook, controller, event_bus)
        self.sub_notebook.add(self.immo_loan_tab, text="Immo-Darlehen", sticky="nsew")
        self.sub_notebook.tab(self.immo_loan_tab, state="normal")
        # Annuitäten Rechner hinzufügen
        self.annuity_loan_tab = AnnuityLoanTab(self.sub_notebook, controller, event_bus)
        self.sub_notebook.add(self.annuity_loan_tab, text="Annuität-Darlehen", sticky="nsew")
        self.sub_notebook.tab(self.annuity_loan_tab, state="normal")
        # Ballon Rechner hinzufügen
        self.balloon_loan_tab = BalloonLoanTab(self.sub_notebook, controller, event_bus)
        self.sub_notebook.add(self.balloon_loan_tab, text="Balloon-Darlehen", sticky="nsew")
        self.sub_notebook.tab(self.balloon_loan_tab, state="normal")
