import json


FILENAME = "movie_database.json"


def validate_existence():
    """
    Checks if the file exists and calls validate_data, if data
    does not exist function calls write_default_data()
    """
    data_exists = True
    try:
        with open(FILENAME, "r") as json_file:
            data_exists = True
    except FileNotFoundError:
        print("File does not exist, creating default Data")
        data_exists = False

    if data_exists:
        return True
    else:
        write_default_data()


def validate_data() -> bool:
    """
    Calls validate_existence() to check if there is any data,
    if there is data to work with it reads the data and checks
    if data is valid. In case data is invalid it calls write_default_data()
    :returns: Boolean
    """
    if validate_existence():
        data_valid = False
        try:
            with open(FILENAME, "r") as json_file:
                data = json.load(json_file)
                if len(data) >= 1 and data != "[]":
                    data_valid = True

        except json.decoder.JSONDecodeError:
            print("File data missing or corrupted, creating default Data")
            data_valid = False

        if data_valid:
            return True
        else:
            write_default_data()
            return False


def write_default_data():
    """
    gets called if data is not existent or invalid and
    writes some default data
    """
    default_data = [{
        "title": "Fight Club",
        "year": 1999,
        "rating": 8.8
    }]
    with open(FILENAME, "w") as file_writer:
        json.dump(default_data, file_writer, indent = 4)


def get_movies_data() -> list:
    """
    Calls validate_data() to verify file integrity.
    If everything is fine the function loads the information from
    the JSON file and returns the data as a list of dictionaries
    :return: list (of dictionaries)
    """
    data_is_invalid = True
    while validate_data():
        if validate_data():
            data_is_valid = False
            with open(FILENAME, "r") as file_reader:
                data = json.load(file_reader)
            return data


def write_movie_data(title: str, year: int, rating: float):
    """
    Adds a movie to the movies database.
    Loads the information from the JSON file, add the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = get_movies_data()
    movies.append({
        "title": title,
        "year": year,
        "rating": rating
    })

    with open(FILENAME, "w") as file_writer:
        json.dump(movies, file_writer, indent = 4)


def delete_movie_data(title: str):
    """
    Deletes a movie from the movies database.
    Loads the information from get_movies_data(), deletes the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = get_movies_data()
    del movies[next(i for i, movie in enumerate(movies) if movie["title"] == title)]

    with open(FILENAME, "w") as file_writer:
        json.dump(movies, file_writer, indent = 4)


def update_movie_data(title: str, rating: float):
    """
    Updates a movie from the movies database.
    Loads the information from get_movies_data(), updates the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = get_movies_data()
    index_of_dictionary_to_update = next(i for i, movie in enumerate(movies) if movie["title"] == title)
    movies[index_of_dictionary_to_update]["rating"] = rating

    with open(FILENAME, "w") as file_writer:
        json.dump(movies, file_writer, indent = 4)
