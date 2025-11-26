from services.movie_service import MovieService
from dotenv import load_dotenv
load_dotenv()

def print_header():
    print("\n==============================")
    print("        FilmScope CLI         ")
    print("==============================")
    print("A simple movie search & favorites tool\n")

def print_menu():
    print("\nPlease choose an option:")
    print(" 1) Search movies")
    print(" 2) Add a movie to favorites")
    print(" 3) View favorites")
    print(" 4) Remove a favorite")
    print(" 5) Get recommendations")
    print(" 0) Exit")

def prompt_choice():
    return input("Enter your choice: ").strip()

def display_movies(movies, show_index=True):
    if not movies:
        print("No movies found.")
        return

    for idx, m in enumerate(movies, start=1):
        prefix = f"{idx}. " if show_index else "- "
        print(f"{prefix}{m.title} ({m.release_date}) | Rating: {m.rating}")

def main():
    service = MovieService()

    print_header()

    while True:
        print_menu()
        choice = prompt_choice()
        
        if choice == "1":
            title = input("\nEnter a movie title to search: ").strip()
            if not title:
                print("Please enter a non-empty title.")
                continue

            results = service.search_movies(title)
            print(f"\nTop results for '{title}':")
            display_movies(results)

        elif choice == "2":
            title = input("\nEnter a movie title to search and save: ").strip()
            if not title:
                print("Please enter a non-empty title.")
                continue

            results = service.search_movies(title)
            if not results:
                print("No results found. Cannot save a favorite.")
                continue

            print(f"\nSearch results for '{title}':")
            display_movies(results)

            try:
                selection = int(input("\nEnter the number of the movie to save as favorite: ").strip())
                if selection < 1 or selection > len(results):
                    print("Invalid selection. No movie saved.")
                    continue
                movie = results[selection - 1]
                service.save_favorite(movie)
                print(f"Saved '{movie.title}' to favorites.")
            except ValueError:
                print("Invalid input. Please enter a number next time.")

        elif choice == "3":
            print("\nYour favorite movies:")
            favorites = service.list_favorites()

            if not favorites:
                print("You don't have any favorites yet.")
                continue

            for idx, (key, val) in enumerate(favorites.items(), start=1):
                title = val.get("title", "Unknown")
                rating = val.get("rating", "N/A")
                release = val.get("release_date", "N/A")
                print(f"{idx}. {title} ({release}) | Rating: {rating} | Key: {key}")

        elif choice == "4":
            favorites = service.list_favorites()
            if not favorites:
                print("\nYou don't have any favorites to remove.")
                continue

            print("\nYour favorite movies:")
            keys = list(favorites.keys())
            for idx, key in enumerate(keys, start=1):
                val = favorites[key]
                title = val.get("title", "Unknown")
                release = val.get("release_date", "N/A")
                print(f"{idx}. {title} ({release})")

            try:
                selection = int(input("\nEnter the number of the favorite to remove: ").strip())
                if selection < 1 or selection > len(keys):
                    print("Invalid selection. No movie removed.")
                    continue
                key_to_remove = keys[selection - 1]
                service.db.remove_favorite(key_to_remove)  # or expose a wrapper method in MovieService
                print("Favorite removed successfully.")
            except ValueError:
                print("Invalid input. Please enter a number next time.")

        elif choice == "5":
            title = input("\nEnter a movie title to base recommendations on: ").strip()
            if not title:
                print("Please enter a non-empty title.")
                continue

            print("Sort recommendations by:")
            print("  1) Rating (default)")
            print("  2) Release date (newest first)")
            strat_choice = input("Enter 1 or 2: ").strip()

            strategy = "rating"
            if strat_choice == "2":
                strategy = "date"

            recs = service.recommend(title, strategy)
            print(f"\nRecommendations for '{title}':")
            display_movies(recs, show_index=True)

            if not recs:
                print("No recommendations available. Returning to main menu.")
                continue

            try:
                selection = int(input(
                    "\nEnter the number of the movie to save as favorite,\n"
                    "or enter 0 to return to the main menu: "
                ).strip())

                if selection == 0:
                    print("Returning to main menu.")
                    continue

                if 1 <= selection <= len(recs):
                    movie = recs[selection - 1]
                    service.save_favorite(movie)
                    print(f"✅ Saved '{movie.title}' to favorites.")
                else:
                    print("Invalid selection. No movie saved.")

            except ValueError:
                print("Invalid input. Please enter a number next time.")


        elif choice == "0":
            print("\nThank you for using FilmScope. Goodbye! 👋")
            break

        else:
            print("\nInvalid option. Please choose a number from the menu.")

        input("\nPress Enter to return to the main menu...")

if __name__ == "__main__":
    main()
