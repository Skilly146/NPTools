import requests


target = 'lollo'


def call_api(game_number, code, api_version):
    root = "https://np.ironhelmet.com/api"
    params = {"game_number": game_number,
              "code": code,
              "api_version": api_version}
    payload = requests.post(root, params).json()['scanning_data']
    return payload


def find_home_world(payload, alias):
    player_list = payload['players']
    star_list = payload['stars']
    for player in player_list:
        if player_list[player]['alias'] == alias:
            huid = (str(player_list[player]['huid']))
            break
    for star in star_list:
        if star == huid:
            home_world = huid, star_list[star]['n']
            break
    return home_world


huid, name = find_home_world(call_api(5194985387065344, 'gHRUO4', '0.1'), target)
print(huid, name)
