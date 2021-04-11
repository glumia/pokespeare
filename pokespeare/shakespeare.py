"""Utilities to interact with the shakespearean translation API service."""
from requests import Session


class ShakespeareRateLimit(Exception):
    pass


class ShakespeareClient:
    def __init__(self):
        self._session = Session()

    def shakespearize(self, text):
        """Get a shakespearean version of the provided text.

        :param text: a string with some text.
        :return: a string with the shakespearean translation of the provided text.
        :raises ShakespeareRateLimit: if we hit the rate limit on funtranslations.com
            APIs.
        """
        resp = self._session.post(
            "https://api.funtranslations.com/translate/shakespeare.json",
            json={"text": text},
        )
        if resp.status_code == 429:
            raise ShakespeareRateLimit
        return resp.json()["contents"]["translated"]


shakespeare_client = ShakespeareClient()
