#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------------
Project Name: reference_architecture
File Name:    primary_widgets.py
Author:       helmutngawa
Date:         27.06.26
Description:  This file contains the primary widget classes. The goal is to
define reusable widget easy to change.
-------------------------------------------------------------------------------
"""

from tkinter import ttk


class PrimaryButton(ttk.Button):
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            style="Primary.TButton",
            **kwargs
        )


class PrimaryCombobox(ttk.Combobox):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(
            parent,
            style="Primary.TCombobox",
            *args,
            **kwargs
        )

class PrimaryEntry(ttk.Entry):
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            style="Primary.TEntry",
            **kwargs
        )


class PrimaryFrame(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            style="Primary.TFrame",
            **kwargs
        )


class PrimaryLabel(ttk.Label):
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            style="Primary.TLabel",
            **kwargs
        )


class PrimaryTreeview(ttk.Treeview):
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            style="Primary.TTreeview",
            **kwargs
        )

class PrimaryNotebook(ttk.Notebook):
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            style="Primary.TNotebook",
            **kwargs
        )
