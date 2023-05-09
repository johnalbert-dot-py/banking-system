from __future__ import annotations
from typing import List
from data.sql_connection import SQLConnection


class BankAccount(SQLConnection):

    """ BankAccount object for interacting with the BankAccount table in database """

    def __init__(self, **kwargs):
        super().__init__()
        self.account_no: int = kwargs.get("account_no", None)
        self.balance: int = kwargs.get("balance", None)
        self.table_name: str = "bank_account"

    def create_table(self) -> bool:
        """ A function for creating table for the current object """
        if self.cursor:
            self.cursor.execute(
                f"CREATE TABLE {self.table_name} ("
                "account_no integer PRIMARY KEY NOT NULL UNIQUE,"
                "balance float NOT NULL DEFAULT 0.0"
                ")"
            )
            return True
        return False

    def get_all(self, operator="OR", **kwargs) -> List[BankAccount] | List[None]:
        bank_accounts = []
        for bank_account in super().get_all(operator, **kwargs):
            bank_accounts.append(
                BankAccount(account_no=bank_account[0], balance=bank_account[1])
            )
        return bank_accounts

    def get_one(self, operator="OR", **kwargs) -> BankAccount | None:
        bank_account = super().get_one(operator, **kwargs)
        if bank_account:
            return BankAccount(account_no=bank_account[0], balance=bank_account[1])
        return None
