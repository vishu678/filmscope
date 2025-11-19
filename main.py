from services.movie_service import MovieService
from dotenv import load_dotenv
load_dotenv()

def main():
    service = MovieService()

    print("\n--- FilmScope CLI ---")
    print("1. Search Movies")
    print("2. Save a Favorite")
    print("3. View Favorites")
    print("4. Recommend Movies")
    choice = input("\nChoose an option: ")

    if choice == "1":
        title = input("Enter movie title: ")
        results = service.search_movies(title)
        for m in results:
            print(f"{m.title} ({m.rating}) — {m.release_date}")

    elif choice == "2":
        title = input("Enter title to search and save: ")
        results = service.search_movies(title)
        movie = results[0]
        service.save_favorite(movie)
        print("Saved:", movie.title)

    elif choice == "3":
        favs = service.list_favorites()
        for key, val in favs.items():
            print(key, ":", val["title"])

    elif choice == "4":
        title = input("Enter movie title: ")
        strategy = input("Sort by (rating/date): ")
        results = service.recommend(title, strategy)
        for m in results:
            print(m.title, m.rating)

if __name__ == "__main__":
    main()
