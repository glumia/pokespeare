import json
from unittest.mock import patch

import pytest
import requests

from pokespeare.pokeapi import (
    PokeAPIClient,
    Pokemon,
    PokemonNotFound,
    clean_pokemon_description,
)


def test_poke_api_client_init():
    poke_api_client = PokeAPIClient()

    assert isinstance(poke_api_client._session, requests.Session)
    assert poke_api_client._base_url == "https://pokeapi.co/api/v2"


def test_get_pokemon_specie_details(m_requests):
    """Check that the correct API request is made and that its json response is
    returned."""
    pokemon_name = "squirtle"
    expected_details = {"dummy": "json"}
    m_requests.get(
        f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_name}",
        json=expected_details,
    )
    poke_api_client = PokeAPIClient()

    details = poke_api_client.get_pokemon_specie_details(pokemon_name)

    assert details == expected_details


def test_get_pokemon_specie_details_not_found(m_requests):
    pokemon_name = "Finn"
    m_requests.get(
        f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_name}",
        status_code=404,
    )
    poke_api_client = PokeAPIClient()

    with pytest.raises(PokemonNotFound):
        poke_api_client.get_pokemon_specie_details(pokemon_name)


@pytest.mark.parametrize(
    "description, expected",
    [
        (
            "If CHARIZARD be\xad\n"
            "comes furious, the\n"
            "flame at the tip\x0cof its tail flares\n"
            "up in a whitish-\n"
            "blue color.",
            "If CHARIZARD becomes furious, the flame at the tip of its tail flares up "
            "in a whitish-blue color.",
        ),
        (
            "Breathing intense,\n"
            "hot flames, it can\n"
            "melt almost any\xad\x0cthing. Its breath\n"
            "inflicts terrible\n"
            "pain on enemies.",
            "Breathing intense, hot flames, it can melt almost anything. Its breath "
            "inflicts terrible pain on enemies.",
        ),
    ],
)
def test_clean_pokemon_description(description, expected):
    """Check that the description is cleaned up as expected."""
    clean_description = clean_pokemon_description(description)

    assert clean_description == expected


def test_pokemon_init():
    name = "squirtle"
    description = "A very cool pokemon."

    pokemon = Pokemon(name, description)

    assert pokemon.name == name
    assert pokemon.description == description


@patch("pokespeare.pokeapi.clean_pokemon_description")
@patch("pokespeare.pokeapi.poke_api_client")
def test_pokemon_query(poke_api_mock, clean_mock, jsons_path):
    """Check that pokemon's details are correctly queried from PokeAPI and that an
    instance with those info is returned."""
    name = "SquiRTLE"  # The case difference with expected_name is intentional
    with open(
        f"{jsons_path}/pokemon_specie_squirtle.json",
        "r",
    ) as fp:
        poke_api_mock.get_pokemon_specie_details.return_value = json.load(fp)
    expected_name = "squirtle"
    expected_desc = (
        "When it feels threatened, it draws its limbs inside\nits shell and sprays "
        "water from its mouth."
    )  # This is the flavor text we expect our function to choose between the
    # alternatives
    clean_mock.return_value = clean_description = "cleaned squirtle description"

    pokemon = Pokemon.query(name)

    assert isinstance(pokemon, Pokemon)
    assert pokemon.name == expected_name
    assert pokemon.description == clean_description
    poke_api_mock.get_pokemon_specie_details.assert_called_with(name)
    clean_mock.assert_called_with(expected_desc)


@patch("pokespeare.pokeapi.poke_api_client")
def test_pokemon_query_not_found(poke_api_mock):
    name = "Finn"
    poke_api_mock.get_pokemon_specie_details.side_effect = PokemonNotFound

    pokemon = Pokemon.query(name)

    assert pokemon is None
