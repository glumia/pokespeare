from unittest.mock import Mock, patch

from pokespeare.shakespeare import ShakespeareRateLimit


@patch("pokespeare.views.pokemon.shakespeare_client")
@patch("pokespeare.views.pokemon.Pokemon")
def test_get_pokemon_description(pokemon_cls, shakespeare_mock, client):
    """Check that pokemon's name is returned and a shakespearean description of it."""
    pokemon_name = "CHARIzARD"
    pokemon = Mock(description="dummy description")
    pokemon.name = pokemon_name.lower()  # Can't assign as a param, `name` is a reserved
    # kwarg of `Mock`.
    pokemon_cls.query.return_value = pokemon
    shakespeare_mock.shakespearize.return_value = shakespearean_desc = "dummy shk desc"

    resp = client.get(f"/pokemon/{pokemon_name}")

    assert resp.get_json() == {"name": pokemon.name, "description": shakespearean_desc}
    pokemon_cls.query.assert_called_with(pokemon_name)
    shakespeare_mock.shakespearize.assert_called_with(pokemon.description)


@patch("pokespeare.views.pokemon.Pokemon")
def test_get_pokemon_description_not_found(pokemon_cls, client):
    pokemon_name = "Finn"
    pokemon_cls.query.return_value = None

    resp = client.get(f"/pokemon/{pokemon_name}")

    assert resp.status_code == 404
    assert resp.get_json()["detail"] == "Not found"


@patch("pokespeare.views.pokemon.shakespeare_client")
@patch("pokespeare.views.pokemon.Pokemon")
def test_get_pokemon_description_rate_limit(pokemon_cls, shakespeare_mock, client):
    """Check that in case of rate limit of the shakespearean translations service we
    don't implode and instead return a meaningful error."""
    pokemon_name = "squirtle"
    pokemon = Mock(name="squirtle", description="A short and concise description.")
    pokemon_cls.query.return_value = pokemon
    shakespeare_mock.shakespearize.side_effect = ShakespeareRateLimit

    resp = client.get(f"/pokemon/{pokemon_name}")

    assert resp.status_code == 503
    assert resp.get_json()["detail"] == (
        "Sorry our server hit the rate limit on partner's shakespearean translations "
        "service, try again later."
    )
