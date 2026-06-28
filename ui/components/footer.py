import tkinter as tk

from tkinter import ttk
from ui.widgets.primary_widgets import (PrimaryButton, PrimaryFrame, PrimaryEntry, 
                                        PrimaryLabel)


class Footer(PrimaryFrame):
    """
    Field at the end of the tool containing some information about the footer.
    This information has to be defined here later ...
    """
    def __init__(self, parent, event_bus):
        super().__init__(parent)

        self.event_bus = event_bus


class FooterStatus(PrimaryFrame):
    """
    Thin status bar showing: Power, Run, Connection (left), Error count (right).
    Colors:
      - Power: green(on), amber(standby), red(off)
      - Run: green(running), grey(idle), red(error)
      - Errors: green(0), red(>0)
    """

    def __init__(self, parent, *, padding=(8, 2, 8, 2)):
        super().__init__(parent, height=40)
        self._err_count = 0

        # Top hairline to detach from Treeview
        ttk.Separator(self, orient="horizontal").grid(row=0, column=0, columnspan=10, sticky="ew")

        # StringVars
        self._power_sv = tk.StringVar(value="Power: Unknown")
        self._run_sv = tk.StringVar(value="Run: —")
        self._conn_sv = tk.StringVar(value="Connected: —")
        self._err_sv = tk.StringVar(value="error count: 0")

        # Small colored dots for quick glance
        self._dot_power = PrimaryLabel(self, text="●")
        self._dot_run = PrimaryLabel(self, text="●")

        # Labels
        self._lbl_power = PrimaryLabel(self, textvariable=self._power_sv)
        self._lbl_run = PrimaryLabel(self, textvariable=self._run_sv)
        self._lbl_conn = PrimaryLabel(self, textvariable=self._conn_sv)
        self._lbl_err = PrimaryLabel(self, textvariable=self._err_sv)

        # Layout  (row 1 = content)
        r, c = 1, 0
        self._dot_power.grid(row=r, column=c, padx=(8, 4))
        c += 1
        self._lbl_power.grid(row=r, column=c)
        c += 1
        ttk.Separator(self, orient="vertical").grid(row=r, column=c, sticky="ns", padx=6)
        c += 1
        self._dot_run.grid(row=r, column=c, padx=(8, 4))
        c += 1
        self._lbl_run.grid(row=r, column=c)
        c += 1
        ttk.Separator(self, orient="vertical").grid(row=r, column=c, sticky="ns", padx=6)
        c += 1
        self._lbl_conn.grid(row=r, column=c, padx=(8, 4))
        c += 1

        # Spacer to push error label to far right
        self.columnconfigure(c, weight=1)
        c += 1
        self._lbl_err.grid(row=r, column=c, padx=(0, 8))

        self.configure(padding=padding)

        # neutral initial colors
        self._set_fg(self._dot_power, "#888")
        self._set_fg(self._dot_run, "#888")
        self._set_fg(self._lbl_err, "#2e7d32")  # green if 0

    # --- public API ---
    def set_connection(self, txt: str | None):
        self._conn_sv.set(f"Connected: {txt or '—'}")

    def set_power(self, state: str):
        s = (state or "unknown").lower()
        label = {
            "on": "Power: ON",
            "off": "Power: OFF",
            "standby": "Power: Standby",
            "unknown": "Power: Unknown"
        }.get(s, "Power: Unknown")
        color = {"on": "#2e7d32", "off": "#b71c1c", "standby": "#f9a825", "unknown": "#888"}.get(s, "#888")
        self._power_sv.set(label)
        self._set_fg(self._dot_power, color)

    def set_run_state(self, state: str | bool):
        if isinstance(state, bool):
            label = "Run: Running" if state else "Run: Idle"
            color = "#2e7d32" if state else "#888"
        else:
            s = str(state or "").lower()
            label = f"Run: {s.capitalize() or '—'}"
            color = {"running": "#2e7d32", "idle": "#888", "stopped": "#455a64", "error": "#b71c1c"}.get(s, "#888")
        self._run_sv.set(label)
        self._set_fg(self._dot_run, color)

    def set_errors(self, n: int):
        self._err_count = max(0, int(n or 0))
        self._err_sv.set(f"error count: {self._err_count}")
        self._set_fg(self._lbl_err, "#2e7d32" if self._err_count == 0 else "#b71c1c")

    def bump_errors(self, delta: int = 1):
        self.set_errors(self._err_count + delta)

    def reset(self):
        self.set_connection("—")
        self.set_power("off")
        self.set_run_state("idle")
        self.set_errors(0)

    # --- helpers ---
    def _set_fg(self, widget: PrimaryLabel, color: str):
        try:
            widget.configure(foreground=color)
        except tk.TclError:
            s = ttk.Style(self)
            name = f"{str(widget)}.TLabel"
            s.configure(name, foreground=color)
            widget.configure(style=name)