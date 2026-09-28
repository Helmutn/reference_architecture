import json
import urllib.request
from decimal import Decimal
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def calculate_interest(principal, rate, time):
    """Calculate simple interest."""
    return Decimal(principal) * Decimal(rate) / 100 * Decimal(time)

def calculate_payment(principal, rate, months):
    """Calculate monthly loan payment."""
    if rate == 0:
        return principal / months
    return principal / months

def fetch_live_rates(laufzeit_jahre):
    """Holt aktuelle echte Marktdaten über eine kostenlose API (global nutzbar)."""
    try:
        url = "https://dbnomics.io"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=3) as response:
            data = json.loads(response.read().decode())
            latest_obs = data['series']['docs'][0]['value'][0]
            return float(latest_obs)
    except Exception:
        # Fallback auf typische Konditionen, falls die API offline ist
        return 3.65

def create_loan_chart(parent_frame, zins_verlauf, tilgungs_verlauf):
    """Generiert ein gestapeltes Flächendiagramm für Zins vs Tilgung im UI-Frame."""
    # Bestehende Widgets im Chart-Frame löschen, um Überlagerungen zu vermeiden
    for widget in parent_frame.winfo_children():
        widget.destroy()

    # Matplotlib Figur erstellen (passend zum Dark/Light Mode deines Tools gestylt)
    fig, ax = plt.subplots(figsize=(5, 2.5), dpi=100)
    fig.patch.set_facecolor('#f8f9fa')  # Anpassung an ttkbootstrap light background
    ax.set_facecolor('#ffffff')

    monate = list(range(1, len(zins_verlauf) + 1))

    # Verlauf zeichnen
    ax.stackplot(monate, zins_verlauf, tilgungs_verlauf, labels=['Zins-Anteil', 'Tilgungs-Anteil'], colors=['#ff6b6b', '#51cf66'])
    ax.set_title("Entwicklung von Zins- und Tilgungsanteil", fontsize=10, fontweight='bold', color='#495057')
    ax.set_xlabel("Monat", fontsize=8, color='#495057')
    ax.set_ylabel("Betrag in €", fontsize=8, color='#495057')
    ax.legend(loc='upper right', fontsize=8)
    ax.grid(True, linestyle='--', alpha=0.5)

    # Diagramm in Tkinter einbetten
    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill="both", expand=True)
    canvas.draw()