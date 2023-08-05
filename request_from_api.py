import requests


def get_random_joke():
    api = "https://v2.jokeapi.dev/joke/Any?type=single"
    response = requests.get(api)
    if response.status_code == 200:
        info = response.json()
        joke = info['joke']
    return joke

def get_random_joke_id():
    api = "https://v2.jokeapi.dev/joke/Any?type=single"
    response = requests.get(api)
    if response.status_code == 200:
        info = response.json()
        id = info['id']
    return id

def get_specific_joke(id_joke):
    api = f"https://v2.jokeapi.dev/joke/Any?idRange={id_joke}"
    response = requests.get(api)
    if response.status_code == 200:
        info = response.json()
        joke = info['joke']
    return joke
