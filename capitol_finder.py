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
def find_home_world(payload, player):
    player_list = payload['players']
    star_list = payload['stars']
    if player.isdigit() and player in player_list:
        huid = (str(player_list[player]['huid']))
    else:
        for player in player_list:
            if player_list[player]['alias'] == player:
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
    return home_world


target = input("Type target's player ID or alias ")
huid, name = find_home_world(call_api(5194985387065344, 'gHRUO4', '0.1'), target)
print(huid, name)
