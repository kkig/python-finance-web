import pytest

from finance.db import get_db


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

    with app.app_context():
        client.post("/buy", data={"symbol": "nflx", "shares": "10"})
        db = get_db()
        count = db.execute("SELECT COUNT(id) FROM transactions").fetchone()[0]
        assert count == 2


@pytest.mark.parametrize(
    ("symbol", "shares", "message"),
    (
        ("", "", b"Missing symbol."),
        ("nflx", "", b"Missing shares."),
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