import movie_storage, statistics, random


def list_movies():
    """
    Gets data from movie_storage.get_movies_data() and prints out
    all the movies currently existing in movie_database.json
    """
    movies = movie_storage.get_movies_data()
    print(f"{len(movies)} movies in total")
    for movie in movies:
        movie_name = movie["title"]
        movie_rating = movie["rating"]
        movie_year = movie["year"]
        print(f"{movie_name} ({movie_year}): {movie_rating}")


def add_movie():
    """
    Asks user for multiple inputs, checks if they are valid.
    If not user is prompted to type again until its valid.
    Then the inputs get parsed to movie_storage.write_movie_data()
    """
    while True:
        user_input_movie_title = input("Enter a movie Title: ")
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
    except Exception as e:
        print(e)

    movie_storage.write_movie_data(user_input_movie_title, user_input_release_year, user_input_movie_rating)
    print(f"Movie {user_input_movie_title} successfully added")


def delete_movie():
    """
    Asks user for movie to delete.
    Then parses the string to movie_storage.delete_movie_data()
    If movie doesn't exist it lets the user know.
    """
    movies = movie_storage.get_movies_data()
    movie_titles = [movie["title"] for movie in movies]
    user_input_movie_name = input("Enter name of movie you want to delete: ")

    if user_input_movie_name in movie_titles:
        movie_storage.delete_movie_data(user_input_movie_name)
        print(f"Movie {user_input_movie_name} successfully deleted!")
    else:
        print(f"Movie {user_input_movie_name} doesn't exist!")


def update_movie():
    """
    Asks user for movie name to update.
    If movie exist in database user is prompted to enter a new rating.
    If movie doesn't exist prints an error message.
    """
    movies = movie_storage.get_movies_data()
    movie_titles = [movie["title"] for movie in movies]
    user_input_movie_name = input("Enter name of movie you want to update: ")

    if user_input_movie_name in movie_titles:
        while True:
            try:
                user_input_new_rating = float(input("Enter new movie rating: "))
                movie_storage.update_movie_data(user_input_movie_name, user_input_new_rating)
                print("rating successfully changed!")
                break
            except ValueError:
                print("Please enter a valid rating")
    else:
        print(f"Movie {user_input_movie_name} doesn't exist!")


def movie_stats():
    """
    Calls list_movies function to get all data and prints the average, median rating.
    Also identifies the worst and best movies and saves them to a list.
    Then parses both lists to print_list_of_tuple function to get a printable string.
    """
    movies = movie_storage.get_movies_data()
    rating_list = [float(movie["rating"]) for movie in movies]

    average_rating = sum(rating_list) / len(rating_list)
    median_rating = statistics.median(rating_list)

    best_rating = max(rating_list)
    worst_rating = min(rating_list)

    best_movies = [(movie["title"], movie["rating"]) for movie in movies if float(movie["rating"]) == best_rating]
    worst_movies = [(movie["title"], movie["rating"]) for movie in movies if float(movie["rating"]) == worst_rating]

    print(f"Average rating: {round(average_rating, 1)}")
    print(f"Median ratinig: {round(median_rating, 1)}")
    print(f"Best movie(s): {get_printable_string_from_tuple(best_movies)}")
    print(f"Worst movie(s): {get_printable_string_from_tuple(worst_movies)}")


def random_movie():
    """
    uses the random module to get a pseudo-random entry from the movies list and prints it.
    """
    movies = movie_storage.get_movies_data()
    random_movie_dictionary = random.choice(movies)
    title = random_movie_dictionary["title"]
    rating = random_movie_dictionary["rating"]
    print(f"You could watch this movie: {title}, it\'s rated {rating}")


def search_movie():
    """
    Gets movies data from movie_storage.get_movies_data() and asks user to enter part
    of a movie name.
    Creates a list of tuples to save all movies and their index in a list of tuples.
    Then iterates over the created list and checks if user search term is part of any movie name,
    if that's the case it saves this movies index in a different list.
    At the end it checks if there were any matching movies found, if not user gets a error message.
    If any movie(s) were found it iterates over the movies list of dictionaries and prints out every movie with
    a matching index from the matching_movies_by_index list.
    """
    movies = movie_storage.get_movies_data()
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
                print(f"{movie["title"]} ({movie["year"]}): {movie["rating"]}")


