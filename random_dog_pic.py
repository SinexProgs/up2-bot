import json
import requests


def get_dog_image():
    response = requests.get("https://api.thedogapi.com/v1/images/search").text
    return json.loads(response)[0]["url"]