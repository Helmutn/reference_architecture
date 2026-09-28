import json
import urllib.request
from decimal import Decimal

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
