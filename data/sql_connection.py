from sqlite3 import Error
import sqlite3
from typing import Any, Dict, List

class SQLConnection:

    """ Main class for SQLite Connection """

    def __init__(self, **kwargs):
        self.conn = kwargs.get("conn", None)
        self.cursor = kwargs.get("cursor", None)
        self.db_file = "bankInfo.db"
        self.table_name = None

        if self.conn is None or self.cursor is None:
            self.connect(self.db_file)

    def connect(self, db_file):
        """ create a database connection to a SQLite database """
        try:
            self.conn = sqlite3.connect(db_file)
            self.cursor = self.conn.cursor()
            return self.cursor
        except Error as error_msg:
            return "Error: " + str(error_msg)

    def check_if_table_exists(self) -> bool:
        """ A function for checking if table exists """
        if self.cursor:
            self.cursor.execute(
                f"SELECT name FROM sqlite_master WHERE type='table' AND name='{self.table_name}'"
            )
            return self.cursor.fetchone() is not None
        return False

    def create_table(self) -> bool:
        """ A function for creating table for the current object """
        return False

    def drop_table(self) -> bool:
        """ A function for dropping table for the current object """
        if self.cursor:
            self.cursor.execute(f"DROP TABLE IF EXISTS {self.table_name}")
            return True
        return False

    def get_one(self, operator="OR", **kwargs) -> Any:
        """ A function that returns one row from the table with the given condition """
        if self.cursor:
            query = f"SELECT * FROM {self.table_name} WHERE "
            for key, value in kwargs.items():
                if isinstance(value, str):
                    query += f"{key} = '{value}' {operator} "
                else:
                    query += f"{key} = {value} {operator} "

            # removes the last operator because it is not needed
            query = query[:-len(operator) - 2]
            self.cursor.execute(query)
            return self.cursor.fetchone()
        return None

    def get_all(self, operator="OR", **kwargs) -> List[Any]:
        """ A function that returns all rows from the table with the given condition """
        if self.cursor:
            query = f"SELECT * FROM {self.table_name} WHERE "
            for key, value in kwargs.items():
                if isinstance(value, str):
                    query += f"{key} = '{value}' {operator} "
                else:
                    query += f"{key} = {value} {operator} "

            # removes the last operator because it is not needed
            query = query[:-len(operator) - 2]
            self.cursor.execute(query)
            return self.cursor.fetchall()
        return []

    def insert_one(self, **kwargs) -> bool:
        """ A function that insert one data on a table """
        if self.cursor and self.conn:
            query = f"INSERT INTO {self.table_name} ("

            for key in kwargs.keys():
                query += f"{key}, "
            query = query[:-2] + ") VALUES ("

            for value in kwargs.values():
                if isinstance(value, str):
                    query += f"'{value}', "
                else:
                    query += f"{value}, "
            query = query[:-2] + ")"

            self.cursor.execute(query)
            self.conn.commit()
            return True
        return False

    def save(self, condition: Dict[str, str|int], **kwargs):
        """ A function that saves the current object to the database """
        if self.cursor and self.conn:
            query = f"UPDATE {self.table_name} SET "

            for key, value in kwargs.items():
                if isinstance(value, str):
                    query += f"{key} = '{value}', "
                else:
                    query += f"{key} = {value}, "
            query = query[:-2] + " WHERE "

            for key, value in condition.items():
                if isinstance(value, str):
                    query += f"{key} = '{value}' AND "
                else:
                    query += f"{key} = {value} AND "
            query = query[:-5]

            self.cursor.execute(query)
            self.conn.commit()
            return True
        return False

    def delete(self, **kwargs):
        """ A function that deletes the current object from the database """
        if self.cursor and self.conn:
            query = f"DELETE FROM {self.table_name} WHERE "

            for key, value in kwargs.items():
                if isinstance(value, str):
                    query += f"{key} = '{value}' AND "
                else:
                    query += f"{key} = {value} AND "
            query = query[:-5]

            self.cursor.execute(query)
            self.conn.commit()
            return True
        return False

    def __repr__(self) -> str:
        # get the first self attribute name
        attr_name = list(vars(self).keys())[4]
        if getattr(self, attr_name):
            return f"<{self.__class__.__name__} Object On {attr_name}={getattr(self, attr_name)}>"
        return f"<{self.__class__.__name__} Object>"
