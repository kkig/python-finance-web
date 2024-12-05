import sqlite3

import pytest
from finance.db import get_db


def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute("SELECT 1")

    assert "closed" in str(e.value)


def test_insert_transaction(app):
    with app.app_context():
        db = get_db()
        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price)"
            "   VALUES (?, ?, ?, ?)",
            (
                1,
                "nflx",
                5,
                500.25,
            ),
        )

        count = db.execute("SELECT COUNT(id) FROM transactions").fetchone()[0]
        assert count == 2
