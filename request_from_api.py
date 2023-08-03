import requests


def get_random_joke():
    api = "https://v2.jokeapi.dev/joke/Any?type=single"
    response = requests.get(api)
    if response.status_code == 200:
        info = response.json()
        joke = info['joke']
    return joke