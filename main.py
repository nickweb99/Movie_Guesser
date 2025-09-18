
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
    # #Api test response
    # API_Test = requests.get("https://api.themoviedb.org/3/authentication", headers=headers)
    # print(API_Test.text)

    rand = random.randint(1, 10)#Replace with upperbound on initial data pull

    main_data_response = requests.get("https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc&with_original_language=en", headers=headers)
    main_data = main_data_response.json()
    movies = main_data["results"]
    for movie in movies:
        print(movie["original_title"])
        print("------------")

main()