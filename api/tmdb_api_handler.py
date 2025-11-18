import requests
from utils.factory import MovieFactory
import os

class TMDbAPIHandler:
    BASE_URL = "https://api.themoviedb.org/3/search/movie"

    def __init__(self):
        self.api_key = os.getenv("TMDB_API_KEY")

    def search(self, title):
        params = {"api_key": self.api_key, "query": title}
        response = requests.get(self.BASE_URL, params=params)

        if response.status_code == 200:
            movies = response.json().get("results", [])
            return [MovieFactory.from_tmdb_json(m) for m in movies[:5]]
        else:
            print("Error contacting TMDb API.")
            return []
