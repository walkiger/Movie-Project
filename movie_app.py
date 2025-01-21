import random
import statistics


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
        for movie in movies:
            movie_name = movie["title"]
            movie_rating = movie["rating"]
            movie_year = movie["year"]
            print(f"{movie_name} ({movie_year}): {movie_rating}")

    def _command_add_movie(self):
        """
        Prompt the user to add a new movie to the storage.
        """
        while True:
            user_input_movie_title = input("Enter a movie title: ")
            if user_input_movie_title == "":
                print("Movie name can't be empty")
            else:
                break

        try:
            while True:
                try:
                    user_input_release_year = int(input("Enter movie release year: "))
                    break
                except ValueError:
                    print("Invalid input, try again.")

            while True:
                try:
                    user_input_movie_rating = float(input("Enter movie rating (1-10): "))
                    break
                except ValueError:
                    print("Invalid input, try again.")

            user_input_movie_poster = input("Enter movie poster URL: ")

            self._storage.add_movie(user_input_movie_title, user_input_release_year, user_input_movie_rating,
                                    user_input_movie_poster)
            print(f"Movie {user_input_movie_title} successfully added")
        except Exception as e:
            print(e)

    def _command_delete_movie(self):
        """
        Prompt the user to delete a movie from the storage.
        """
        movies = self._storage.list_movies()
        movie_titles = [movie["title"] for movie in movies]
        user_input_movie_name = input("Enter name of movie you want to delete: ")

        if user_input_movie_name in movie_titles:
            self._storage.delete_movie(user_input_movie_name)
            print(f"Movie {user_input_movie_name} successfully deleted!")
        else:
            print(f"Movie {user_input_movie_name} doesn't exist!")

    def _command_update_movie(self):
        """
        Prompt the user to update the rating of an existing movie in the storage.
        """
        movies = self._storage.list_movies()
        movie_titles = [movie["title"] for movie in movies]
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
        print(f"Movies: {movies}")  # Debug print
        rating_list = [float(movie["rating"]) for movie in movies]

        if not rating_list:
            print("No movies available to calculate statistics.")
            return

        average_rating = sum(rating_list) / len(rating_list)
        median_rating = statistics.median(rating_list)

        best_rating = max(rating_list)
        worst_rating = min(rating_list)

        best_movies = [(movie["title"], movie["rating"]) for movie in movies if float(movie["rating"]) == best_rating]
        worst_movies = [(movie["title"], movie["rating"]) for movie in movies if float(movie["rating"]) == worst_rating]

        print(f"Average rating: {round(average_rating, 1)}")
        print(f"Median rating: {round(median_rating, 1)}")
        print(f"Best movie(s): {self._get_printable_string_from_tuple(best_movies)}")
        print(f"Worst movie(s): {self._get_printable_string_from_tuple(worst_movies)}")

    def _command_random_movie(self):
        """
        Pick a random movie from the storage and print its details.
        """
        movies = self._storage.list_movies()
        print(f"Movies: {movies}")  # Debug print

        if not movies:
            print("No movies available to pick a random movie.")
            return

        random_movie_dictionary = random.choice(movies)
        title = random_movie_dictionary["title"]
        rating = random_movie_dictionary["rating"]
        print(f"You could watch this movie: {title}, it's rated {rating}")


    def _command_search_movie(self):
        """
        Search for movies in the storage by a user-provided search term.
        """
        movies = self._storage.list_movies()
        user_search_term = input("Enter part of movie name: ")
        all_movie_titles_with_index = [(i, movie["title"]) for i, movie in enumerate(movies)]

        matching_movie_by_index = []
        for index, movie_title in enumerate(all_movie_titles_with_index):
            if user_search_term.lower() in str(movie_title[1]).lower():
                matching_movie_by_index.append(index)

        if len(matching_movie_by_index) == 0:
            print("Movie name not found!")
        else:
            for i, movie in enumerate(movies):
                if i in matching_movie_by_index:
                    print(f"{movie['title']} ({movie['year']}): {movie['rating']}")

    def _command_movies_sorted_by_rating(self):
        """
        List all movies sorted by their rating in descending order.
        """
        movies = self._storage.list_movies()
        movies_sorted_by_rating_list = sorted(movies, key=lambda x: x["rating"], reverse=True)
        for movie in movies_sorted_by_rating_list:
            print(f"{movie['title']} ({movie['year']}): {movie['rating']}")

    def _command_movies_sorted_by_year(self):
        """
        List all movies sorted by their release year.
        The user can choose the sorting order (ascending or descending).
        """
        movies = self._storage.list_movies()
        descending_order = False
        while True:
            user_choice = input("Do you want the latest movies first? (Y/N)\n")
            if user_choice.lower() == "y":
                descending_order = True
                break
            elif user_choice.lower() == "n":
                break
            else:
                print("Please enter 'Y' or 'N'")

        movies_sorted_by_year_list = sorted(movies, key=lambda x: x["year"], reverse=descending_order)
        for movie in movies_sorted_by_year_list:
            print(f"{movie['title']} ({movie['year']}): {movie['rating']}")

    def _command_filter_movies(self):
        """
        Filter movies based on user-provided criteria (minimum rating, start year, end year).
        """
        movies = self._storage.list_movies()
        minimum_rating = self._get_float_input("Enter minimum rating, leave blank for no filter: ")
        start_year = self._get_int_input("Enter start year, leave blank for no filter: ")
        end_year = self._get_int_input("Enter end year, leave blank for no filter: ")

        filtered_movies = []
        for movie in movies:
            if minimum_rating is not None and movie["rating"] < minimum_rating:
                continue
            if start_year is not None and movie["year"] < start_year:
                continue
            if end_year is not None and movie["year"] > end_year:
                continue
            filtered_movies.append(movie)

        if filtered_movies:
            print("Filtered movies:")
            for movie in filtered_movies:
                print(f"{movie['title']} ({movie['year']}): {movie['rating']}")
        else:
            print("\nThere are no movies with your filters applied.")

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
            }
        }
        print("--------- Welcome to my Movies Database! ---------")
        while True:
            self._storage.list_movies()
            self._print_menu(FUNCTION_DICTIONARY)
            user_choice = input("Enter Choice (0-10): ")
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
