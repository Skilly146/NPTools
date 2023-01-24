import utils
import matplotlib.pyplot as plt

game_number, api_key = utils.credentials("AStonedApe's_32_Player_Game")
payload = utils.call_api(game_number, api_key)

x_coords = []
y_coords = []
for field in payload['stars']:
    x_coords.append(payload['stars'][field]['x'])
    y_coords.append(payload['stars'][field]['y'])

fig, ax = plt.subplots()
ax.scatter(x_coords, y_coords)
plt.show()
