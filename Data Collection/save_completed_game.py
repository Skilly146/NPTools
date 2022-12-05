import utils
import os.path
import json

game_number = input('What is the game number? ').replace(' ', '')
payload = utils.call_api(game_number)
utils.add_new_credentials(game_number)
name = payload['name'].lower().replace(' ', '_')
game_incomplete = False
for star in payload['stars']:
    if not int(payload['stars'][star]['v']):
        print("This game isn't completed yet")
        game_incomplete = True
        break
if not game_incomplete:
    if 'y' == input('Would you like to save game {} '.format(name)):
        if not os.path.exists('game_data/{}.json'.format(name)):
            with open('game_data/{}.json'.format(name), 'x') as f:
                json.dump(payload, f)
            with open('game_data/game_name_to_number_converter.json') as f:
                source = json.load(f)
            with open('game_data/game_name_to_number_converter.json', 'w') as f:
                source[game_number] = name
                json.dump(source, f, indent=4)
