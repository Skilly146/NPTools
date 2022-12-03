from utils import call_api, credentials, add_new_credentials
import os.path
import json

game_number = input('What is the game number? ').replace(' ', '')
payload = call_api(game_number)
if not credentials(payload['name']):
    add_new_credentials(game_number)
name = payload['name'].lower().replace(' ', '_')
if 'y' == input('Would you like to save game {} '.format(name)):
    if not os.path.exists('game_data/{}.json'.format(name)):
        with open('game_data/{}.json'.format(name), 'x') as f:
            json.dump(payload, f)
        with open('game_data/game_name_to_number_converter.json') as f:
            source = json.load(f)
        with open('game_data/game_name_to_number_converter.json', 'w') as f:
            source[game_number] = name
            json.dump(source, f, indent=4)
