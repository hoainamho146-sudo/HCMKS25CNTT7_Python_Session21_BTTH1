"""
MoMo Wallet Simulation System.

This module provides a CLI-based wallet application with:
- Deposit
- Transfer
- Balance checking
- Logging
- Exception handling
"""

import logging
import re


logging.basicConfig(
    filename="momo_transactions.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class InvalidAmountError(Exception):
    """Raised when transaction amount is invalid."""


class InsufficientBalanceError(Exception):
    """Raised when balance is insufficient."""


class Wallet:
    """Represents a MoMo wallet."""

    HIGH_VALUE_THRESHOLD = 10_000_000

    def __init__(self):
        """Initialize wallet with zero balance."""
        self.balance = 0

    def deposit(self, amount):
        """
        Deposit money into wallet.

        Args:
            amount (int): Deposit amount.

        Raises:
            InvalidAmountError: If amount <= 0.
        """
        if amount <= 0:
            raise InvalidAmountError(
                f"Attempted to process {amount} VND."
            )

        self.balance += amount

        logging.info(
            "Deposit successful: +%s VND. Current Balance: %s",
            amount,
            self.balance
        )

    def transfer(self, phone_number, amount):
        """
        Transfer money to another user.

        Args:
            phone_number (str): Receiver phone number.
            amount (int): Transfer amount.

        Raises:
            InvalidAmountError: If amount <= 0.
            InsufficientBalanceError: If balance is insufficient.
        """
        if amount <= 0:
            raise InvalidAmountError(
                f"Attempted to process {amount} VND."
            )

        if amount > self.balance:
            raise InsufficientBalanceError(
                f"Attempted to transfer {amount} VND "
                f"with balance {self.balance} VND."
            )

        if amount >= self.HIGH_VALUE_THRESHOLD:
            logging.warning(
                "High value transaction detected: %s VND to %s",
                amount,
                phone_number
            )

        self.balance -= amount

        logging.info(
            "Transfer successful: -%s VND to %s. "
            "Current Balance: %s",
            amount,
            phone_number,
            self.balance
        )

    def get_balance(self):
        """
        Return current balance.

        Returns:
            int: Current balance.
        """
        logging.info(
            "Balance checked. Current Balance: %s",
            self.balance
        )

        return self.balance


def format_currency(amount):
    """
    Format currency with comma separator.

    Args:
        amount (int): Money amount.

    Returns:
        str: Formatted string.
    """
    return f"{amount:,}"


def validate_phone_number(phone_number):
    """
    Validate Vietnamese phone number.

    Args:
        phone_number (str): Phone number.

    Returns:
        bool: Validation result.
    """
    return bool(re.fullmatch(r"\d{10}", phone_number))


def display_menu():
    """Display application menu."""
    print("\n========== VÍ MOMO GIẢ LẬP ==========")
    print("1. Nạp tiền vào ví")
    print("2. Chuyển tiền")
    print("3. Xem số dư hiện tại")
    print("4. Thoát chương trình")
    print("=====================================")


def deposit_menu(wallet):
    """
    Handle deposit operation.

    Args:
        wallet (Wallet): Wallet object.
    """
    print("\n--- NẠP TIỀN VÀO VÍ ---")

    while True:
        try:
            amount = int(input("Nhập số tiền cần nạp: "))

            wallet.deposit(amount)

            print(
                f"\nNạp tiền thành công: "
                f"+{format_currency(amount)} VND"
            )

            print(
                f"Số dư hiện tại: "
                f"{format_currency(wallet.balance)} VND"
            )
            break

        except ValueError:
            print("Lỗi: Vui lòng nhập số tiền hợp lệ.")

            logging.error(
                "ValueError: Invalid numeric input for deposit."
            )

        except InvalidAmountError as error:
            print("Lỗi: Số tiền giao dịch phải lớn hơn 0.")

            logging.error(
                "InvalidAmountError: %s",
                error
            )
            break


def transfer_menu(wallet):
    """
    Handle transfer operation.

    Args:
        wallet (Wallet): Wallet object.
    """
    print("\n--- CHUYỂN TIỀN ---")

    phone_number = input(
        "Nhập số điện thoại người nhận: "
    )

    if not validate_phone_number(phone_number):
        print("Lỗi: Số điện thoại phải gồm đúng 10 chữ số.")
        return

    try:
        amount = int(
            input("Nhập số tiền cần chuyển: ")
        )

        wallet.transfer(phone_number, amount)

        print(
            f"\nChuyển tiền thành công tới "
            f"số điện thoại {phone_number}."
        )

        print(
            f"Số tiền đã chuyển: "
            f"{format_currency(amount)} VND"
        )

        print(
            f"Số dư còn lại: "
            f"{format_currency(wallet.balance)} VND"
        )

    except ValueError:
        print("Lỗi: Vui lòng nhập số tiền hợp lệ.")

        logging.error(
            "ValueError: Invalid numeric input "
            "for transfer."
        )

    except InvalidAmountError as error:
        print("Lỗi: Số tiền giao dịch phải lớn hơn 0.")

        logging.error(
            "InvalidAmountError: %s",
            error
        )

    except InsufficientBalanceError as error:
        print(
            "\nGiao dịch thất bại: "
            "Số dư của bạn không đủ."
        )

        print(
            f"Số dư hiện tại: "
            f"{format_currency(wallet.balance)} VND"
        )

        logging.error(
            "InsufficientBalanceError: %s",
            error
        )


def show_balance(wallet):
    """
    Display wallet balance.

    Args:
        wallet (Wallet): Wallet object.
    """
    balance = wallet.get_balance()

    print("\n--- SỐ DƯ VÍ MOMO ---")

    print(
        f"Số dư hiện tại: "
        f"{format_currency(balance)} VND"
    )


def main():
    """Run application."""
    wallet = Wallet()

    while True:
        display_menu()

        choice = input(
            "\nChọn chức năng (1-4): "
        )

        if choice == "1":
            deposit_menu(wallet)

        elif choice == "2":
            transfer_menu(wallet)

        elif choice == "3":
            show_balance(wallet)

        elif choice == "4":
            print(
                "\nCảm ơn bạn đã sử dụng dịch vụ."
            )

            logging.info("System shutdown")
            break

        else:
            print(
                "Lựa chọn không hợp lệ. "
                "Vui lòng thử lại."
            )


if __name__ == "__main__":
    main()
