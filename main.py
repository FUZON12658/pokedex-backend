import asyncio
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from sqlalchemy.ext.asyncio import async_sessionmaker
from db import engine
from schemas import PokemonModel
from crud import CRUD
from processPokemonData import fetch_pokemon_data_in_batches, process_and_store_pokemon_data
import os

app = FastAPI(
    title="PokeApi implementation",
    description="This is the implementation of pokeapi assignment by edtraa",
    docs_url="/",
)

# Allow all origins (*), allow specific headers, and allow all methods
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Create async session
session = async_sessionmaker(bind=engine, expire_on_commit=False)

crud = CRUD()


@app.get("/v1/pokemons", response_model=List[PokemonModel], tags=["v1"])
async def getPokemons(query: str = None):
    try:
        # Fetch pokemons from the database
        pokemons = await crud.get_pokemons(session)

        if not pokemons:
            # Fetch data from the PokeAPI in batches
            pokemon_data_batches = await fetch_pokemon_data_in_batches()

            # Process the fetched Pokémon data and store it in the databaseg
            await process_and_store_pokemon_data(pokemon_data_batches, session)

            # Fetch Pokémon from the database again
            pokemons = await crud.get_pokemons(session)

        # Filter pokemons based on query
        if query:
            query = query.lower()
            pokemons = [
                pokemon
                for pokemon in pokemons
                if query in pokemon.name.lower() or query in pokemon.type.lower()
            ]

        return pokemons

    except Exception as e:
        # Log the error for debugging purposes
        print(f"An error occurred: {e}")

        pokemons = await crud.get_pokemons(session)

        # Filter pokemons based on query
        if query:
            query = query.lower()
            pokemons = [
                pokemon
                for pokemon in pokemons
                if query in pokemon.name.lower() or query in pokemon.type.lower()
            ]

        return pokemons


        

