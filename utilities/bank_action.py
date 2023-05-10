from data.user import User


class BankAction:

    """A class for bank actions like deposit, withdraw, transfer"""

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
                    return True
                return False
            print(f"User with Bank Account {user_id} not found.")
            return False
        print(
            f"You don't have sufficient funds, Your account balance is {self.user.bank.balance}"
        )
        return False
