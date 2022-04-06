# Just fill out your parameters in the labelled configuration section,
# and then you can directly copy the printed list into NP

from math import pi, cos, sin
import sys

### Beginning of configuration section ###

distance = int()   # Distance in light years between each player (Distance is along the circumference, not linear)
players = int()    # Amount of players
team_size = int()  # Amount of players on each team
team_padding = float()
# Amount of extra units of variable DISTANCE between teams
# (0 will have everyone DISTANCE apart, 1 will have everyone 2 DISTANCE apart,
# 1.5 would be 2.5 units of DISTANCE)
world_in_center = None
# Boolean asking if you want an extra world in the center of the map,
# useful because if you only use the outer stars NP won't spawn stars in the center

### End of configuration section ###

if players % team_size == 0:
    num_teams = players / team_size  # Calculates amount of teams for future reference
    map_radius = (num_teams * (distance * (team_size + team_padding))) / (2 * pi)
    # Calculates map radius for future reference
else:
    print("{p} players can not be split into teams of {s}".format(p=players, s=team_size))
    sys.exit()


# Finds home world coordinates based of circle radius and inputted angle
def world_placer(angle, radius):
    x, y = radius * cos(angle), radius * sin(angle)
    return [x + 40, y + 40]


radians = pi / ((num_teams * (team_size + team_padding)) / 2)
# Determines angular distance between each home world, including padding
totalSpaces = int((2 * pi) / (pi / ((num_teams * (team_size + team_padding)) / 2)))
# Determines total amount of home worlds and padding spaces
homeWorlds = []  # Initializes list of home world coordinates
curAngle = 0  # Initializes variable to store current angle around the circle

# for every player, determine if current player is start of new team, if so then
# add TEAM_PADDING + RADIANS so there is spacing between players,
# and finally add home world coordinates for each player in team
for world in range(players):
    if world % team_size == 0:
        curAngle += (team_padding*radians) + radians
        homeWorlds.append(world_placer(curAngle, map_radius))
    else:
        curAngle += radians
        homeWorlds.append(world_placer(curAngle, map_radius))

# Decides to add an extra coordinate in the center using world_in_center variable from configuration
if world_in_center:
    homeWorlds.append([0 + 40, 0 + 40])

# Prints completed homeWorlds list in compatible format with NP
print(homeWorlds)
