from storage.storage_json import StorageJson

# Create an instance of StorageJson with a sample JSON file
storage = StorageJson('movies.json')

# List movies
print(storage.list_movies())

# Add a new movie
storage.add_movie('Inception', 2010, 8.8, 'poster_url')

# List movies again to see the added movie
print(storage.list_movies())

# Update the movie's rating
storage.update_movie('Inception', 9.0)

# List movies again to see the updated rating
print(storage.list_movies())

# Delete the movie
storage.delete_movie('Inception')

# List movies again to see the removed movie
print(storage.list_movies())
