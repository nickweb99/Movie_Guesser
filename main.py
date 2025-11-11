
import configparser
import requests
import random
import secrets
import json
import msvcrt
from rapidfuzz import fuzz

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

def clear_last_line():
    CURSOR_UP_ONE = "\x1b[1A"
    ERASE_LINE = "\x1b[2K"
    print(CURSOR_UP_ONE + ERASE_LINE, end="")

def main():
    print("Welcome to the Movie Guesser game!")
    print("Would you like to play? Press 1 for yes and 2 for no.")
    play_game = None
    while(play_game != b'1'):
        play_game = msvcrt.getch()
        if play_game.decode() == '1':
            print("Welcome!")
        elif play_game.decode() == '2':
            print("Ok, goodbye!")
            return

    Selection = GetRandomMovie()
    Win = False
    ClueNums = list(range(1,7))
    for i in range(1,6):
        if Win == True:
            break

        Clue = random.choice(ClueNums)
        ClueNums.remove(Clue)
        print(f"Here's clue number {i}:")
        GenerateClue(i, Selection, Clue)
    
        while True:
            guess = input("Name the movie:")
            if guess != "" and CloseGuess(guess, Selection["original_title"]):
                Win = True
                break
            elif guess == "":
                clear_last_line()
                continue
            else:
                print("Incorrect")
            break
    
    if Win == True:
        print("You Win!")
    else:
        print(f"The movie was {Selection["original_title"]}")
        print("You Lose.")

def CloseGuess(Input, Model):
    score = fuzz.ratio(Input.lower(), Model.lower())
    if score > 80:
        return True
    else:
        return False

def GenerateClue(guess, Selection, Clue):
    GenreResponse = requests.get("https://api.themoviedb.org/3/genre/movie/list?language=en", headers=headers)
    GenreData = GenreResponse.json()
    Genres = GenreData["genres"]
    OurGenres = Selection["genre_ids"]
    CastResponse = requests.get(f"https://api.themoviedb.org/3/movie/{Selection["id"]}/credits", headers=headers)
    CastData = CastResponse.json()
    Cast = CastData["cast"]
    Star = Cast[0]
    StarName = Star["name"]
    StarCharacter = Star["character"]

    if guess == 5:
        print("Here is this movies synopsis:")
        print(Selection["overview"])
        return
    else:
        match Clue:
            case 1:
                print(f"The average rating of this movie is a {Selection["vote_average"]}/10")
            case 2:
                print("Here are this movies Genres:")
                for OurGenre in OurGenres:
                    for Genre in Genres:
                        if Genre["id"] == OurGenre:
                            print(Genre['name'])       
            case 3:
                print(f"This movie was released on {Selection["release_date"]}")
            case 4:
                print(f"This movie starts with the letter: {Selection["original_title"][0]}")
                return
            case 5:
                print(f"The lead actor in this movie is {StarName}")
                return
            case 6:
                print(f"The lead role in the movie is {StarCharacter}")
                return
    
def GetRandomMovie():
    page = secrets.randbelow(99) + 1
    main_data_response = requests.get(f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page={page}&sort_by=popularity.desc&with_original_language=en&vote_count.gte=1000", headers=headers)
    main_data = main_data_response.json()
    movies = main_data["results"]
    rand = secrets.randbelow(len(movies)-1) + 1
    return movies[rand]



main()