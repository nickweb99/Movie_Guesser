
import configparser
import requests

config = configparser.ConfigParser()

try:
    config.read('config.ini')
except configparser.Error as e:
    print(f"Error reading config file: {e}")

api_key = config['API_SETTINGS']['api_key']

url = "https://api.themoviedb.org/3/authentication"

headers = {
    "accept": "application/json",
    "Authorization": api_key
}

def main():
    print("Welcome to the Movie Guesser game!")

    response = requests.get(url, headers=headers)

    print(response.text)

main()