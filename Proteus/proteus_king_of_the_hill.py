import random

### Beginning of configuration section ###

distance = int()  # Distance in light years between each player
players = int()  # Amount of players
galaxy_type = ''  # 'circular' for circular galaxy and 'random' for random hex
scoring_zone_coords = []
# Coordinates for scoring zones, each coord is a tuple (x, y) within list item.
# Optional, will only create 1 in the center if you don't put anything
player_starting_infra = {'e': int(), 'i': int(), 's': int(), 'st': int(), 'ga': int(),
                         'wh': int(), 'x': float(), 'y': float(), 'r': int()}
# Set starting infra for all players. 'e' = economy, 'i' = industry, 's' = science,
# 'st' = ships, 'ga' = warp gate (0 means none, 1 means yes)
# 'wh' = star UID of desired connection star (optional), 'x' = x coord (optional)
# 'y' = y coord (optional), 'r' = natural resources (optional)
ai_on_zone = bool()  # If there should be AIs on each hill
ai_starting_infra = {'e': int(), 'i': int(), 's': int(), 'st': int(),
                     'wh': int(), 'r': int()}
# Set starting infra for all AIs. 'e' = economy, 'i' = industry, 's' = science,
# 'st' = ships, 'wh' = star UID of desired connection star (optional),
# 'r' = natural resources (optional)

### End of configuration section ###

star_format = {'stars': [{"uid": int, "name": str, "x": float, "y": float,
                          "r": int, "ga": int, "e": int, "i": int,
                          "s": int, "st": int, "puid": int, "wh": int}, {}]}
print(star_format)
