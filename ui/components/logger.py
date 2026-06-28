import sys
import pyperclip
import tkinter as tk

from datetime import datetime
from ui.widgets.primary_widgets import PrimaryTreeview

class Logger(PrimaryTreeview):
    def __init__(self, parent, event_bus):
        super().__init__(parent, columns=("msg",))

        self.heading("#0", text='Time')
        self.heading("msg", text='Message', anchor='w')
        self.column("#0", width=150, minwidth=125)
        self.column("msg", width=2250, minwidth=500)
        self.pack(side='left', fill='both')
        scroller_x_axe = tk.Scrollbar(parent, orient='horizontal')
        scroller_x_axe.pack(side='bottom', fill='x')
        scroller_y_axe = tk.Scrollbar(parent)
        scroller_y_axe.pack(side='right', fill='y')
        scroller_x_axe.config(command=self.xview)
        scroller_y_axe.config(command=self.yview)
        self.config(xscrollcommand=scroller_x_axe.set, yscrollcommand=scroller_y_axe.set)
        self.tag_configure('error', foreground='red')
        
        def copy_from_treeview(_):
            selections = self.selection()  # get hold of selected rows
            copied_string = ""
            for row in selections:
                text = self.item(row, 'text')  # get text for each selected row
                values = self.item(row, 'values')  # get values for each selected row
                tmp_value = ''
                for item in values:
                    tmp_value += f"{item} "
                copied_string += f"{text} {tmp_value}\n"
            pyperclip.copy(copied_string)

            # Erkennt macOS automatisch
            if sys.platform == "darwin":
                self.bind("<Command-Key-c>", copy_from_treeview)
            else:
                self.bind("<Control-Key-c>", copy_from_treeview)

        event_bus.subscribe("log", self.add_log)

    def clear_logger(self):
        for row in self.get_children():
            self.delete(row)

    def add_log(self, p_message, error_msg=False):
        current_datetime = datetime.now().strftime("%d.%m.%Y, %H:%M:%S")
        if error_msg:
            self.insert("", 0, text=current_datetime, values=(p_message,), tags='error')
            # self.footer.bump_errors(1)
        else:
            self.insert("", 0, text=current_datetime, values=(p_message,))
        # self.footer.set_errors(get_http_error_count())