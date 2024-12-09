def test_get(client, auth):
    """User should be logged in."""
    response = client.get("/")

    assert response.status_code == 302
    assert response.headers.get("Location") == "/auth/login"

    """Logged in user can access the page."""
    auth.login()
    assert client.get("/").status_code == 200


def test_stock(client, auth):
    auth.login()

    """Index page should show list of stocks the user own."""
    with client:
        response = client.get("/")

        assert b"$10,000.00" in response.data
        assert b"NFLX" in response.data


def test_no_stock(client, auth):
    auth.login("test2", "test")

    with client:
        response = client.get("/")

        assert response.status_code == 200
        assert b"NFLX" not in response.data
