def test_ping(client):
    """Check that the flask application works as expected and that the '/ping' view was
    registered."""
    resp = client.get("/ping")

    assert resp.data == b"pong"
