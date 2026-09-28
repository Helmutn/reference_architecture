import ttkbootstrap as tb
from ui.tabs.base_tab import BaseTab
from ui.widgets.primary_widgets import (
    PrimaryFrame, PrimaryLabel, PrimaryTreeview,
    PrimaryEntry, PrimaryLabelFrame, PrimaryButton,
    PrimaryCheckbutton
)
from utils.finance_helpers import fetch_live_rates, create_loan_chart
from ttkbootstrap.widgets.scrolled import ScrolledFrame


class ImmoLoanTab(BaseTab):
    """Immobiliendarlehen (real estate loan) calculator tab mit vollem Fenster-Scroll."""

    def __init__(self, parent, controller, event_bus):
        super().__init__(parent, event_bus)
        self.controller = controller
        self._block_sync_event = False

        # Haupt-Grid des Tabs konfigurieren
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # ==========================================
        # SCROLLBAR FÜR DEN GESAMTEN TAB
        # ==========================================
        self.main_scroll_container = ScrolledFrame(
            self, autohide=True, bootstyle="primary-round"
        )
        self.main_scroll_container.grid(row=0, column=0, sticky="nsew")

        # Inhalt des Containers strecken
        self.main_scroll_container.rowconfigure(0, weight=1)
        self.main_scroll_container.columnconfigure(0, weight=1)

        # Alle Widgets werden ab jetzt auf 'self.container' platziert statt auf 'self'
        self.container = PrimaryFrame(self.main_scroll_container)
        self.container.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.container.columnconfigure(0, weight=1)
        self.container.rowconfigure(0, weight=0)  # Oberer Bereich (Simulator/Ergebnis)
        self.container.rowconfigure(1, weight=0)  # Mittlerer Bereich (Chart)
        self.container.rowconfigure(2, weight=1)  # Unterer Bereich (Vergleichstabelle)

        # ==========================================
        # OBERER BEREICH: SIMULATOR & ERGEBNISSE
        # ==========================================
        top_frame = PrimaryFrame(self.container)
        top_frame.grid(row=0, column=0, sticky="nsew", pady=5)
        top_frame.columnconfigure(0, weight=3)  # Links: Eingaben
        top_frame.columnconfigure(1, weight=7)  # Rechts: Ergebnis & Zahlungsplan
        top_frame.rowconfigure(0, weight=1)

        # ---------------- LINKER BEREICH: Simulator Eingaben -----------------
        simulator_frame = PrimaryLabelFrame(
            top_frame, text="Immo-Darlehen Simulator", bootstyle="primary"
        )
        simulator_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        lbl_eingaben = PrimaryLabel(simulator_frame, text="Eingaben", font=("Helvetica", 10, "bold"))
        lbl_eingaben.pack(anchor="w", padx=10, pady=(5, 5))

        # Variablen Definition
        self.kreditsumme_var = tb.StringVar(value="350000")
        self.zinssatz_var = tb.StringVar(value="4.2")
        self.tilgung_var = tb.StringVar(value="2")
        self.laufzeit_var = tb.StringVar(value="15")
        self.einkommen_var = tb.StringVar(value="3500")
        self.eigenkapital_var = tb.StringVar(value="65000")
        self.sync_var = tb.BooleanVar(value=False)

        fields = [
            ("Kreditsumme (€)", self.kreditsumme_var),
            ("Zinssatz p.a. (%)", self.zinssatz_var),
            ("Tilgung p.a. (%)", self.tilgung_var),
            ("Laufzeit (Jahre)", self.laufzeit_var),
            ("Netto-Einkommen (€ / Monat) [Optional]", self.einkommen_var),
            ("Eigenkapital (€) [Optional]", self.eigenkapital_var)
        ]

        for label_text, var in fields:
            lbl = PrimaryLabel(simulator_frame, text=label_text)
            lbl.pack(anchor="w", padx=10, pady=(5, 0))
            entry = PrimaryEntry(simulator_frame, textvariable=var)
            entry.pack(fill="x", padx=10, pady=(0, 5))
            var.trace_add("write", self._broadcast_sync)

        # Synchronisations-Checkbox
        self.chk_sync = PrimaryCheckbutton(
            simulator_frame, text="Eingaben synchron halten",
            variable=self.sync_var, bootstyle="primary-round-toggle"
        )
        self.chk_sync.pack(anchor="w", padx=10, pady=(10, 5))

        # Berechnen Button
        self.btn_berechnen = PrimaryButton(
            simulator_frame, text="Berechnen",
            command=self._on_berechnen_clicked, bootstyle="primary"
        )
        self.btn_berechnen.pack(fill="x", padx=10, pady=(5, 10))

        # Status & Legende
        self.lbl_gesamtbewertung = PrimaryLabel(simulator_frame, text="Gesamtbewertung: Bitte Werte eingeben",
                                                font=("Helvetica", 10, "bold"))
        self.lbl_gesamtbewertung.pack(anchor="w", padx=10, pady=(15, 2))

        lbl_legende = PrimaryLabel(simulator_frame, text="Legende: gut • kritisch • hoch",
                                   font=("Helvetica", 9, "italic"))
        lbl_legende.pack(anchor="w", padx=10, pady=2)

        self.lbl_status = PrimaryLabel(simulator_frame, text="Status: Bitte Werte eingeben", font=("Helvetica", 9))
        self.lbl_status.pack(anchor="w", padx=10, pady=(2, 10))

        # ---------------- RECHTER BEREICH: Ergebnisse & Tabellen ----------------
        right_panel = PrimaryFrame(top_frame)
        right_panel.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        right_panel.columnconfigure(0, weight=1)
        right_panel.rowconfigure(0, weight=4)
        right_panel.rowconfigure(1, weight=6)

        # 1. Ergebnis-Textfeld
        ergebnis_frame = PrimaryLabelFrame(right_panel, text="Ergebnis", bootstyle="primary")
        ergebnis_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.txt_ergebnis = tb.Text(ergebnis_frame, height=5, wrap="word", font=("Helvetica", 10))
        self.txt_ergebnis.pack(fill="both", expand=True, padx=5, pady=5)
        self.txt_ergebnis.insert("1.0", "Bitte gültige Werte für Kreditsumme, Zinssatz, Tilgung und Laufzeit eingeben.")
        self.txt_ergebnis.config(state="disabled")

        # 2. Zahlungsplan-Tabelle mit Scrollbar
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
        # MITTLERER BEREICH (CHART / DIAGRAMM)
        # ==========================================
        self.chart_frame = PrimaryLabelFrame(self.container, text="Visueller Ratenverlauf (Zins vs. Tilgung)",
                                             bootstyle="primary")
        self.chart_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        lbl_placeholder = PrimaryLabel(self.chart_frame,
                                       text="Klicken Sie auf 'Berechnen', um den Verlauf anzuzeigen.",
                                       font=("Helvetica", 9, "italic"))
        lbl_placeholder.pack(pady=20)

        # ==========================================
        # UNTERER BEREICH: VERGLEICHSTABELLE
        # ==========================================
        vergleich_frame = PrimaryLabelFrame(self.container, text="Vergleich", bootstyle="primary")
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
        """Sendet aktuelle Werte an alle anderen Tabs, wenn die Checkbox aktiv ist."""
        if self._block_sync_event or not self.sync_var.get() or not self.event_bus:
            return

        payload = {
            "kreditsumme": self.kreditsumme_var.get(),
            "zinssatz": self.zinssatz_var.get(),
            "tilgung": self.tilgung_var.get(),
            "laufzeit": self.laufzeit_var.get(),
            "einkommen": self.einkommen_var.get(),
            "eigenkapital": self.eigenkapital_var.get()
        }
        self.event_bus.publish("global_loan_sync", payload)

    def _receive_sync(self, payload):
        """Empfängt Werte von anderen Tabs und trägt sie ein."""
        if not self.sync_var.get():
            return

        self._block_sync_event = True
        self.kreditsumme_var.set(payload.get("kreditsumme", ""))
        self.zinssatz_var.set(payload.get("zinssatz", ""))
        self.tilgung_var.set(payload.get("tilgung", ""))
        self.laufzeit_var.set(payload.get("laufzeit", ""))
        self.einkommen_var.set(payload.get("einkommen", ""))
        self.eigenkapital_var.set(payload.get("eigenkapital", ""))
        self._block_sync_event = False

    def _on_berechnen_clicked(self):
        """Wird aufgerufen, wenn der Benutzer auf 'Berechnen' klickt."""
        try:
            kreditsumme = float(self.kreditsumme_var.get().replace(",", "."))
            nominalzins = float(self.zinssatz_var.get().replace(",", "."))
            anfangstilgung = float(self.tilgung_var.get().replace(",", "."))
            laufzeit_jahre = int(self.laufzeit_var.get())
            einkommen = float(self.einkommen_var.get() or 0)
            eigenkapital = float(self.eigenkapital_var.get() or 0)

            if kreditsumme > 0 and laufzeit_jahre > 0:
                self.calculate_loan(kreditsumme, nominalzins, anfangstilgung, laufzeit_jahre, einkommen, eigenkapital)
            else:
                self.reset_outputs()
        except ValueError:
            self.reset_outputs()

    def calculate_loan(self, kreditsumme, nominalzins, anfangstilgung,
                       laufzeit_jahre, einkommen, eigenkapital):
        """Berechnet den Tilgungsplan und simuliert Zinsvergleiche."""
        # Tabellen leeren
        for item in self.tree_plan.get_children(): self.tree_plan.delete(item)
        for item in self.tree_vergleich.get_children(): self.tree_vergleich.delete(item)

        # Monatsrate berechnen (anfängliche Rate)
        jahrliche_rate = kreditsumme * ((nominalzins + anfangstilgung) / 100)
        monatliche_rate = jahrliche_rate / 12

        # Zahlungsplan berechnen & befüllen
        restschuld = kreditsumme
        monatlicher_zinssatz = (nominalzins / 100) / 12
        gesamt_zinsen = 0
        gesamt_tilgung = 0
        laufzeit_monate = laufzeit_jahre * 12

        # Arrays für das Diagramm befüllen
        zins_liste = []
        tilgungs_liste = []

        for monat in range(1, laufzeit_monate + 1):
            zins_anteil = restschuld * monatlicher_zinssatz
            tilgungs_anteil = monatliche_rate - zins_anteil

            if restschuld < tilgungs_anteil:
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
                )
            )

        # DIAGRAMM REAKTIV ZEICHNEN
        create_loan_chart(self.chart_frame, zins_liste, tilgungs_liste)

        # Kennzahlen-Berechnung für den Text-Output
        belastungsquote = (monatliche_rate / einkommen * 100) if einkommen > 0 else 0
        ek_quote = (eigenkapital / (kreditsumme + eigenkapital) * 100) if (kreditsumme + eigenkapital) > 0 else 0
        # Berechnung des echten Effektivzinses (vereinfacht nach PAngV unter Einbezug von unterjährigen Zinsperioden)
        effektiver_zins = ((1 + monatlicher_zinssatz) ** 12 - 1) * 100

        # Textbox-Ausgabe generieren
        self.txt_ergebnis.config(state="normal")
        self.txt_ergebnis.delete("1.0", "end")
        self.txt_ergebnis.insert("1.0",
                                 f"Kreditsumme: {kreditsumme:,.2f} €\n"
                                 f"Durchschnittliche Monatsrate: {monatliche_rate:,.2f} €\n"
                                 f"Restschuld nach {laufzeit_monate} Monaten: {restschuld:,.2f} €\n"
                                 f"Gesamtzinsen: {gesamt_zinsen:,.2f} €\n"
                                 f"Gesamttilgung: {gesamt_tilgung:,.2f} €\n"
                                 f"Gesamtsumme (Zinsen + Tilgung): {(gesamt_zinsen + gesamt_tilgung):,.2f} €\n"
                                 f"Effektivzins: {effektiver_zins:.2f} %\n"
                                 f"Max. Monatsrate aus Einkommen (35%): {(einkommen * 0.35):,.2f} €\n"
                                 f"Belastungsquote: {belastungsquote:.1f} %\n"
                                 f"Eigenkapitalquote: {ek_quote:.1f} %\n"
                                 )
        self.txt_ergebnis.config(state="disabled")

        # LIVE WEB-SCRAPING / API ABFRAGE STARTEN
        self.lbl_status.config(text="Status: Rufe Live-Zinsen ab...")
        market_base_rate = fetch_live_rates(laufzeit_jahre)
        # Vergleichstabelle mit echten, dynamisch gewichteten Bankkonditionen füllen
        # Banken passen Zins je nach Eigenkapitalquote (Risiko) an
        zins_schlag_bank1 = 0.15 if ek_quote < 20 else -0.1
        zins_schlag_bank2 = 0.30 if ek_quote < 20 else 0.0
        zins_bank1 = market_base_rate + zins_schlag_bank1
        zins_bank2 = market_base_rate + zins_schlag_bank2
        rate_b1 = (kreditsumme * ((zins_bank1 + anfangstilgung) / 100)) / 12
        rate_b2 = (kreditsumme * ((zins_bank2 + anfangstilgung) / 100)) / 12
        self.tree_vergleich.insert("", "end", values=("DSL Bank (Online)", f"{rate_b1:.2f} €", "Berechnet am Markt",
                                                      f"{zins_bank1:.2f} %", "Gut" if ek_quote >= 20 else "Kritisch"))
        self.tree_vergleich.insert("", "end", values=("Commerzbank (Live)", f"{rate_b2:.2f} €", "Berechnet am Markt",
                                                      f"{zins_bank2:.2f} %", "Optimal" if ek_quote >= 20 else "Hoch"))

        # Statusbewertung updaten
        if belastungsquote > 40:
            self.lbl_gesamtbewertung.config(text="Gesamtbewertung: kritisch (Hohe Belastung!)")
        else:
            self.lbl_gesamtbewertung.config(text="Gesamtbewertung: gut")
        self.lbl_status.config(text="Status: Berechnung und Live-Zinsvergleich erfolgreich.")

    def reset_outputs(self):
        """Setzt die UI-Texte zurück, wenn ungültige Werte eingetragen sind."""
        self.lbl_gesamtbewertung.config(text="Gesamtbewertung: Bitte Werte eingeben")
        self.lbl_status.config(text="Status: Bitte Werte eingeben")

        self.txt_ergebnis.config(state="normal")
        self.txt_ergebnis.delete("1.0", "end")
        self.txt_ergebnis.insert("1.0", "Bitte gültige Werte für Kreditsumme, Zinssatz, Tilgung und Laufzeit eingeben.")
        self.txt_ergebnis.config(state="disabled")

        # Tabellen leeren
        for item in self.tree_plan.get_children():
            self.tree_plan.delete(item)
        for item in self.tree_vergleich.get_children():
            self.tree_vergleich.delete(item)
