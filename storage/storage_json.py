import json
from .istorage import IStorage

class StorageJson(IStorage):
    def __init__(self, file_path):
        self.file_path = file_path

    def validate_existence(self):
        """
        Checks if the file exists and calls validate_data, if data
        does not exist function calls write_default_data()
        """
        try:
            with open(self.file_path, "r"):
                return True
        except FileNotFoundError:
            print("File does not exist, creating default Data")
            self.write_default_data()
            return False

    def validate_data(self) -> bool:
        """
        Calls validate_existence() to check if there is any data,
        if there is data to work with it reads the data and checks
        if data is valid. In case data is invalid it calls write_default_data()
        :returns: Boolean
        """
        if self.validate_existence():
            try:
                with open(self.file_path, "r") as json_file:
                    data = json.load(json_file)
                    if len(data) >= 1:
                        return True
            except json.decoder.JSONDecodeError:
                print("File data missing or corrupted, creating default Data")
                self.write_default_data()
                return False
        return False

    def write_default_data(self):
        """
        Gets called if data is not existent or invalid and
        writes some default data
        """
        default_data = [{
            "title": "Fight Club",
            "year": 1999,
            "rating": 8.8
        }]
        with open(self.file_path, "w") as file_writer:
            json.dump(default_data, file_writer, indent=4)

    def _load_movies(self):
        if self.validate_data():
            with open(self.file_path, "r") as file:
                return json.load(file)
        return []

    def _save_movies(self, movies):
        with open(self.file_path, "w") as file:
            json.dump(movies, file, indent=4)

    def list_movies(self):
        return self._load_movies()

    def add_movie(self, title, year, rating, poster):
        movies = self._load_movies()
        movies.append({"title": title, "year": year, "rating": rating, "poster": poster})
        self._save_movies(movies)

    def delete_movie(self, title):
        movies = self._load_movies()
        movies = [movie for movie in movies if movie["title"] != title]
        self._save_movies(movies)

    def update_movie(self, title, rating):
        movies = self._load_movies()
        for movie in movies:
            if movie["title"] == title:
                movie["rating"] = rating
                break
        self._save_movies(movies)
