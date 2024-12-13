import pytest

from flask import g

from finance.db import database


def test_get_login_required(client, auth):
    """User should be logged in to access the page."""
    response = client.get("/")
    assert response.status_code == 302
    assert response.headers.get("Location") == "/auth/login"

    auth.login()
    assert client.get("/").status_code == 200


def test_get(client, auth):
    """GET /sell page should have list of user's stocks."""
    auth.login()
    response = client.get("/sell")
    assert b"NFLX" in response.data


@pytest.mark.parametrize(
    ("symbol", "shares", "message"),
    (
        ("", "", b"Symbol and number of shares are required."),
        ("NFLX", "", b"Symbol and number of shares are required."),
        ("NFLX@%", "1", b"Invalid input for symbol or number of shares."),
        ("NFLX", "1@@%", b"Invalid input for symbol or number of shares."),
        ("NFLX", "50", b"Invalid amount of shares for the symbol."),
        ("NFLX", "0", b"Invalid amount of shares for the symbol."),
    ),
)
def test_post_invalid_input(symbol, shares, message, client, auth):
    auth.login()

    response = client.post("/sell", data={"symbol": symbol, "shares": shares})

    assert response.status_code == 200
    assert message in response.data


def test_post(client, app, auth):
    auth.login()

    """POST /sell with valid input should update database."""
    with app.app_context():
        client.get("/")
        symbol = "AMZN"

        db, user_id = database(), g.user["id"]
        prev_cash = g.user["cash"]

        response = client.post("/sell", data={"symbol": symbol, "shares": "1"})

        after_count = db.execute(
            "SELECT COUNT(id) FROM transactions WHERE user_id = ?", (user_id,)
        ).fetchone()[0]

        assert prev_cash < g.user["cash"]
        assert 4 == after_count
        assert b"AMZN" not in response.data
