from tkinter import ttk

from ui.components.header import Header
from ui.components.footer import Footer

from ui.tabs.control_tab import ControlTab
from ui.tabs.monitoring_tab import MonitoringTab


class MainWindow:

    def __init__(
        self,
        root,
        controller,
        event_bus
    ):

        Header(
            root,
            controller
        ).pack(
            fill="x",
            padx=10,
            pady=10
        )

        notebook = ttk.Notebook(root)

        notebook.pack(
            fill="both",
            expand=True
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

        Footer(
            root,
            event_bus
        ).pack(
            fill="both"
        )