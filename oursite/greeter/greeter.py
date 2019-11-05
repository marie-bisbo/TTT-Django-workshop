import requests
from rest_framework import status
from rest_framework.response import Response
from random import choice


def joke(search_term):
    url = "https://icanhazdadjoke.com/search"
    params = {"term": search_term}
    headers = {"Accept": "application/json"}
    request = requests.get(url, headers=headers, params=params)
    if request.json()["total_jokes"] > 0:
        api_response = choice(request.json()["results"])["joke"]
        print(api_response)
        return Response(api_response, status=status.HTTP_200_OK)
    else:
        api_response = "According to my joke API, that's just not funny."
        print(api_response)
        return Response(api_response, status=status.HTTP_200_OK)
