from api.tmdb_api_handler import TMDbAPIHandler
from database.firebase_manager import FirebaseManager
from patterns.strategy import SortByRating, SortByReleaseDate

class MovieService:
    def __init__(self):
        self.api = TMDbAPIHandler()
        self.db = FirebaseManager()

    def search_movies(self, title):
        return self.api.search(title)

    def save_favorite(self, movie):
        self.db.add_favorite(movie)

    def list_favorites(self):
        return self.db.get_favorites()

    def recommend(self, title, strategy="rating"):
        movies = self.api.search(title)

        if strategy == "date":
            sorter = SortByReleaseDate()
        else:
            sorter = SortByRating()

        return sorter.sort(movies)
