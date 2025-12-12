# recharge/recharge.py

from decimal import Decimal, ROUND_HALF_UP

def calculate_received_amount(amount, fee_percent=2.5, promo_bonus=0):
    """
    Calculate what the user receives after gateway/service fee and any promo bonus.

    - amount: Decimal or number, money user is paying (in currency units)
    - fee_percent: percentage charge (e.g. 2.5 for 2.5%)
    - promo_bonus: flat bonus added to user's account after fees

    Returns Decimal rounded to 2 decimals.
    """
    amt = Decimal(str(amount))
    fee = (amt * Decimal(str(fee_percent))) / Decimal("100")
    received = amt - fee + Decimal(str(promo_bonus))
    # Round to 2 decimal places Banker's / half up
    return received.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
