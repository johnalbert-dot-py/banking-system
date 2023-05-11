from data.user import User


class BankAction:

    """
    A class for bank actions like deposit, withdraw, transfer

    Example:
        ```python
        from data.user import User
        from utilities.bank_action import BankAction

        user = User().get_one(bank_account_no="1234567890")
        bank_action = BankAction(user=user)
        bank_action.check_account_balance()
        bank_action.deposit()
        ```

    Attributes:
        user (User): The user object

    Methods:
        `get_user(account_no=None)`: A function for getting the user with updated data, if account_no is not provided, it will use the user's bank account number\n
        `check_account_balance()`: A function for checking the user's account balance\n
        `deposit()`: A function for depositing money to the user's account\n
        `withdraw()`: A function for withdrawing money from the user's account\n
        `transfer()`: A function for transferring money from the user's account to another user's account\n

    """

    def __init__(self, user: User):
        self.user = user

    def get_user(self, account_no=None) -> User | None:
        """A function for getting the user with updated data"""
        user = User().get_one(
            bank_account_no=self.user.bank_account_no if not account_no else account_no
        )
        return user

    def check_account_balance(self) -> float:
        """A function for checking the user's account balance"""
        user = self.get_user()
        print(f"Your account balance is {user.bank.balance}")
        return user.bank.balance

    def deposit(self) -> bool:
        """A function for depositing money to the user's account"""
        amount = input("Enter amount: ")
        success = self.user.bank.save(
            balance=self.user.bank.balance + int(amount),
            condition={"account_no": self.user.bank_account_no},
        )
        return success

    def withdraw(self) -> bool:
        """A function for withdrawing money from the user's account"""
        amount = input("Enter amount: ")
        current_users_balance = self.get_user().bank.balance
        if current_users_balance >= int(amount):
            success = self.user.bank.save(
                balance=current_users_balance - int(amount),
                condition={"account_no": self.user.bank_account_no},
            )
            print(f"You have successfully withdrawn {amount}")
            return success
        print(
            f"You don't have sufficient funds, Your account balance is {self.user.bank.balance}"
        )
        return False

    def transfer(self) -> bool:
        """A function for transferring money from the user's account to another user's account"""
        amount = input("Enter amount: ")
        current_users_balance = self.get_user().bank.balance
        if current_users_balance >= int(amount):
            user_id = input("Enter User Account Number: ")
            to_user = self.get_user(account_no=user_id)

            if to_user:
                # charge the current user
                success = self.user.bank.save(
                    balance=self.user.bank.balance - int(amount),
                    condition={"account_no": self.user.bank_account_no},
                )

                if success:
                    # transfer to the other user
                    to_user.bank.save(
                        balance=to_user.bank.balance + int(amount),
                        condition={"account_no": to_user.bank_account_no},
                    )
                    print(
                        f"{amount} successfully transferred to {to_user.first_name} {to_user.last_name}"
                    )
                    return True
                return False
            print(f"User with Bank Account {user_id} not found.")
            return False
        print(
            f"You don't have sufficient funds, Your account balance is {self.user.bank.balance}"
        )
        return False
