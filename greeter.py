import requests
from random import choice


def joke(search_term):
    url = "https://icanhazdadjoke.com/search"
    params = {"term": search_term}
    headers = {"Accept": "application/json"}
    request = requests.get(url, headers=headers, params=params)
    if request.json()["total_jokes"] > 0:
        response = choice(request.json()["results"])["joke"]
        print(response)
    else:
        response = "According to my joke API, that's just not funny."
        print(response)
