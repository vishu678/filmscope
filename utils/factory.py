from models.movie import Movie

class MovieFactory:
    @staticmethod
    def from_tmdb_json(data):
        return Movie(
            movie_id=data.get("id"),
            title=data.get("title", "Unknown"),
            rating=data.get("vote_average", "N/A"),
            overview=data.get("overview", ""),
            release_date=data.get("release_date", "N/A")
        )