import asyncio
import requests
import uuid
from typing import List
from models import Pokemon
from schemas import PokemonModel


async def fetch_pokemon_data():
    # Fetch data for a batch of Pokémon URLs asynchronously
    url = f"https://pokeapi.co/api/v2/pokemon?limit=10000&offset=0"
    response = await asyncio.get_event_loop().run_in_executor(None, requests.get, url)
    return response.json()

async def fetch_pokemon_data_in_batches():
    # Fetch Pokémon data for all batches asynchronously
    pokemon_data_batches = []
    pokemon_data = await fetch_pokemon_data()
    pokemon_data_batches.append(pokemon_data)
    return pokemon_data_batches

async def process_and_store_pokemon_data(pokemon_data_batches, session):
    tasks = []
    for pokemon_data_batch in pokemon_data_batches:
        for pokemon_info in pokemon_data_batch["results"]:
            pokemon_url = pokemon_info["url"]
            tasks.append(fetch_and_store_pokemon_info(pokemon_url, session))
    await asyncio.gather(*tasks)

async def fetch_and_store_pokemon_info(url, session):
    pokemon_info_response = await fetch_pokemon_data_from_url(url)
    await store_pokemon_info_in_db(pokemon_info_response, session)

async def fetch_pokemon_data_from_url(url):
    response = await asyncio.get_event_loop().run_in_executor(None, requests.get, url)
    return response.json()

async def store_pokemon_info_in_db(pokemon_info, session):
    # Extract necessary information
    pokemon_id = str(uuid.uuid4())
    name = pokemon_info["name"]
    types = "/".join([type_data["type"]["name"] for type_data in pokemon_info["types"]])
    
    # Extract image URLs from sprites
    image_urls = []
    sprites = pokemon_info["sprites"]
    for key in sprites:
        if sprites[key] is not None:  # Check if the sprite URL is not None
            if key == "front_default":
                image_urls.append(sprites[key])
            elif isinstance(sprites[key], dict) and "front_default" in sprites[key]:
                image_urls.append(sprites[key]["front_default"])
    
    # Create a PokemonModel instance
    pokemon_model = PokemonModel(id=pokemon_id, name=name, type=types, image_urls=image_urls)
    
    # Create a Pokemon object and add it to the database
    async with session() as db_session:
        db_pokemon = Pokemon(**pokemon_model.dict())
        db_session.add(db_pokemon)
        await db_session.commit()