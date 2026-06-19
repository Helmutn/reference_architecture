from tkinter import ttk


def apply_theme():

    style = ttk.Style()

    style.theme_use("clam")

    style.configure(
        "Primary.TButton",
        font=("Segoe UI", 10),
        padding=6
    )

    style.configure(
        "Status.TLabel",
        font=("Segoe UI", 11, "bold")
    )