def movies_sorted_by_rating():
    """
    uses sorted() function to create a list of movies sorted by their rating.
    Next it iterates over said list and prints out all movies with their info.
    """
    movies = movie_storage.get_movies_data()
    movies_sorted_by_rating_list = sorted(movies, key = lambda x: x["rating"], reverse = True)
    for movie in movies_sorted_by_rating_list:
        print(f"{movie["title"]} ({movie["year"]}): {movie["rating"]}")


def movies_sorted_by_year():
    """
    Asks user for sorting order.
    Then uses sorted() function to create a list of movies sorted by their release year.
    Next it iterates over said list and prints out all movies with their info.
    """
    movies = movie_storage.get_movies_data()
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

    movies_sorted_by_year_list = sorted(movies, key=lambda x: x["year"], reverse = descending_order)
    for movie in movies_sorted_by_year_list:
        print(f"{movie["title"]} ({movie["year"]}): {movie["rating"]}")


def filter_movies():
    """
    Asks user for filter criteria, validates input with get_float_input() and get_int_input()
    and creates a new list with filter applied.
    If there are movies matching the filter prints them out, if not it prints a error message.
    """
    movies = movie_storage.get_movies_data()
    minimum_rating = get_float_input("Enter minimum rating, leave blank for no filter: ")
    start_year = get_int_input("Enter start year, leave blank for no filter: ")
    end_year = get_float_input("Enter end year, leave blank for no filter: ")

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
            print(f"{movie["title"]} ({movie["year"]}): {movie["rating"]}")
    else:
        print("\nThere are no movies with your filters applied.")


def get_printable_string_from_tuple(a_list: list) -> str:
    """
    Helper function to convert list of tuples into a string and returns it.
    :return: fstring
    """
    if len(a_list) > 1:
        string_to_print = ""
        for item in a_list:
            string_to_print += f"({item[0]}, {item[1]}) "
        return string_to_print
    else:
        return f"{a_list[0][0]}, {a_list[0][1]}"


def get_float_input(prompt: str):
    """
    validates user input if its empty or able to convert into float
    :return: None or Converted Input
    """
    while True:
        user_input = input(prompt)
        if user_input == "":
            return None
        try:
            return float(user_input)
        except ValueError:
            print("Invalid, please enter a number!")


def get_int_input(prompt: str):
    """
    validates user input if its empty or able to convert into integer
    :return: None or Converted Input
    """
    while True:
        user_input = input(prompt)
        if user_input == "":
            return None
        try:
            return int(user_input)
        except ValueError:
            print("Invalid, please enter a valid year!")


def print_menu(function_dict: dict):
    """
    prints a function dictionary as a menu
    """
    print("Menu:")
    for key, value in function_dict.items():
        print(f"{key}. {value["name"]}")


def main():
    FUNCTION_DICTIONARY = {
        "0": {
            "function": exit,
            "name": "Exit"
        },
        "1": {
            "function": list_movies,
            "name": "List movies"
        },
        "2": {
            "function": add_movie,
            "name": "Add movie"
        },
        "3": {
            "function": delete_movie,
            "name": "Delete movie"
        },
        "4": {
            "function": update_movie,
            "name": "Update movie"
        },
        "5": {
            "function": movie_stats,
            "name": "Stats"
        },
        "6": {
            "function": random_movie,
            "name": "Random movie"
        },
        "7": {
            "function": search_movie,
            "name": "Search movie"
        },
        "8": {
            "function": movies_sorted_by_rating,
            "name": "Movies sorted by rating"
        },
        "9": {
            "function": movies_sorted_by_year,
            "name": "Movies sorted by year"
        },
        "10": {
            "function": filter_movies,
            "name": "Filter movies"
        }
    }
    print("--------- Welcome to my Movies Database! ---------")
    while True:
        movie_storage.get_movies_data()
        print_menu(FUNCTION_DICTIONARY)
        user_choice = input("Enter Choice (0-10): ")
        if user_choice == "0":
            print("bye bye! :>")
            FUNCTION_DICTIONARY[user_choice]["function"]()
        elif user_choice in FUNCTION_DICTIONARY:
            print()
            FUNCTION_DICTIONARY[user_choice]["function"]()
        else:
            continue
        # buffer so the menu doesn't overwrite the requested option
        input("\nPress enter to continue\n")


if __name__ == "__main__":
    main()
