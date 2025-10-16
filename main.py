
import configparser
import requests
import random
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
    print(Selection)#["original_title"])
    for i in range(1,6):
        if Win == True:
            break
        print(f"Here is your clue number {i}:")
        GenerateClue(i, Selection)
    
        while True:
            guess = input("Name the movie:")
            #if guess == Selection["original_title"]:
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

def GenerateClue(guess, Selection):
    print(guess)
    match guess:
        case 1:
            return
        case 2:
            GenreResponse = requests.get("https://api.themoviedb.org/3/genre/movie/list?language=en", headers=headers)
            GenreData = GenreResponse.json()
            Genres = GenreData["genres"]
            OurGenres = Selection["genre_ids"]
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
            print("Here is this movies synopsis:")
            print(Selection["overview"])
            return
        
        #Clue options
        #Ascii Version of image? 
        #Cast? not sure if I can get this from the api

    
def GetRandomMovie():
    page = random.randint(1, 99)
    main_data_response = requests.get("https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=99&sort_by=popularity.desc&with_original_language=en&vote_count.gte=1000", headers=headers)
    main_data = main_data_response.json()
    #print(main_data)
    movies = main_data["results"]
    rand = random.randint(1, len(movies))
    # for movie in movies:
    #     print(movie["original_title"])
    #     print("------------")
    #print(movies[rand])
    return movies[rand]



main()

#Updates: 
#Fix randomness, does not seem random enough
#Make it so that close guesses work if they are close enough