import pytest


def test_get(client, auth):
    """Redirect user to login page when not authenticated."""
    assert client.get("/buy").status_code == 302

    auth.login()
    assert client.get("/buy").status_code == 200


def test_post(client, auth):
    auth.login()

    """Post request return code 200"""
    response = client.post("/buy", data={"symbol": "nflx", "shares": "5"})
    assert response.status_code == 302
    assert response.headers.get("Location") == "/"


@pytest.mark.parametrize(
    ("symbol", "shares", "message"),
    (("", "", b"Missing symbol."), ("nflx", "", b"Missing shares.")),
)
def test_post_validates(client, auth, symbol, shares, message):
    auth.login()

    """Invalid input will render error message."""
    response = client.post("/buy", data={"symbol": symbol, "shares": shares})

    assert response.status_code == 200
    assert b"Buy" in response.data
    assert message in response.data
