from flask import Blueprint

from pokespeare.pokeapi import Pokemon
from pokespeare.shakespeare import ShakespeareRateLimit, shakespeare_client

bp = Blueprint("pokemon", __name__, url_prefix="/pokemon")


@bp.route("/<pokemon_name>")
def get_pokemon_description(pokemon_name):
    pokemon = Pokemon.query(pokemon_name)
    if pokemon is None:
        return {"detail": "Not found"}, 404
    try:
        return {
            "name": pokemon.name,
            "description": shakespeare_client.shakespearize(pokemon.description),
        }
    except ShakespeareRateLimit:
        return {
            "detail": "Sorry our server hit the rate limit on partner's "
            "shakespearean translations service, try again later."
        }, 503
