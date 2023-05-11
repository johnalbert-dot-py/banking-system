from data.user import User
from screens.dashboard import dashboard


def sign_up():
    """Dashboard screen for Sign Up"""

    print("\n=== Sign Up ====\n")
    stop = False

    while not stop:
        first_name = input("Enter First Name: ")
        last_name = input("Enter Last Name: ")
        pin = int(input("Enter Pin (6 digit): "))

        if len(str(pin)) != 6:
            print("Pin must be 6 digits")
            continue
        else:
            user = User()
            user_created = user.insert_one(
                first_name=first_name, last_name=last_name, pin=pin
            )

            if user_created:
                print("Your account number is: ", str(user_created))
                print("User created successfully")
                stop = True
    return
