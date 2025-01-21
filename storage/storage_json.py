import json
from .istorage import IStorage


class StorageJson(IStorage):
    """
    A class to represent storage for movies using JSON format.
    """

    def __init__(self, file_path='data/movies.json'):
        """
        Initialize the StorageJson with the given file path.

        :param file_path: Path to the JSON file.
        """
        self.file_path = file_path


    def validate_existence(self):
        """
        Validate if the JSON file exists.

        :return: True if file exists, False otherwise.
        """
        try:
            with open(self.file_path, "r"):
                return True
        except FileNotFoundError:
            print("File does not exist, creating default data")
            self.write_default_data()
            return False


    def validate_data(self) -> bool:
        """
        Validate the data in the JSON file.

        :return: True if data is valid, False otherwise.
        """
        if self.validate_existence():
            try:
                with open(self.file_path, "r") as json_file:
                    data = json.load(json_file)
                    if len(data) >= 1:
                        return True
            except json.decoder.JSONDecodeError:
                print("File data missing or corrupted, creating default data")
                self.write_default_data()
                return False
        return False


    def write_default_data(self):
        """
        Write default data to the JSON file.
        """
        default_data = [{
            "title": "Fight Club",
            "year": 1999,
            "rating": 8.8
        }]
        with open(self.file_path, "w") as file_writer:
            json.dump(default_data, file_writer, indent=4)


    def list_movies(self):
        """
        List all movies from the JSON file.

        :return: Dictionary of movies.
        """
        movies = {}
        if self.validate_data():
            with open(self.file_path, "r") as json_file:
                data = json.load(json_file)
                for movie in data:
                    title = movie["title"]
                    movies[title] = {
                        "year": movie["year"],
                        "rating": movie["rating"],
                        "poster": movie.get("poster", "")
                    }
        return movies


    def add_movie(self, title, year, rating, poster):
        """
        Add a new movie to the JSON file.

        :param title: Title of the movie.
        :param year: Release year of the movie.
        :param rating: Rating of the movie.
        :param poster: Poster URL of the movie.
        """
        movies = self.list_movies()
        movies[title] = {"year": year, "rating": rating, "poster": poster}
        self._save_movies(movies)


    def delete_movie(self, title):
        """
        Delete a movie from the JSON file.

        :param title: Title of the movie to delete.
        """
        movies = self.list_movies()
        if title in movies:
            del movies[title]
            self._save_movies(movies)


    def update_movie(self, title, rating):
        """
        Update the rating of an existing movie in the JSON file.

        :param title: Title of the movie to update.
        :param rating: New rating of the movie.
        """
        movies = self.list_movies()
        if title in movies:
            movies[title]["rating"] = rating
            self._save_movies(movies)


    def _save_movies(self, movies):
        """
        Save movies to the JSON file.

        :param movies: Dictionary of movies to save.
        """
        data = [{"title": title, "year": details["year"], "rating": details["rating"], "poster": details.get("poster", "")}
                for title, details in movies.items()]
        with open(self.file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)
