import requests
from typing import Optional

JOKE_API_BASE_URL = "https://v2.jokeapi.dev/joke/Any?"


def fetch_joke(api_url: str, data_key: str) -> Optional[str]:
    """ Fetches a joke from the JokeAPI and extracts the data specified by the data_key. """
    response = requests.get(api_url)
    if response.status_code == 200:
        joke_data = response.json()
        return joke_data.get(data_key)
    return None

def get_random_joke() -> Optional[str]:
    """ Fetches a random joke from the JokeAPI. """
    return fetch_joke(f"{JOKE_API_BASE_URL}type=single", 'joke')

def get_random_joke_id() -> Optional[str]:
    """ Fetches a random joke ID from the JokeAPI. """
    return fetch_joke(f"{JOKE_API_BASE_URL}type=single", 'id')

def get_specific_joke(joke_id: int) -> Optional[str]:
    """ Fetches a specific joke from the JokeAPI based on the joke_id. """
    specific_joke_api = f"{JOKE_API_BASE_URL}idRange={joke_id}"
    return fetch_joke(specific_joke_api, 'joke')
