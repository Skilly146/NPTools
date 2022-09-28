import requests
import sys


# Calls api then returns payload and winning star count
def call_api(game_number, code, api_version):
    root = "https://np.ironhelmet.com/api"
    params = {"game_number": game_number,
              "code": code,
              "api_version": api_version}
    payload = requests.post(root, params).json()['scanning_data']
    goal = payload['stars_for_victory']
    return payload, goal


#
def prenamed_teams(payload):
    listTeams = []  # index is puid and value is what team they are
    for player in payload['players']:  # Determine each player's team using names
        uidPlayer = payload['players'][player]['uid']
        namePlayer = payload['players'][player]['alias']
        teamNumber = namePlayer[0]
        listTeams.insert(uidPlayer, teamNumber)
    return listTeams


def team_scoring(listTeams, payload):
    scoreTeams = {}  # keys are team name and value is star count
    for team in listTeams:
        if team not in scoreTeams:
            scoreTeams[team] = 0
    for star in payload['stars']:  # Count up stars owned by each team
        ownerStar = payload['stars'][star]['puid']
        if ownerStar == -1:
            continue
        ownerTeam = listTeams[ownerStar]
        scoreTeams[ownerTeam] += 1
    return scoreTeams


def list_by_score(scoreTeams, goal):
    teamPos = []
    for team in scoreTeams:
        teamStarCount = scoreTeams[team]
        if not teamPos:
            teamPos.append((team, teamStarCount))
        elif teamStarCount <= teamPos[-1][1]:
            teamPos.append((team, teamStarCount))
        else:
            copyTeamPos = teamPos.copy()
            for curIndex, pos in enumerate(copyTeamPos):
                if teamStarCount > pos[1]:
                    teamPos.insert(curIndex, (team, teamStarCount))
                    break
    for place, teamData in enumerate(teamPos, 1):
        name, score = teamData[0], teamData[1]
        print("{tPlace}. Team {tName} has {tScore} stars".format(tPlace=place, tName=name, tScore=score))
    if teamPos[0][1] >= goal:
        topTeam = teamPos[0][0]
        topStars = teamPos[0][1]
        sys.exit("Team {tName} has won with {sCount} stars".format(tName=topTeam, sCount=topStars))
