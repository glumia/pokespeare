import pytest
import requests

from pokespeare.shakespeare import ShakespeareClient, ShakespeareRateLimit


def test_shakespeare_client_init():
    shakespeare_client = ShakespeareClient()

    assert isinstance(shakespeare_client._session, requests.Session)


def test_shakespearize(m_requests):
    """Check that the correct API request is made and that the return value is as
    expected."""
    text = "Some text to shakespearize."
    client = ShakespeareClient()
    expected_translation = "Shakespearized text."
    m_requests.post(
        "https://api.funtranslations.com/translate/shakespeare.json",
        json={
            "success": {"total": 1},
            "contents": {
                "translated": expected_translation,
                "text": text,
                "translation": "shakespeare",
            },
        },
    )

    translation = client.shakespearize(text)

    assert translation == expected_translation
    assert m_requests.last_request.json() == {"text": text}


def test_shakespearize_rate_limit(m_requests):
    """Check that the correct exception is raised if we hit a rate limit on the API
    service."""
    text = "Some text to shakespearize."
    client = ShakespeareClient()
    m_requests.post(
        "https://api.funtranslations.com/translate/shakespeare.json", status_code=429
    )

    with pytest.raises(ShakespeareRateLimit):
        client.shakespearize(text)
