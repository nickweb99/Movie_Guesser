
import configparser
import requests
import random
import json
import msvcrt

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
    print(Selection)#["original_title"])
    for i in range(1,6):
        print(f"Here is your clue number {i}:")
        GenerateClue(i)
    
        while True:
            guess = input("Name the movie:")
            if guess == Selection["original_title"]:
                print("You Win!")
                break
            elif guess == "":
                clear_last_line()
                continue
            else:
                print("Incorrect")
            break

def GenerateClue(guess):
    match guess:
        case 1:
            return
        case 2:
            return
        case 3:
            return
        case 4:
            return
        case 5:
            return
        
        #Clue options
        #Display overview
        #genre_ids
        #release_date
        #Ascii Version of image? 
        #Cast? not sure if I can get this from the api

    
def GetRandomMovie():
    page = random.randint(1, 99)
    main_data_response = requests.get("https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=99&sort_by=popularity.desc&with_original_language=en&vote_count.gte=1000", headers=headers)
    main_data = main_data_response.json()
    movies = main_data["results"]
    rand = random.randint(1, len(movies))
    # for movie in movies:
    #     print(movie["original_title"])
    #     print("------------")
    #print(movies[rand])
    return movies[rand]



main()
