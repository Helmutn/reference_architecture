from tkinter import ttk

from ui.components.menu_bar import MenuBar
from ui.components.header import Header
from ui.components.logger import Logger
from ui.components.footer import FooterStatus

from ui.widgets.primary_widgets import PrimaryNotebook
from ui.widgets.primary_widgets import PrimaryFrame

from ui.tabs.control_tab import ControlTab
from ui.tabs.monitoring_tab import MonitoringTab
from ui.tabs.youtube_tracker_tab import YoutubeTrackerTab


class MainWindow:
    def __init__(self, root, controller, event_bus):
        root.config(menu=MenuBar())

        self.header = Header(root, controller)
        self.header.pack(fill="x", side="top", padx=10, pady=10)

        core_frame = PrimaryFrame(root, padding=5)
        core_frame.pack(fill="both", expand=True)
        # Wichtig: Die Spalte im Core Frame muss dehnbar sein
        core_frame.columnconfigure(0, weight=1)
        # Zeilen-Gewichtung für das 70:30 Verhältnis definieren:
        # Zeile 0 (Tab) bekommt Gewicht 7, Zeile 1 (Logger) bekommt Gewicht 3
        core_frame.rowconfigure(0, weight=7)
        core_frame.rowconfigure(1, weight=3)

        tab_frame =PrimaryFrame(core_frame)
        tab_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=(5, 0))

        logger_frame = PrimaryFrame(core_frame)
        logger_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=(5, 0))

        notebook = PrimaryNotebook(tab_frame)
        notebook.pack(fill="both", expand=True)

        notebook.add(
            YoutubeTrackerTab(
                notebook,
                controller,
                event_bus
            ),
            text="Youtube Tracker"
        )

        notebook.add(
            ControlTab(
                notebook,
                controller,
                event_bus
            ),
            text="Control"
        )

        notebook.add(
            MonitoringTab(
                notebook,
                controller,
                event_bus
            ),
            text="Monitoring"
        )

        self.logger = Logger(logger_frame, event_bus)
        self.logger.pack(fill="both", expand=True, pady=(5, 0))

        self.footer_status = FooterStatus(root)
        self.footer_status.pack(fill="x", side="bottom", padx=10, pady=10)