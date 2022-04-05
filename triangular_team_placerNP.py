# Just fill out your parameters in the labelled configuration section,
# and then you can directly copy the printed list into NP

import sys

### Beginning of Configuration Section ###

distance = 25      # Distance between each team (Group of players)
players = 14       # Amount of players
team_size = 2      # Amount of players on each team
team_distance = 5  # Distance between each teammate

### End of configuration section ###

# Checks if amount of players can be split into even teams of TEAM_SIZE
if players % team_size == 0:
    num_teams = int(players / team_size)  # Calculates amount of teams for future reference
    base_coords = []  # Initializes list for center coordinates of each team
    curCoords = [0, 0]  # Initializes object to store current coordinates for 'for' loop
    x_delta, y_delta = distance/2, ((3 ** 0.5) * distance)/2
    # Calculates each leg of the right triangle made by splitting the equilateral triangle
    # with side lengths Distance in half
else:
    print("{p} players can not be split into teams of {s}".format(p=players, s=team_size))
    sys.exit()
