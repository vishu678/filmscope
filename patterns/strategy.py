class SortStrategy:
    def sort(self, movies):
        pass

class SortByRating(SortStrategy):
    def sort(self, movies):
        return sorted(movies, key=lambda m: m.rating or 0, reverse=True)

class SortByReleaseDate(SortStrategy):
    def sort(self, movies):
        return sorted(movies, key=lambda m: m.release_date or "0", reverse=True)
