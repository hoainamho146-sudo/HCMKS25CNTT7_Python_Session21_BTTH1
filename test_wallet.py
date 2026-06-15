"""
Unit tests for Wallet class.
"""

import unittest

from wallet import (
    Wallet,
    InvalidAmountError,
    InsufficientBalanceError
)


class TestWallet(unittest.TestCase):
    """Test cases for Wallet."""

    def setUp(self):
        """Create wallet before each test."""
        self.wallet = Wallet()

    def test_deposit_success(self):
        """Deposit should increase balance."""
        self.wallet.deposit(100000)

        self.assertEqual(
            self.wallet.balance,
            100000
        )

    def test_transfer_insufficient_balance(self):
        """
        Transfer should raise
        InsufficientBalanceError.
        """
        with self.assertRaises(
            InsufficientBalanceError
        ):
            self.wallet.transfer(
                "0987654321",
                500000
            )

    def test_invalid_amount(self):
        """
        Deposit negative amount should raise
        InvalidAmountError.
        """
        with self.assertRaises(
            InvalidAmountError
        ):
            self.wallet.deposit(-1000)


if __name__ == "__main__":
    unittest.main()
