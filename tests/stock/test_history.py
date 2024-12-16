def test_get(client, auth):
    """User should be logged in to access the page."""
    response = client.get("/history")
    assert response.status_code == 302
    assert response.headers.get("Location") == "/auth/login"

    auth.login()
    assert client.get("/history").status_code == 200


def test_stock(client, auth):
    """The page should show transactions of the user made."""
    auth.login()

    response = client.get("/history")
    assert b"Transacted" in response.data
    assert b"2018-01-01 00:00:00" in response.data
