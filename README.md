# Movie Project

## Purpose
This project is a movie management application that allows users to list, add, delete, update, and search for movies. The application fetches movie details from the OMDb API and generates a website displaying the movie collection.

## Setup

### Prerequisites
- Python 3.x installed on your machine
- An OMDb API key (sign up at [OMDb API](http://www.omdbapi.com/apikey.aspx) to get one)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/movies_project.git
   cd movies_project```
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
    ```
3. Create a config.py file in the root directory and add your OMDb API key:
    ```python
   OMDB_API_KEY = 'your_api_key_here'

   ```
### Usage
1. Run the application:
    ```bash
    python main.py
   ```
2. Follow the on-screen instructions to list, add, delete, update, and search for movies.
3. Generate a website displaying the movie collection by selecting the "Generate website" option from the menu.
### License
This project is licensed under the MIT License.
