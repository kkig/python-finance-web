import pytest
from flask import g, session
from finance.db import get_db


def test_register(client, app):
    assert client.get("/auth/register").status_code == 200

    # response = client.post(
    #     "/auth/register", data={"username":}
    # )
