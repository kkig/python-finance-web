import pytest
from flask import g, session
from finance.db import get_db


def test_register(client, app):
    assert client.get("/auth/register").status_code == 200

    response = client.post(
        "/auth/register", data={"username": "a", "password": "b", "confirmation": "b"}
    )
    assert response.headers.get("Location") == "/auth/login"

    with app.app_context():
        assert (
            get_db().execute("SELECT * FROM users WHERE username = 'a'").fetchone()
            is not None
        )


@pytest.mark.parametrize(
    ("username", "password", "conf", "message"),
    (
        ("", "", "", b"Username is required."),
        ("a", "", "", b"Password is required."),
        ("a", "b", "", b"Confirmation is required."),
        ("a", "b", "c", b"Confirmation did not match with the password."),
        ("test", "test", "test", b"User test is already registered."),
    ),
)
def test_register_validate(client, username, password, conf, message):
    response = client.post(
        "/auth/register",
        data={"username": username, "password": password, "confirmation": conf},
    )

    assert response.status_code == 200
    assert message in response.data


def test_login(client, auth):
    assert client.get("/auth/login").status_code == 200

    response = auth.login()
    assert response.headers.get("Location") == "/"

    with client:
        client.get("/")
        assert session["user_id"] == 1
        assert g.user["username"] == "test"


@pytest.mark.parametrize(
    ("username", "password", "message"),
    (
        ("", "", b"Username is required."),
        ("test", "", b"Password is required."),
        ("foo", "bar", b"Invalid username and/or password."),
    ),
)
def test_login_validate(client, auth, username, password, message):
    response = auth.login(username, password)

    assert response.status_code == 200
    assert message in response.data
