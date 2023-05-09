from screens.login import login


if __name__ == "__main__":

    while True:
        template = """
    [ Bank App ]

    [1] Log In
    [2] Register
        """
        print(template)
        choice = input("Enter choice: ")

        if choice == "1":
            login()
        else:
            print("Invalid choice")
