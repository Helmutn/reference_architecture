#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------------
Project Name: reference_architecture
File Name:    youtube_tracker_tab.py
Author:       helmutngawa
Date:         27.06.26
Description:  [Enter a brief description of the script's purpose]
-------------------------------------------------------------------------------
"""

from ui.widgets.primary_widgets import PrimaryLabel
from ui.tabs.base_tab import BaseTab


class YoutubeTrackerTab(BaseTab):
    def __init__(self, parent, controller, event_bus):
        super().__init__(parent, controller, event_bus)

        self.label = PrimaryLabel(self, text=controller)
        self.label.pack(pady=20)

        event_bus.subscribe("tracker_status", self.update_status)

    def update_status(self, status):
        self.label.config(text=status)