# Just fill out your parameters in the labelled configuration section,
# and then you can directly copy the printed list into NP

import sys
from random import randrange

### Beginning of Configuration Section ###

distance = 15      # Distance between each team (Group of players)
players = 14       # Amount of players
team_size = 2      # Amount of players on each team
team_distance = 5  # Distance between each teammate
forbidden_coords = []
# If your amount of players is the smallest possible number for a big triangle (Ex: 11 players
# in a 15 player triangle) then you can forbid certain coordinates from being used as spawn
# points. I suggest using the corner spots or chopping off the top
random_spawning = False
# Boolean value determining if the program uses random or sequential spawning. Random spawning
# can place home worlds on any point of the triangle, which creates more interesting maps
# but could leave a player way out of the way. Sequential spawning starts near the base of
# triangle and moves all the way to the right then moves up one layer, creating more of
# a trapezoid then a triangle, but guarantees everyone is together.

### End of configuration section ###

# Checks if amount of players can be split into even teams of TEAM_SIZE
if players % team_size == 0:
    num_teams = int(players / team_size)  # Calculates amount of teams for future reference
    base_coords = []  # Initializes list for center coordinates of each team
    curCoords = [0, 0]  # Initializes object to store current coordinates for 'for' loop
else:
    print("{p} players can not be split into teams of {s}".format(p=players, s=team_size))
    sys.exit()


# Finds a triangle with a side length of X players that can fit all teams
def calculate_triangle(neededPoints, sideLength):
    x_delta, y_delta = sideLength / 2, ((3 ** 0.5) * sideLength) / 2
    triSize = 1
    while True:
        triPoints = []
        curX, curY = 0, 0
        count = 1
        testTri = triSize
        while testTri > 0:
            for point in range(testTri):
                triPoints.append([curX, curY])
                curX += x_delta * 2
            curY += y_delta
            curX = x_delta * count
            count += 1
            testTri -= 1
        if len(triPoints) >= neededPoints:
            return triPoints
        else:
            triSize += 1


# Calls CALCULATE_TRIANGLE to create the complete triangle
totalPoints = calculate_triangle(num_teams, distance)

forbidTestPoints = totalPoints.copy()
# Removes any points from totalPoints if they are in the FORBIDDEN_COORDS list
for point in forbidTestPoints:
    if point in forbidden_coords:
        totalPoints.remove(point)

spawnPoints = []
if random_spawning:
    # Chooses NUM_TEAMS amount of random coordinates from totalPoints to use as spawn positions
    for team in range(num_teams):
        i = randrange(0, len(totalPoints))
        spawnPoints.append(totalPoints[i])
        totalPoints.pop(i)
else:
    # appends the first NUM_TEAMS amount of coordinates from totalPoints to spawnPoints
    for team in range(num_teams):
        spawnPoints.append(totalPoints[team])

groupedPoints = spawnPoints.copy()
# Adds an extra spawn point TEAM_DISTANCE away from each original point
for team in spawnPoints:
    x, y = team[0] + team_distance, team[1]
    groupedPoints.append([x, y])

# Prints completed list in compatible format of NP, just copy and paste
print(groupedPoints)
