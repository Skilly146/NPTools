import requests


# Calls api then returns payload
def call_api(game_number, code, api_version):
    root = "https://np.ironhelmet.com/api"
    params = {"game_number": game_number,
              "code": code,
              "api_version": api_version}
    payload = requests.post(root, params).json()['scanning_data']
    return payload


# Takes a game payload and targeted players alias and returns home world UID and in game name
def find_home_world(payload):
    target_player = input("Type target's player ID or alias ")
    player_list = payload['players']
    star_list = payload['stars']
    if target_player.isdigit() and target_player in player_list:
        huid = (str(player_list[target_player]['huid']))
    else:
        for player in player_list:
            if player_list[player]['alias'] == target_player:
                huid = (str(player_list[player]['huid']))
                break
    try:
        for star in star_list:
            if star == huid:
                home_world = huid, star_list[star]['n']
                break
    except UnboundLocalError:
        print("Invalid alias or player ID")
        quit()
    print(home_world[0], home_world[1])
    return home_world


def star_stats(payload):
    target_star = input("Type star's UID or name ")
    star_list = payload['stars']
    key_list = {'c': 'Ship Fraction', 'e': 'Economy', 'uid': "Star's Unique ID",
                'i': 'Industry', 's': 'Science', 'n': "Star's Current Name",
                'puid': "Player ID of Star's Owner", 'r': 'Natural Resources Including Terraforming',
                'ga': 'If the Star Has a Warp Gate, 0 = No, 1 = Yes',
                'v': 'If the Star is Visible, 0 = No, 1 = Yes',
                'y': "Star's Y Coordinate, 8 Light Years to 1 Coordinate",
                'x': "Star's X Coordinate, 8 Light Years to 1 Coordinate",
                'nr': 'Natural Resources not Including Terraforming', 'st': 'Number of ships on star'}
    if target_star.isdigit() and target_star in star_list:
        stats = (star_list[target_star])
    else:
        for star in star_list:
            if star_list[star]['n'] == target_star:
                stats = (star_list[star])
                break
    try:
        for i in stats:
            print(key_list[i] + ':', stats[i])
    except UnboundLocalError:
        print("Invalid star UID or name")


scanning_data = call_api(5194985387065344, 'gHRUO4', '0.1')
needed_function = int(input("Would you like to (1), find a player's home world or (2), get a star's stats "))

if needed_function == 1:
    find_home_world(scanning_data)
elif needed_function == 2:
    star_stats(scanning_data)
