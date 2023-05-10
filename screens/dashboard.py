from data.user import User


def dashboard(user_id: int):

    """Dashboard screen for bank"""

    stop = False

    while not stop:
        user = User().get_one(id=user_id)

        if user is None:
            return

        template = f"""

    [ Bank Dashboard ]

    Account Name: {user.first_name} {user.last_name}
    Account No: {user.bank.account_no}
    Balance: {user.bank.balance}

    [1] Deposit
    [2] Withdraw
    [3] Transfer

        """
        print(template)
        choice = input("Enter choice: ")
        pass
