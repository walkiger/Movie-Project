import csv
from .istorage import IStorage


class StorageCsv(IStorage):
    """
    A class to represent storage for movies using CSV format.
    """

    def __init__(self, file_path='data/movies.csv'):
        """
        Initialize the StorageCsv with the given file path.

        :param file_path: Path to the CSV file.
        """
        self.file_path = file_path

    def validate_existence(self):
        """
        Validate if the CSV file exists.

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
        Validate the data in the CSV file.

        :return: True if data is valid, False otherwise.
        """
        if self.validate_existence():
            try:
                with open(self.file_path, "r") as csv_file:
                    reader = csv.DictReader(csv_file)
                    data = list(reader)
                    if len(data) >= 1:
                        return True
            except Exception as e:
                print(f"Error reading CSV file: {e}")
                self.write_default_data()
                return False
        return False

    def write_default_data(self):
        """
        Write default data to the CSV file.
        """
        default_data = [
            {"title": "Fight Club", "year": 1999, "rating": 8.8}
        ]
        with open(self.file_path, "w", newline='') as csv_file:
            fieldnames = ["title", "year", "rating"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(default_data)

    def list_movies(self):
        """
        List all movies from the CSV file.

        :return: Dictionary of movies.
        """
        movies = {}
        if self.validate_data():
            with open(self.file_path, "r") as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    title = row["title"]
                    movies[title] = {
                        "year": int(row["year"]),
                        "rating": float(row["rating"]),
                        "poster": row.get("poster", "")
                    }
        return movies

    def add_movie(self, title, year, rating, poster):
        """
        Add a new movie to the CSV file.

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
        Delete a movie from the CSV file.

        :param title: Title of the movie to delete.
        """
        movies = self.list_movies()
        if title in movies:
            del movies[title]
            self._save_movies(movies)

    def update_movie(self, title, rating):
        """
        Update the rating of an existing movie in the CSV file.

        :param title: Title of the movie to update.
        :param rating: New rating of the movie.
        """
        movies = self.list_movies()
        if title in movies:
            movies[title]["rating"] = rating
            self._save_movies(movies)

    def _save_movies(self, movies):
        """
        Save movies to the CSV file.

        :param movies: Dictionary of movies to save.
        """
        with open(self.file_path, "w", newline='') as csv_file:
            fieldnames = ["title", "year", "rating", "poster"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for title, details in movies.items():
                row = {"title": title, "year": details["year"], "rating": details["rating"],
                       "poster": details["poster"]}
                writer.writerow(row)
