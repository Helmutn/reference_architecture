import ttkbootstrap as tb
from ttkbootstrap.widgets.scrolled import ScrolledFrame
from ui.tabs.base_tab import BaseTab
from ui.widgets.primary_widgets import (
    PrimaryFrame, PrimaryLabel, PrimaryTreeview,
    PrimaryEntry, PrimaryLabelFrame, PrimaryButton,
    PrimaryCheckbutton
)
from utils.finance_helpers import fetch_live_rates, create_loan_chart


class BalloonLoanTab(BaseTab):
    """Ballon-Darlehen (balloon loan) calculator tab mit integriertem Chart-Fenster."""

    def __init__(self, parent, controller, event_bus):
        super().__init__(parent, event_bus)
        self.controller = controller
        self._block_sync_event = False

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # SCROLLBAR FÜR DEN GESAMTEN TAB
        self.main_scroll_container = ScrolledFrame(self, autohide=True, bootstyle="primary-round")
        self.main_scroll_container.grid(row=0, column=0, sticky="nsew")
        self.main_scroll_container.rowconfigure(0, weight=1)
        self.main_scroll_container.columnconfigure(0, weight=1)

        self.container = PrimaryFrame(self.main_scroll_container)
        self.container.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.container.columnconfigure(0, weight=1)

        # Grid Gewichtung für 3 Sektionen: Rechner, Chart, Vergleich
        self.container.rowconfigure(0, weight=0)  # Rechner oben
        self.container.rowconfigure(1, weight=0)  # Chart mitte
        self.container.rowconfigure(2, weight=1)  # Vergleich unten

        # ==========================================
        # OBERER BEREICH: SIMULATOR & ERGEBNISSE
        # ==========================================
        top_frame = PrimaryFrame(self.container)
        top_frame.grid(row=0, column=0, sticky="nsew", pady=5)
        top_frame.columnconfigure(0, weight=3)
        top_frame.columnconfigure(1, weight=7)
        top_frame.rowconfigure(0, weight=1)

        # ---------------- LINKS: Eingaben -----------------
        simulator_frame = PrimaryLabelFrame(top_frame, text="Ballon-Darlehen Simulator", bootstyle="primary")
        simulator_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.kreditsumme_var = tb.StringVar(value="350000")
        self.zinssatz_var = tb.StringVar(value="4.4")
        self.ballon_var = tb.StringVar(value="100000")  # NEU: Ziel-Endsumme
        self.laufzeit_var = tb.StringVar(value="15")
        self.einkommen_var = tb.StringVar(value="3500")
        self.eigenkapital_var = tb.StringVar(value="65000")
        self.sync_var = tb.BooleanVar(value=False)

        fields = [
            ("Kreditsumme (€)", self.kreditsumme_var),
            ("Zinssatz p.a. (%)", self.zinssatz_var),
            ("Schlussrate / Ballon (€)", self.ballon_var),
            ("Laufzeit (Jahre)", self.laufzeit_var),
            ("Netto-Einkommen (€/Monat)", self.einkommen_var),
            ("Eigenkapital (€)", self.eigenkapital_var)
        ]

        for label_text, var in fields:
            lbl = PrimaryLabel(simulator_frame, text=label_text)
            lbl.pack(anchor="w", padx=10, pady=(4, 0))
            entry = PrimaryEntry(simulator_frame, textvariable=var)
            entry.pack(fill="x", padx=10, pady=(0, 4))
            var.trace_add("write", self._broadcast_sync)

        self.chk_sync = PrimaryCheckbutton(simulator_frame, text="Eingaben synchron halten", variable=self.sync_var,
                                           bootstyle="primary-round-toggle")
        self.chk_sync.pack(anchor="w", padx=10, pady=(10, 5))

        self.btn_berechnen = PrimaryButton(simulator_frame, text="Berechnen", command=self._on_berechnen_clicked,
                                           bootstyle="primary")
        self.btn_berechnen.pack(fill="x", padx=10, pady=(5, 10))

        self.lbl_gesamtbewertung = PrimaryLabel(simulator_frame, text="Gesamtbewertung: Bitte berechnen",
                                                font=("Helvetica", 10, "bold"))
        self.lbl_gesamtbewertung.pack(anchor="w", padx=10, pady=(10, 2))

        self.lbl_status = PrimaryLabel(simulator_frame, text="Status: Bereit", font=("Helvetica", 9))
        self.lbl_status.pack(anchor="w", padx=10, pady=(2, 10))

        # ---------------- RECHTS: Text & Tabelle ----------------
        right_panel = PrimaryFrame(top_frame)
        right_panel.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        right_panel.columnconfigure(0, weight=1)
        right_panel.rowconfigure(0, weight=4)
        right_panel.rowconfigure(1, weight=6)

        ergebnis_frame = PrimaryLabelFrame(right_panel, text="Ergebnis", bootstyle="primary")
        ergebnis_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.txt_ergebnis = tb.Text(ergebnis_frame, height=5, wrap="word", font=("Helvetica", 10))
        self.txt_ergebnis.pack(fill="both", expand=True, padx=5, pady=5)
        self.txt_ergebnis.config(state="disabled")

        zahlungsplan_frame = PrimaryLabelFrame(right_panel, text="Zahlungsplan", bootstyle="primary")
        zahlungsplan_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        zahlungsplan_frame.columnconfigure(0, weight=1)
        zahlungsplan_frame.rowconfigure(0, weight=1)

        columns_plan = ("monat", "zinsen", "tilgung", "rate", "restschuld")
        self.tree_plan = PrimaryTreeview(zahlungsplan_frame, columns=columns_plan, show="headings", bootstyle="primary")
        self.tree_plan.grid(row=0, column=0, sticky="nsew", padx=(5, 0), pady=5)

        scrollbar_plan = tb.Scrollbar(zahlungsplan_frame, orient="vertical", command=self.tree_plan.yview,
                                      bootstyle="primary-vertical")
        scrollbar_plan.grid(row=0, column=1, sticky="ns", pady=5, padx=(0, 5))
        self.tree_plan.configure(yscrollcommand=scrollbar_plan.set)

        for col in columns_plan:
            self.tree_plan.heading(col, text=col.capitalize())
            self.tree_plan.column(col, anchor="center", width=95)

        # ==========================================
        # MITTLERER BEREICH: CHART / DIAGRAMM-FRAME
        # ==========================================
        self.chart_frame = PrimaryLabelFrame(self.container, text="Visueller Ratenverlauf (Zins vs. Tilgung)",
                                             bootstyle="primary")
        self.chart_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        # Platzhalter Text vor der ersten Berechnung
        lbl_placeholder = PrimaryLabel(self.chart_frame, text="Klicken Sie auf 'Berechnen', um den Verlauf anzuzeigen.",
                                       font=("Helvetica", 9, "italic"))
        lbl_placeholder.pack(pady=20)

        # ==========================================
        # UNTERER BEREICH: VERGLEICHSTABELLE
        # ==========================================
        vergleich_frame = PrimaryLabelFrame(self.container, text="Vergleich (Live Online-Angebote)",
                                            bootstyle="primary")
        vergleich_frame.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)

        columns_vergleich = ("variante", "monatsrate", "gesamtkosten", "effektivzins", "belastung")
        self.tree_vergleich = PrimaryTreeview(vergleich_frame, columns=columns_vergleich, show="headings",
                                              bootstyle="primary")
        for col in columns_vergleich:
            self.tree_vergleich.heading(col, text=col.capitalize())
            self.tree_vergleich.column(col, anchor="center", width=130)
        self.tree_vergleich.pack(fill="both", expand=True, padx=5, pady=5)

        if self.event_bus:
            self.event_bus.subscribe("global_loan_sync", self._receive_sync)

    def _broadcast_sync(self, *args):
        if self._block_sync_event or not self.sync_var.get() or not self.event_bus:
            return
        payload = {
            "kreditsumme": self.kreditsumme_var.get(), "zinssatz": self.zinssatz_var.get(),
            "laufzeit": self.laufzeit_var.get(), "einkommen": self.einkommen_var.get(),
            "eigenkapital": self.eigenkapital_var.get()
        }
        self.event_bus.publish("global_loan_sync", payload)

    def _receive_sync(self, payload):
        if not self.sync_var.get(): return
        self._block_sync_event = True
        self.kreditsumme_var.set(payload.get("kreditsumme", ""))
        self.zinssatz_var.set(payload.get("zinssatz", ""))
        self.laufzeit_var.set(payload.get("laufzeit", ""))
        self.einkommen_var.set(payload.get("einkommen", ""))
        self.eigenkapital_var.set(payload.get("eigenkapital", ""))
        self._block_sync_event = False

    def _on_berechnen_clicked(self):
        try:
            kreditsumme = float(self.kreditsumme_var.get().replace(",", "."))
            nominalzins = float(self.zinssatz_var.get().replace(",", "."))
            ballonsumme = float(self.ballon_var.get().replace(",", "."))
            laufzeit_jahre = int(self.laufzeit_var.get())
            einkommen = float(self.einkommen_var.get() or 0)
            eigenkapital = float(self.eigenkapital_var.get() or 0)

            if kreditsumme > ballonsumme and laufzeit_jahre > 0:
                self.calculate_balloon_loan(kreditsumme, nominalzins, ballonsumme, laufzeit_jahre, einkommen,
                                            eigenkapital)
        except ValueError:
            self.reset_outputs()

    def calculate_balloon_loan(self, kreditsumme, nominalzins, ballonsumme, laufzeit_jahre, einkommen, eigenkapital):
        for item in self.tree_plan.get_children(): self.tree_plan.delete(item)
        for item in self.tree_vergleich.get_children(): self.tree_vergleich.delete(item)

        laufzeit_monate = laufzeit_jahre * 12
        monatlicher_zinssatz = (nominalzins / 100) / 12

        # Formel zur Berechnung der konstanten Rate bei vorgegebener Ziel-Schlussrate (Ballon)
        q = 1 + monatlicher_zinssatz
        monatliche_rate = (kreditsumme * (q ** laufzeit_monate) - ballonsumme) * (q - 1) / ((q ** laufzeit_monate) - 1)

        restschuld = kreditsumme
        gesamt_zinsen = 0
        gesamt_tilgung = 0

        # Arrays für das Diagramm vorbereiten
        zins_liste = []
        tilgungs_liste = []

        for monat in range(1, laufzeit_monate + 1):
            zins_anteil = restschuld * monatlicher_zinssatz
            tilgungs_anteil = monatliche_rate - zins_anteil

            # Am letzten Monat wird der Ballon fällig
            if monat == laufzeit_monate:
                tilgungs_anteil = restschuld
            monatliche_rate = zins_anteil + tilgungs_anteil
            restschuld -= tilgungs_anteil
            gesamt_zinsen += zins_anteil
            gesamt_tilgung += tilgungs_anteil
            zins_liste.append(zins_anteil)
            tilgungs_liste.append(tilgungs_anteil)

            self.tree_plan.insert("", "end", values=(
                monat, f"{zins_anteil:.2f} €", f"{tilgungs_anteil:.2f} €",
                f"{monatliche_rate:.2f} €", f"{max(0.0, restschuld):.2f} €"
            ))
        # CHART LIVE ZEICHNEN
        create_loan_chart(self.chart_frame, zins_liste, tilgungs_liste)
        belastungsquote = (monatliche_rate / einkommen * 100) if einkommen > 0 else 0
        ek_quote = (eigenkapital / (kreditsumme + eigenkapital) * 100) if (kreditsumme + eigenkapital) > 0 else 0
        self.txt_ergebnis.config(state="normal")
        self.txt_ergebnis.delete("1.0", "end")
        self.txt_ergebnis.insert("1.0",
                                 f"Kreditsumme: {kreditsumme:,.2f} €\n"
                                 f"Monatliche Standardrate: {zins_liste[0] + tilgungs_liste[0]:,.2f} €\n"
                                 f"End-Schlussrate (Ballon fällig): {monatliche_rate:,.2f} €\n"
                                 f"Gesamtzinsen über Laufzeit: {gesamt_zinsen:,.2f} €\n"
                                 f"Effektivzins: {((1 + monatlicher_zinssatz) ** 12 - 1) * 100:.2f} %\n"
                                 f"Belastungsquote: {belastungsquote:.1f} %\n"
                                 )
        self.txt_ergebnis.config(state="disabled")
        # Live Online Zins-Vergleich laden
        market_base_rate = fetch_live_rates(laufzeit_jahre)
        self.tree_vergleich.insert("", "end",
                                   values=("DSL Bank (Ballon)", f"{monatliche_rate * 0.98:.2f} €", "Markt-Kondition",
                                           f"{market_base_rate:.2f} %", "Gut"))
        self.lbl_status.config(text="Status: Berechnung und Diagrammerstellung erfolgreich.")

    def reset_outputs(self):
        self.lbl_status.config(text="Status: Fehlerhafte Eingabe.")
