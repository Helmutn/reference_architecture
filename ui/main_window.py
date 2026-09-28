from ui.components.menu_bar import MenuBar
from ui.components.header import Header
from ui.components.logger import Logger
from ui.components.footer import FooterStatus

from ui.widgets.primary_widgets import PrimaryNotebook
from ui.widgets.primary_widgets import PrimaryFrame

from ui.tabs.control_tab import ControlTab
from ui.tabs.finance_tab import FinanceTab
from ui.tabs.monitoring_tab import MonitoringTab
from ui.tabs.youtube_tracker_tab import YoutubeTrackerTab


class MainWindow:
    def __init__(self, root, controller, event_bus):

        self.header = Header(root, controller, event_bus)
        self.header.pack(fill="x", side="top", padx=10, pady=10)

        core_frame = PrimaryFrame(root, padding=5)
        core_frame.pack(fill="both", expand=True)
        core_frame.columnconfigure(0, weight=1)
        core_frame.rowconfigure(0, weight=7)
        core_frame.rowconfigure(1, weight=3)

        tab_frame =PrimaryFrame(core_frame)
        tab_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=(5, 0))

        logger_frame = PrimaryFrame(core_frame)
        logger_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=(5, 0))

        # Save Notebook as instance variable
        self.notebook = PrimaryNotebook(tab_frame)
        self.notebook.pack(fill="both", expand=True)

        # Define tabs as instance variables
        self.finance_tab = FinanceTab(self.notebook, controller, event_bus)
        self.youtube_tracker_tab = YoutubeTrackerTab(self.notebook, controller, event_bus)
        self.control_tab = ControlTab(self.notebook, controller, event_bus)
        self.monitoring_tab = MonitoringTab(self.notebook, controller, event_bus)

        # Add tabs to notebook
        self.notebook.add(self.finance_tab, text="Finance")
        self.notebook.tab(self.finance_tab, state="normal")
        self.notebook.add(self.youtube_tracker_tab, text="Youtube Tracker")
        self.notebook.add(self.control_tab, text="Control")
        self.notebook.add(self.monitoring_tab, text="Monitoring")

        self.logger = Logger(logger_frame, event_bus)
        self.logger.pack(fill="both", expand=True, pady=(5, 0))

        self.footer_status = FooterStatus(root, event_bus)
        self.footer_status.pack(fill="x", side="bottom", padx=10, pady=10)

        menu_callback = dict()
        menu_callback["clear_logger"] = self.logger.clear_logger
        root.config(menu=MenuBar(menu_callback))

        self.controller = controller

        event_bus.subscribe("model_changed", self._on_model_changed)
        event_bus.subscribe("power_changed", self._on_power_changed)

    def _on_model_changed(self, model):
        """
        Event handling when the user selects a model.
        :param model: The selected model. For example, Data model or Device model.
        :return: None
        """
        if model == "Data model":
            self.notebook.tab(self.youtube_tracker_tab, state="normal")
            self.notebook.tab(self.control_tab, state="disabled")
            self.notebook.tab(self.finance_tab, state="normal")
            self.notebook.select(self.youtube_tracker_tab)
        else:
            self.notebook.tab(self.youtube_tracker_tab, state="disabled")
            self.notebook.tab(self.control_tab, state="normal")
            self.notebook.tab(self.finance_tab, state="normal")
            self.notebook.select(self.control_tab)

    def _on_power_changed(self, power_state):
        if power_state == "Power OFF":
            self.youtube_tracker_tab.btn_update.config(state="normal")
            self.notebook.tab(self.finance_tab, state="normal")
            if self.header.selected_model.get() == "Data model":
                self.notebook.tab(self.youtube_tracker_tab, state="normal")
                self.notebook.select(self.youtube_tracker_tab)
            else:
                self.notebook.tab(self.control_tab, state="normal")
                self.notebook.select(self.control_tab)
            self.footer_status.set_power("on")
            self.footer_status.set_connection(self.controller.data_service.get_url())
        else:
            self.youtube_tracker_tab.btn_update.config(state="disabled")
            self.notebook.tab(self.youtube_tracker_tab, state="disabled")
            self.notebook.tab(self.control_tab, state="disabled")
            self.notebook.tab(self.monitoring_tab, state="disabled")
            self.notebook.tab(self.finance_tab, state="disabled")
            self.footer_status.set_power("off")