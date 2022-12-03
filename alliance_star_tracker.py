import sys
import utils
from time import sleep

def prenamed_teams(payload):
    list_teams = []  # index is puid and value is what team they are
    for player in payload['players']:  # Determine each player's team using names
        uid_player = payload['players'][player]['uid']
        name_player = payload['players'][player]['alias']
        team_number = name_player[0]
        list_teams.insert(uid_player, team_number)
    return list_teams


def team_scoring(list_teams, payload):
    score_teams = {}  # keys are team name and value is star count
    for team in list_teams:
        if team not in score_teams:
            score_teams[team] = 0
    for star in payload['stars']:  # Count up stars owned by each team
        owner_star = payload['stars'][star]['puid']
        if owner_star == -1:
            continue
        owner_team = list_teams[owner_star]
        score_teams[owner_team] += 1
    return score_teams


def list_by_score(score_teams, goal):
    team_pos = []
    for team in score_teams:
        team_star_count = score_teams[team]
        if not team_pos:
            team_pos.append((team, team_star_count))
        elif team_star_count <= team_pos[-1][1]:
            team_pos.append((team, team_star_count))
        else:
            copy_team_pos = team_pos.copy()
            for curIndex, pos in enumerate(copy_team_pos):
                if team_star_count > pos[1]:
                    team_pos.insert(curIndex, (team, team_star_count))
                    break
    for place, teamData in enumerate(team_pos, 1):
        name, score = teamData[0], teamData[1]
        print("{tPlace}. Team {tName} has {tScore} stars".format(tPlace=place, tName=name, tScore=score))
    if team_pos[0][1] >= goal:
        top_team = team_pos[0][0]
        top_stars = team_pos[0][1]
        sys.exit("Team {tName} has won with {sCount} stars".format(tName=top_team, sCount=top_stars))


# Main loop that calls checkStarCounts to get the amount of stars on each team every tick
while True:
    game_name = ''
    game_number, api_key = utils.credentials(game_name)
    # Calls api to get payload
    scanning_data = utils.call_api(game_number, api_key)
    goal_stars = scanning_data['stars_to_win']
    print(scanning_data['tick'])
    # returns list of each player and what team they are on, input is payload
    list_of_teams = prenamed_teams(scanning_data)
    # returns how many stars each team has, input is list of every player's team
    score_of_teams = team_scoring(list_of_teams, scanning_data)
    # prints a list of each team's score in order of highest to the lowest score
    list_by_score(score_of_teams, goal_stars)

    # Finds time from next tick in the game and program sleeps until next tick
    time_remaining = scanning_data['tick_rate'] * (1 - scanning_data['tick_fragment'])
    print(time_remaining)
    sleep(time_remaining * 60 + 60)
