from movie_app import MovieApp
from storage.storage_csv import StorageCsv
# Or switch to StorageJson if needed5
# from storage.storage_json import StorageJson

def main():
    """
    Main function to initialize and run the movie application.
    """
    storage = StorageCsv('data/movies.csv')
    # If you want to use JSON storage, switch to:
    # storage = StorageJson('data/movies.json')
    movie_app = MovieApp(storage)
    movie_app.run()

if __name__ == "__main__":
    main()
