def test_get(client, auth):
    """Redirect user to login page when not logged in."""
    assert client.get("/quote").status_code == 302

    """Return page when user logged in."""
    auth.login()
    response = client.get("/quote")

    assert response.status_code == 200


def test_post(client, auth):
    auth.login()

    """Return apology page when input is empty."""
    response = client.post("/quote", data={"qSymbol": ""})
    assert response.status_code == 200
    assert b"Symbol for quote is required." in response.data

    """Return quote to page."""
    response = client.post("/quote", data={"qSymbol": "NFLX"})
    assert response.status_code == 200
    assert b"NFLX" in response.data


def test_post_symbol(client, auth):
    auth.login()

    """Return apology page when symbol is invalid."""
    response = client.post("/quote", data={"qSymbol": "lok"})
    assert response.status_code == 200
    assert b"Invalid symbol for quote." in response.data
