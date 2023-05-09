from data.user import User
from screens.dashboard import dashboard


def login():

    """ Dashboard screen for Log In """

    print("\n=== LOGIN ====\n")
    stop = False

    while not stop:
        account_no = input("Enter Account Number: ")
        pin = input("Enter PIN: ")

        user = User().get_one(bank_account_no=account_no, pin=pin)
        if user is None:
            print("Invalid username or password")
        else:
            stop = True
            return dashboard(user.id)
