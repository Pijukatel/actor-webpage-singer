import requests
import json

def generate_song(lyrics: str, api_key: str, genre: str= "Hip Hop") -> str:
    """Generate song and return generated music link"""
    api_url = "https://api.topmediai.com/v1/music"

    payload = {
        "is_auto": 0,
        "prompt": genre,
        "lyrics": lyrics}
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }

    response = requests.request("POST", api_url, json=payload, headers=headers)
    if response.status_code != 200:
        raise Exception(response.text)

    songs = json.loads(response.text)["data"]

    return songs[0]["audio_file"] # It generates multiple song versions by default. Return just the first for now.

def get_song(link: str) -> bytes:
    return requests.request("GET", link).content
