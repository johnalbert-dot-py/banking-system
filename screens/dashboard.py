from data.user import User
from utilities.bank_action import BankAction


def dashboard(user_id: int):
    """Dashboard screen for bank"""

    stop = False

    while not stop:
        user = User().get_one(id=user_id)

        if user is None:
            return

        bank_action = BankAction(user=user)

        template = f"""

    [ Bank Dashboard ]

    Account Name: {user.first_name} {user.last_name}
    Account No: {user.bank.account_no}
    Balance: {user.bank.balance:,}

    [1] Deposit
    [2] Withdraw
    [3] Transfer

        """
        print(template)
        choice = int(input("Enter choice: "))

        if choice == 1:
            bank_action.deposit()
        elif choice == 2:
            bank_action.withdraw()
        elif choice == 3:
            bank_action.transfer()
        else:
            print("Invalid choice: ", choice)
