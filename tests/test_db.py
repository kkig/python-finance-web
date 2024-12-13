import sqlite3

import pytest
from finance.db import database, get_db, DB


def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute("SELECT 1")

    assert "closed" in str(e.value)


def test_caller(app):
    """Caller should return BD's methods when valid key is passed"""
    with app.app_context():
        db = database()
        res = db.get("shares", 1)

    assert res is not None

    """Caller should return None when invalid key is passed."""
    with app.app_context():
        db = database()
        res = db.get("date", 1)

    assert res is None


class TestTrans:
    def test_insert_trans(self, app):
        with app.app_context():
            db = database()
            count = db.execute("SELECT COUNT(id) FROM transactions").fetchone()[0]
            data = {"id": 1, "symbol": "nflx", "shares": 5, "price": 500.25}
            db.insert("trans", **data)

            count_new = db.execute("SELECT COUNT(id) FROM transactions").fetchone()[0]
            assert count_new == count + 1

    def test_get_shares(self, app):
        with app.app_context():
            db = database()
            stocks = db.get("shares", 1)
        assert stocks[1]["symbol"] == "NFLX"
        assert stocks[1]["shares"] == 6

    def test_get_shares_none(self, app):
        with app.app_context():
            db = DB()
            stock = db.get_shares(1)
        assert stock is not None


class TestUsers:
    def test_get_user(self, app):
        with app.app_context():
            db = database()
            user = db.get("user", 1)

            assert user["username"] == "test"

    def test_get_cash(self, app):
        """Should return ther cash user has."""
        with app.app_context():
            db = database()
            cash = db.get("cash", 1)

        assert cash == 10000.00

    def test_get_cash_invalid_user(self, app):
        """Invalid user_id should return None."""
        with app.app_context():
            db = database()
            cash = db.get("cash", 10)

        assert cash is None

    def test_update_cash(self, app):
        with app.app_context():
            db, id = database(), 1
            prev = db.get("cash", id)
            db.update("cash", 1, 500)

            new = db.get("cash", id)

        assert new != prev
