import random
import statistics
import requests
import os
from config import OMDB_API_KEY


class MovieApp:
    def __init__(self, storage):
        """
        Initialize the MovieApp with the given storage.

        :param storage: An instance of a storage class that implements IStorage.
        """
        self._storage = storage


    def _command_list_movies(self):
        """
        List all movies in the storage and print their details.
        """
        movies = self._storage.list_movies()
        print(f"{len(movies)} movies in total")
        for title, details in movies.items():
            movie_name = title
            movie_rating = details.get("rating", "N/A")
            movie_year = details.get("year", "N/A")
            print(f"{movie_name} ({movie_year}): {movie_rating}")


    def _command_add_movie(self):
        """
        Prompt the user to enter a movie title, fetch details from the OMDb API,
        and save the movie details in the data structure.
        """
        movie_title = input("Enter movie title: ").strip()
        api_key = OMDB_API_KEY
        base_url = "http://www.omdbapi.com/"
        params = {
            "apikey": api_key,
            "t": movie_title
        }

        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            movie_data = response.json()
            if movie_data["Response"] == "True":
                # Handle 'N/A' value for the rating
                rating = movie_data["imdbRating"]
                if rating == "N/A":
                    rating = None  # or you can set a default value like 0.0

                self._storage.add_movie(
                    movie_data["Title"],
                    int(movie_data["Year"]),
                    float(rating) if rating is not None else 0.0,  # Use 0.0 or another default value if rating is None
                    movie_data["Poster"]
                )
                print(f"Movie '{movie_data['Title']}' added successfully!")
            else:
                print(f"Movie not found: {movie_title}")
        else:
            print(f"Error: Unable to access the OMDb API. Status code: {response.status_code}")


    def _command_delete_movie(self):
        """
        Prompt the user to enter a movie title to delete it from the storage.
        """
        movies = self._storage.list_movies()
        if not movies:
            print("No movies available to delete.")
            return

        movie_titles = list(movies.keys())
        for index, title in enumerate(movie_titles, start=1):
            print(f"{index}. {title}")

        while True:
            try:
                selected_index = int(input("Enter the number of the movie you want to delete: ")) - 1
                if selected_index < 0 or selected_index >= len(movie_titles):
                    raise IndexError

                selected_title = movie_titles[selected_index]
                self._storage.delete_movie(selected_title)
                print(f"Movie '{selected_title}' deleted successfully!")
                break
            except (ValueError, IndexError):
                print("Invalid input. Please enter a valid number corresponding to the movie.")


    def _command_update_movie(self):
        """
        Prompt the user to update the rating of an existing movie in the storage.
        """
        movies = self._storage.list_movies()
        movie_titles = list(movies.keys())
        user_input_movie_name = input("Enter name of movie you want to update: ")

        if user_input_movie_name in movie_titles:
            while True:
                try:
                    user_input_new_rating = float(input("Enter new movie rating: "))
                    self._storage.update_movie(user_input_movie_name, user_input_new_rating)
                    print("Rating successfully changed!")
                    break
                except ValueError:
                    print("Please enter a valid rating")
        else:
            print(f"Movie {user_input_movie_name} doesn't exist!")


    def _command_movie_stats(self):
        """
        Calculate and print statistics for the movies in storage,
        including average rating, median rating, and best/worst movies.
        """
        movies = self._storage.list_movies()
        # print(f"Movies: {movies}")  # Debug print

        if not movies:
            print("No movies available to calculate statistics.")
            return

        rating_list = [float(details["rating"]) for details in movies.values()]

        average_rating = sum(rating_list) / len(rating_list)
        median_rating = statistics.median(rating_list)

        best_rating = max(rating_list)
        worst_rating = min(rating_list)

        best_movies = [
            (title, details["rating"]) for title, details in movies.items()
            if float(details["rating"]) == best_rating
        ]
        worst_movies = [
            (title, details["rating"]) for title, details in movies.items()
            if float(details["rating"]) == worst_rating
        ]

        print(f"Average rating: {round(average_rating, 1)}")
        print(f"Median rating: {round(median_rating, 1)}")
        print(f"Best movie(s): {self._get_printable_string_from_tuple(best_movies)}")
        print(f"Worst movie(s): {self._get_printable_string_from_tuple(worst_movies)}")


    def _command_random_movie(self):
        """
        Pick a random movie from the storage and print its details.
        """
        movies = self._storage.list_movies()
        # print(f"Movies: {movies}")  # Debug print

        if not movies:
            print("No movies available to pick a random movie.")
            return

        # Convert dictionary items to a list of tuples
        movie_items = list(movies.items())
        random_movie_tuple = random.choice(movie_items)
        title = random_movie_tuple[0]
        details = random_movie_tuple[1]
        rating = details["rating"]
        print(f"You could watch this movie: {title}, it's rated {rating}")


    def _command_search_movie(self):
        """
        Prompt the user to search for a movie by title.
        The search is case-insensitive and matches partial titles.
        """
        movies = self._storage.list_movies()
        user_input_movie_name = input("Enter part of movie name: ").strip()

        matching_movies = {
            title: details for title, details in movies.items()
            if user_input_movie_name.lower() in title.lower()
        }

        if not matching_movies:
            print(f"No matches found for '{user_input_movie_name}'.")
            return

        all_movie_titles_with_index = [
            (i, title) for i, title in enumerate(matching_movies.keys(), start=1)
        ]
        for index, title in all_movie_titles_with_index:
            print(f"{index}. {title}")

        while True:
            try:
                selected_index = input(
                    "Enter the number of the movie you want details for (leave empty to list all): "
                ).strip()
                if selected_index == "":
                    print("Listing all matching movies:")
                    for title, details in matching_movies.items():
                        print(f"\nTitle: {title}")
                        print(f"Year: {details['year']}")
                        print(f"Rating: {details['rating']}")
                        print(f"Poster: {details.get('poster', 'N/A')}")
                    break
                else:
                    selected_index = int(selected_index) - 1
                    if selected_index < 0 or selected_index >= len(all_movie_titles_with_index):
                        raise IndexError

                    selected_title = all_movie_titles_with_index[selected_index][1]
                    selected_movie = matching_movies[selected_title]

                    print(f"\nTitle: {selected_movie['title']}")
                    print(f"Year: {selected_movie['year']}")
                    print(f"Rating: {selected_movie['rating']}")
                    print(f"Poster: {selected_movie.get('poster', 'N/A')}")
                    break
            except (ValueError, IndexError):
                print("Invalid input. Please enter a valid number corresponding to the movie.")

    def _command_movies_sorted_by_rating(self):
        """
        Print movies sorted by rating in descending order.
        """
        movies = self._storage.list_movies()
        if not movies:
            print("No movies available to sort.")
            return

        # Sort movies by rating in descending order
        movies_sorted_by_rating_list = sorted(
            movies.items(), key=lambda item: item[1]["rating"], reverse=True
        )

        for index, (title, details) in enumerate(movies_sorted_by_rating_list, start=1):
            print(f"{index}. {title} ({details['year']}): {details['rating']}")

    def _command_movies_sorted_by_year(self):
        """
        Print movies sorted by year in ascending or descending order.
        """
        movies = self._storage.list_movies()
        if not movies:
            print("No movies available to sort.")
            return

        descending_order = input("Do you want the latest movies first? (Y/N): ").strip().lower() == "y"

        # Sort movies by year
        movies_sorted_by_year_list = sorted(
            movies.items(), key=lambda item: item[1]["year"], reverse=descending_order
        )

        for index, (title, details) in enumerate(movies_sorted_by_year_list, start=1):
            print(f"{index}. {title} ({details['year']}): {details['rating']}")

    def _command_filter_movies(self):
        """
        Filter and print movies based on user-provided rating and year range.
        """
        movies = self._storage.list_movies()
        if not movies:
            print("No movies available to filter.")
            return

        min_rating_input = input("Enter minimum rating, leave blank for no filter: ").strip()
        start_year_input = input("Enter start year, leave blank for no filter: ").strip()
        end_year_input = input("Enter end year, leave blank for no filter: ").strip()

        minimum_rating = float(min_rating_input) if min_rating_input else None
        start_year = int(start_year_input) if start_year_input else None
        end_year = int(end_year_input) if end_year_input else None

        filtered_movies = {
            title: details for title, details in movies.items()
            if (minimum_rating is None or details["rating"] >= minimum_rating) and
               (start_year is None or details["year"] >= start_year) and
               (end_year is None or details["year"] <= end_year)
        }

        if not filtered_movies:
            print("No movies found matching the filters.")
            return

        for index, (title, details) in enumerate(filtered_movies.items(), start=1):
            print(f"{index}. {title} ({details['year']}): {details['rating']}")


    def _command_generate_website(self):
        """
        Generate a website with the list of movies.
        """
        template_path = os.path.join('_static', 'index_template.html')
        output_path = 'index.html'

        if not os.path.exists(template_path):
            print(f"Error: Template file not found at {template_path}")
            return

        with open(template_path, 'r') as file:
            template_content = file.read()

        template_content = template_content.replace("__TEMPLATE_TITLE__", "My Movie Collection")

        movie_grid_html = ""
        movies = self._storage.list_movies()
        for title, details in movies.items():
            movie_grid_html += f"""
            <div class="movie-item">
                <h2>{title} ({details['year']})</h2>
                <p>Rating: {details['rating']}</p>
                <img src="{details['poster']}" alt="Poster for {title}">
            </div>
            """

        template_content = template_content.replace("__TEMPLATE_MOVIE_GRID__", movie_grid_html)

        with open(output_path, 'w') as file:
            file.write(template_content)

        print("Website was generated successfully.")


    def _get_printable_string_from_tuple(self, a_list):
        """
        Convert a list of tuples into a string for printing.

        :param a_list: List of tuples.
        :return: Formatted string.
        """
        if len(a_list) > 1:
            string_to_print = ""
            for item in a_list:
                string_to_print += f"({item[0]}, {item[1]}) "
            return string_to_print
        else:
            return f"{a_list[0][0]}, {a_list[0][1]}"


    def _get_float_input(self, prompt):
        """
        Prompt the user for a float input, validate, and return the value.

        :param prompt: The input prompt message.
        :return: User's input as a float, or None if input is empty.
        """
        while True:
            user_input = input(prompt)
            if user_input == "":
                return None
            try:
                return float(user_input)
            except ValueError:
                print("Invalid, please enter a number!")


    def _get_int_input(self, prompt):
        """
        Prompt the user for an integer input, validate, and return the value.

        :param prompt: The input prompt message.
        :return: User's input as an integer, or None if input is empty.
        """
        while True:
            user_input = input(prompt)
            if user_input == "":
                return None
            try:
                return int(user_input)
            except ValueError:
                print("Invalid, please enter a valid year!")


    def _print_menu(self, function_dict):
        """
        Print the menu options for the user.

        :param function_dict: Dictionary containing the menu options and corresponding functions.
        """
        print("Menu:")
        for key, value in function_dict.items():
            print(f"{key}. {value['name']}")

    def run(self):
        """
        Run the movie app, print the menu, and handle user commands.
        """
        FUNCTION_DICTIONARY = {
            "0": {
                "function": exit,
                "name": "Exit"
            },
            "1": {
                "function": self._command_list_movies,
                "name": "List movies"
            },
            "2": {
                "function": self._command_add_movie,
                "name": "Add movie"
            },
            "3": {
                "function": self._command_delete_movie,
                "name": "Delete movie"
            },
            "4": {
                "function": self._command_update_movie,
                "name": "Update movie"
            },
            "5": {
                "function": self._command_movie_stats,
                "name": "Stats"
            },
            "6": {
                "function": self._command_random_movie,
                "name": "Random movie"
            },
            "7": {
                "function": self._command_search_movie,
                "name": "Search movie"
            },
            "8": {
                "function": self._command_movies_sorted_by_rating,
                "name": "Movies sorted by rating"
            },
            "9": {
                "function": self._command_movies_sorted_by_year,
                "name": "Movies sorted by year"
            },
            "10": {
                "function": self._command_filter_movies,
                "name": "Filter movies"
            },
            "11": {
                "function": self._command_generate_website,
                "name": "Generate website"
            }
        }
        print("--------- Welcome to my Movies Database! ---------")
        while True:
            self._storage.list_movies()
            self._print_menu(FUNCTION_DICTIONARY)
            user_choice = input("Enter Choice (0-11): ")
            if user_choice == "0":
                print("Bye bye! :>")
                FUNCTION_DICTIONARY[user_choice]["function"]()
            elif user_choice in FUNCTION_DICTIONARY:
                print()
                FUNCTION_DICTIONARY[user_choice]["function"]()
            else:
                continue
            # buffer so the menu doesn't overwrite the requested option
            input("\nPress enter to continue\n")
