import pytest
from flask import g

from finance.db import database
from finance.stock import get_stock_total


def test_get_login_required(client, auth):
    """User should be logged in to send GET request"""
    response = client.get("/buy")
    assert response.status_code == 302
    assert response.headers.get("Location") == "/auth/login"


def test_post_login_required(client):
    """User should be logged in to send POST request"""
    response = client.post("/buy", data={"symbol": "nflx", "shares": "5"})
    assert response.status_code == 302
    assert response.headers.get("Location") == "/auth/login"


def test_get(client, auth):
    """Logged in user can access the page"""
    auth.login()
    response = client.get("/buy")
    assert response.status_code == 200


def test_post(app, client, auth):
    """Post request with valid data return index page"""
    auth.login()
    response = client.post("/buy", data={"symbol": "nflx", "shares": "5"})
    assert response.status_code == 302
    assert response.headers.get("Location") == "/"


def test_post_insert(app, client, auth):
    """Post request with valid data should add data to database"""
    auth.login()
    client.post("/buy", data={"symbol": "nflx", "shares": "10"})

    with app.app_context():
        db = database()
        count = db.execute(
            "SELECT COUNT(id) FROM transactions WHERE user_id = ?", (1,)
        ).fetchone()[0]

        assert count == 4


@pytest.mark.parametrize(
    ("symbol", "shares", "message"),
    (
        ("", "", b"Symbol and shares are required."),
        ("nflx", "", b"Symbol and shares are required."),
        ("lok", "3", b"Invalid symbol."),
        ("nflx", "-5", b"Invalid value for shares."),
    ),
)
def test_post_validates(client, auth, symbol, shares, message):
    auth.login()

    """Invalid input will render error message."""
    response = client.post("/buy", data={"symbol": symbol, "shares": shares})

    assert response.status_code == 200
    assert b"Buy" in response.data
    assert message in response.data


def test_get_stock_total(app, auth):
    with app.app_context():
        auth.login()
        data = get_stock_total(1)
        stocks = data["stocks"]
        amzn = stocks[0]

        assert amzn["symbol"] == "amzn"
        assert amzn["shares"] == 5
        assert data["total"] is not None
