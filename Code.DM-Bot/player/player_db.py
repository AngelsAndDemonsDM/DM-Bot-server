import logging
import os
import sqlite3


class PlayerDB:
    def __init__(self, db_name: str) -> None:
        self._setup_db(db_name)
        self._connection = sqlite3.connect("DM-Bot.Data/" + db_name)

    def _setup_db(self, db_name: str) -> None:
        if not os.path.exists("DM-Bot.Data/" + db_name):
            os.makedirs("DM-Bot.Data/" + db_name)
    
    def _create_table(self) -> None:
        """
        Creates the 'users' table in the database if such a table does not already exist.
        """
        check_table_sql = """
        SELECT name FROM sqlite_master WHERE type='table' AND name='users';
        """
        cursor = self._connection.cursor()
        cursor.execute(check_table_sql)
        result = cursor.fetchone()
        if not result:
            create_table_sql = """
            CREATE TABLE users (
                ID INTEGER PRIMARY KEY,
                DiscordID TEXT NOT NULL,
                Name TEXT,
                Data TEXT
            );
            """
            cursor.execute(create_table_sql)
            self._connection.commit()

    def __getitem__(self, discord_id: str) -> dict:
        """
        Returns information about a user by their Discord ID.

        Args:
            discord_id (str): Discord ID пользователя.

        Returns:
            dict: User information in the form of a dictionary {'Name': name, 'Data': data}.
        """
        select_sql = """
        SELECT Name, Data
        FROM users
        WHERE DiscordID = ?;
        """
        cursor = self._connection.cursor()
        cursor.execute(select_sql, (discord_id,))
        row = cursor.fetchone()
        if row:
            return {'Name': row[0], 'Data': row[1]}
        else:
            return {'Name': None, 'Data': None}

    # main class metods
    def add_member(self, discord_id: str, name: str, data) -> None:
        """
        Add a new member to the database.

        Args:
            discord_id (str): The Discord ID of the member.
            name (str): The name of the member.
            data (int): The role level of the member.
        """
        insert_sql = """
        INSERT INTO users (DiscordID, Name, Data) VALUES (?, ?, ?);
        """
        cursor = self._connection.cursor()
        cursor.execute(insert_sql, (discord_id, name, data))
        self._connection.commit()