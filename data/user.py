from __future__ import annotations
from typing import List
from data.sql_connection import SQLConnection
from data.bank_account import BankAccount
from utilities.generators import id_generator


class User(SQLConnection):

    """User object for interacting with the User table in database"""

    def __init__(self, **kwargs):
        super().__init__()
        self.id: int = kwargs.get("id", None)  # pylint: disable=invalid-name
        self.first_name: str = kwargs.get("first_name", None)
        self.last_name: str = kwargs.get("last_name", None)
        self.pin: int = kwargs.get("pin", None)
        self.bank_account_no: int = kwargs.get("bank_account_no", None)
        self.bank: BankAccount = kwargs.get("bank", None)

        self.table_name = "user"

    def create_table(self) -> bool:
        """A function for creating table for the current object"""
        if self.cursor:
            self.cursor.execute(
                f"CREATE TABLE {self.table_name} ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,"
                "first_name varchar(255) NOT NULL,"
                "last_name varchar(255) NOT NULL,"
                "pin integer(6) NOT NULL,"
                "bank_account_no integer NOT NULL UNIQUE,"
                "FOREIGN KEY (bank_account_no) REFERENCES bank_account(account_no)"
                ")"
            )
            return True
        return False

    def insert_one(
        self, first_name: str, last_name: str, pin: int
    ):  # pylint: disable=arguments-differ
        """A function that insert one data on a table"""
        bank_account_no = id_generator()
        bank_account = BankAccount(conn=self.conn, cursor=self.cursor)

        # check if bank account number already exists
        while bank_account.get_one(account_no=bank_account_no):
            bank_account_no = id_generator()

        bank_account.insert_one(account_no=bank_account_no)
        super().insert_one(
            first_name=first_name,
            last_name=last_name,
            pin=pin,
            bank_account_no=bank_account_no,
        )
        return bank_account_no

    def get_all(self, operator="OR", **kwargs) -> List[User] | List[None]:
        users = []
        bank_account = BankAccount()
        for user in super().get_all(operator, **kwargs):
            bank_account_for_user = bank_account.get_one(account_no=user[4])
            if bank_account_for_user:
                users.append(
                    User(
                        id=user[0],
                        first_name=user[1],
                        last_name=user[2],
                        pin=user[3],
                        bank_account_no=user[4],
                        bank=BankAccount(
                            account_no=bank_account_for_user.account_no,
                            balance=bank_account_for_user.balance,
                        ),
                    )
                )
        return users

    def get_one(self, operator="OR", **kwargs) -> User | None:
        user = super().get_one(operator, **kwargs)
        if user:
            bank_account = BankAccount()
            bank_account_for_user = bank_account.get_one(account_no=user[4])
            if bank_account_for_user:
                return User(
                    id=user[0],
                    first_name=user[1],
                    last_name=user[2],
                    pin=user[3],
                    bank_account_no=user[4],
                    bank=BankAccount(
                        account_no=bank_account_for_user.account_no,
                        balance=bank_account_for_user.balance,
                    ),
                )
        return None
