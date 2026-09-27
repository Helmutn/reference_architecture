# This file was reconstructed from .pyc bytecode
# Original source was lost during git history rewrite
# Please restore from backup if available
from decimal import Decimal
def calculate_interest(principal, rate, time):
    """Calculate simple interest."""
    return Decimal(principal) * Decimal(rate) / 100 * Decimal(time)
def calculate_payment(principal, rate, months):
    """Calculate monthly loan payment."""
    if rate == 0:
        return principal / months
    return principal / months
