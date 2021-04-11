"""Utilities to interact with PokeAPI."""
from requests import Session


class PokemonNotFound(Exception):
    pass


class PokeAPIClient:
    def __init__(self):
        self._session = Session()
        self._base_url = "https://pokeapi.co/api/v2"

    def get_pokemon_specie_details(self, pokemon_name):
        """Get pokemon's specie details.

        :param pokemon_name: pokemon's name.
        :return: a dict with the details about pokemon's specie. Check
            https://pokeapi.co/docs/v2#pokemon-species for the details about its
            structure.
        :raises PokemonNotFound: if the pokemon is not found on PokeAPI.
        """
        pokemon_name = pokemon_name.lower()  # PokeAPI is case sensitive
        resp = self._session.get(self._base_url + f"/pokemon-species/{pokemon_name}")
        if resp.status_code == 404:
            raise PokemonNotFound
        return resp.json()


poke_api_client = PokeAPIClient()


def clean_pokemon_description(description):
    """Remove odd character sequences from the provided string.

    :param description: the description to clean.
    :return: the cleaned up description.
    """
    return (
        description.replace("\xad\n", "")
        .replace("\xad\x0c", "")
        .replace("\x0c", " ")
        .replace("-\n", "-")
        .replace("\n", " ")
    )


class Pokemon:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    @classmethod
    def query(cls, pokemon_name):
        """Query pokemon on PokeAPI.

        :param pokemon_name: pokemon's name.
        :return: an instance of this class if a pokemon with this name is found on
            PokeAPI, `None` otherwise.
        """
        try:
            pokemon_details = poke_api_client.get_pokemon_specie_details(pokemon_name)
        except PokemonNotFound:
            return None

        name = pokemon_details["name"]

        descriptions = [
            d["flavor_text"]
            for d in pokemon_details["flavor_text_entries"]
            if d["language"]["name"] == "en"
        ]
        # We choose exactly one of the descriptions and not a random one to allow
        # clients to cache our responses.
        description = clean_pokemon_description(descriptions[-1])

        return cls(name, description)
