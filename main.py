
import configparser
import requests
import random
import json

config = configparser.ConfigParser()

try:
    config.read('config.ini')
except configparser.Error as e:
    print(f"Error reading config file: {e}")

api_key = config['API_SETTINGS']['api_key']

headers = {
    "accept": "application/json",
    "Authorization": api_key
}

def main():
    print("Welcome to the Movie Guesser game!")
    Selection = GetRandomMovie()
    print(Selection["original_title"])
    
def GetRandomMovie():
    page = random.randint(1, 99)
    main_data_response = requests.get("https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=99&sort_by=popularity.desc&with_original_language=en&vote_count.gte=1000", headers=headers)
    main_data = main_data_response.json()
    movies = main_data["results"]
    rand = random.randint(1, len(movies))#Replace with upperbound on initial data pull
    # for movie in movies:
    #     print(movie["original_title"])
    #     print("------------")
    #print(movies[rand])
    return movies[rand]



main()
