import checkStarCounts as csc
from time import sleep

# Info for the API call
game_number = "5237130488709120"  # Found in URL of game
code = "Y6E1Ae"                   # Can be generated in options menu
api_version = "0.1"               #

# Main loop that calls checkStarCounts to get the amount of stars on each team every tick
while True:
    # Calls api to get payload
    scanningData, goalStars = csc.call_api(game_number, code, api_version)
    print(scanningData['tick'])
    # returns list of each player and what team they are on, input is payload
    listTeams = csc.prenamed_teams(scanningData)
    # returns how many stars each team has, input is list of every player's team
    scoreTeams = csc.team_scoring(listTeams, scanningData)
    # prints a list of each team's score in order of highest to the lowest score
    csc.list_by_score(scoreTeams, goalStars)

    # Finds time from next tick in the game and program sleeps until next tick
    time_remaining = scanningData['tick_rate'] * (1 - scanningData['tick_fragment'])
    print(time_remaining)
    sleep(time_remaining * 60 + 60)
