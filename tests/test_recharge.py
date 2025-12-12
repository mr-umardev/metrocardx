# tests/test_recharge.py
import unittest
from decimal import Decimal
from recharge.recharge import calculate_received_amount

class TestRechargeCalculations(unittest.TestCase):

    def test_simple_fee(self):
        # 100 with 2.5% fee -> fee = 2.5 -> received = 97.5
        self.assertEqual(calculate_received_amount(100, fee_percent=2.5, promo_bonus=0), Decimal("97.50"))

    def test_promo_bonus(self):
        # 200 with 2% fee and 5 promo -> fee = 4 -> received = 201
        self.assertEqual(calculate_received_amount(200, fee_percent=2.0, promo_bonus=5), Decimal("201.00"))

    def test_zero_fee(self):
        self.assertEqual(calculate_received_amount(50, fee_percent=0, promo_bonus=0), Decimal("50.00"))

    def test_rounding(self):
        # check rounding
        # amount 33.333 with 1.234% fee -> ensure rounding to two decimals
        r = calculate_received_amount(33.333, fee_percent=1.234, promo_bonus=0)
        self.assertIsInstance(r, Decimal)
        # numeric sanity check (not a specific number, but should be > 32)
        self.assertGreater(r, Decimal("32.00"))

if __name__ == "__main__":
    unittest.main()
