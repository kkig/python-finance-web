import sqlite3
from datetime import datetime

from flask import current_app, g


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


# Function to register close_db to app
def init_app(app):
    app.teardown_appcontext(close_db)


sqlite3.register_converter("timestamp", lambda v: datetime.fromisoformat(v.decode()))


class DB:
    def __init__(self):
        self._db = get_db()

    def execute(self, *args):
        return self._db.execute(*args)

    def commit(self):
        self._db.commit()

    def insert_trans(self, id, symbol, shares, price):
        """Insert data to transaction table.
        :param id: int - id of user making transaction
        :param symbol: str - symbol of stock
        :param shares: int - number of shares
        :param price: float - price of the stock
        """
        self.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price)"
            "   VALUES (?, ?, ?, ?)",
            (
                id,
                symbol.upper(),
                shares,
                price,
            ),
        )
        self.commit()

    def get_user(self, user_id):
        """Get user information."""
        return self.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()

    def get_shares(self, id):
        """Get counts of stock per symbol.

        :param id: id of user who made transactions
        :return: sum of shares by symbol in a list
        """
        records = self.execute(
            "SELECT SUM(shares) as [total_shares], symbol FROM transactions"
            "   WHERE user_id = ? GROUP BY symbol",
            (id,),
        ).fetchall()

        return [
            {"shares": stock["total_shares"], "symbol": stock["symbol"]}
            for stock in records
        ]

    def get_cash(self, id):
        """Get cash of the user.

        :param id: int - id of user
        :return: float - cash of the user
        """
        cash = self.execute(
            "SELECT cash FROM users WHERE id = ?",
            (id,),
        ).fetchone()
        return cash[0] if cash else None

    def update_cash(self, id, cash):
        """Update cash of the user.

        :params id: int - id of the user
        :params cash: float - new cash value of the user
        :return: None
        """
        self.execute("UPDATE users SET cash = ? WHERE id = ?", (cash, id))
        self.commit()


class Caller:
    def __init__(self):
        self.db = DB()

    def execute(self, *args):
        return self.db.execute(*args)

    def get(self, key, *args):
        res = None
        try:
            if key == "user":
                res = self.db.get_user(*args)
            elif key == "shares":
                res = self.db.get_shares(*args)
            elif key == "cash":
                res = self.db.get_cash(*args)
        except sqlite3.Error as e:
            print(e)
        return res

    def insert(self, table, **kwargs):
        try:
            if table == "trans":
                self.db.insert_trans(**kwargs)
                self.db.commit()
        except sqlite3.Error as e:
            print(e)

    def update(self, key, *args):
        try:
            if key == "cash":
                self.db.update_cash(*args)
                self.db.commit()
        except sqlite3.Error as e:
            print(e)


def database():
    return Caller()
