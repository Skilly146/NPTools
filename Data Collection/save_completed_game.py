from utils import call_api
import json

game_number = input('What is the game number? ').replace(' ', '')
payload = call_api(game_number)
name = payload['name'].lower().replace(' ', '_')
if 'y' == input('Would you like to save game {} '.format(name)):
    with open('game_data/{}.json'.format(name), 'x') as f:
        json.dump(payload, f)
