# from tkinter import Menu
from ttkbootstrap import Menu


class BaseMenu(Menu):
    def __init__(self):
        super().__init__(tearoff=0)

    def add_menu(self, name:str, menu: Menu):
        self.add_cascade(label=name, menu=menu)


class MenuBar(BaseMenu):
    def __init__(self, callback:dict):
        super().__init__()

        self.callback = callback

        self.menu_file = BaseMenu()
        self.menu_edit = BaseMenu()
        self.menu_tools = BaseMenu()
        self.menu_test = BaseMenu()
        self.menu_help = BaseMenu()

        self.add_menu("File", menu=self.menu_file)
        self.add_menu("Edit", menu=self.menu_edit)
        self.add_menu("Tools", menu=self.menu_tools)
        self.add_menu("Test", menu=self.menu_test)
        self.add_menu("Help", menu=self.menu_help)

        self.menu_edit.add_cascade(label="Clear logger",
                                   command=self.callback.get("clear_logger"))