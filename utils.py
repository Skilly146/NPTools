import requests
import random
import math
import json
import os.path


# Calls api then returns payload
def call_api(game_number, api_key=None):
    api_version = '0.1'
    api_output = None
    if api_key:
        root = "https://np.ironhelmet.com/api"
        params = {"game_number": game_number,
                  "code": api_key,
                  "api_version": api_version}
        api_output = requests.post(root, params).json()['scanning_data']
    else:
        root = "http://nptriton.cqproject.net/game/{}/full".format(game_number)
        api_output = requests.post(root).json()
    if not api_output:
        with open('game_data/game_name_to_number_converter.json') as f:
            converter_dict = json.load(f)
        with open('game_data/{}.json'.format(converter_dict[str(game_number)])) as f:
            api_output = json.load(f)
    return api_output


def star_distance(start_x, start_y, end_x, end_y):
    x_dif = start_x - end_x
    y_dif = start_y - end_y
    sq_x_dif = x_dif ** 2
    sq_y_dif = y_dif ** 2
    return math.sqrt(sq_x_dif + sq_y_dif)


def step_distance_angle(star_x, star_y, home_star_distance, angle):
    x = star_x
    y = star_y
    distance = home_star_distance

    x += math.cos(angle) * distance
    y += math.sin(angle) * distance

    return x, y


def create_wormholes(universe, count, mirror):
    if mirror:
        return

    gate_count = 0
    all_stars = []

    for star in universe['stars']:
        # make sure we don't build wormholes in the players starting empire.
        if universe['stars'][star]['puid'] == -1:
            all_stars.append(star)
    while gate_count < count:
        star = universe['stars'][random.choice(all_stars)]
        target = universe['stars'][random.choice(all_stars)]
        dist = star_distance(float(star['x']), float(star['y']), float(target['x']), float(target['y']))
        if dist > 2:
            star['wh'] = target['uid']
            target['wh'] = star['uid']

            star['r'] = 5
            target['r'] = 5
            all_stars.remove(str(star['uid']))
            all_stars.remove(str(target['uid']))

            if len(all_stars) < 2:
                return universe

            gate_count += 1
    return universe


# star = star object, chance = 1 or 2 (1 means 10% gate chance, 2 means 30% gate chance)
def test_warpgate(star, chance):
    if chance:
        gate_roll = random.randint(0, 99)
        if chance == 1 and gate_roll < 10:
            star['ga'] = 1
        if chance == 2 and gate_roll < 30:
            star['ga'] = 1
    return star


# home_world_distance = 16 in a regular 64p game, players = 64
def create_home_star_points_quad_flower_64(home_world_distance, players):
    home_star_points = []
    xjhdexters_data = [[31.9068, -6.2000], [8.7681, 0.0000], [21.1681, 0.0000], [31.9068, 6.2000], [42.6456, 12.4000],
                       [44.9731, 24.5796], [54.3572, 16.4741], [56.6847, 28.6537], [56.2323, 41.0455],
                       [44.2548, 44.2548], [53.0229, 53.0229], [41.0455, 56.2323], [28.6537, 56.6847],
                       [24.5796, 44.9731], [16.4741, 54.3572], [12.4000, 42.6456], [6.2000, 31.9068], [0.0000, 8.7681],
                       [0.0000, 21.1681], [-6.2000, 31.9068], [-12.4000, 42.6456], [-24.5796, 44.9731],
                       [-16.4741, 54.3572], [-28.6537, 56.6847], [-41.0455, 56.2323], [-44.2548, 44.2548],
                       [-53.0229, 53.0229], [-56.2323, 41.0455], [-56.6847, 28.6537], [-44.9731, 24.5796],
                       [-54.3572, 16.4741], [-42.6456, 12.4000], [-31.9068, 6.2000], [-8.7681, 0.0000],
                       [-21.1681, 0.0000], [-31.9068, -6.2000], [-42.6456, -12.4000], [-44.9731, -24.5796],
                       [-54.3572, -16.4741], [-56.6847, -28.6537], [-56.2323, -41.0455], [-44.2548, -44.2548],
                       [-53.0229, -53.0229], [-41.0455, -56.2323], [-28.6537, -56.6847], [-24.5796, -44.9731],
                       [-16.4741, -54.3572], [-12.4000, -42.6456], [-6.2000, -31.9068], [0.0000, -8.7681],
                       [0.0000, -21.1681], [6.2000, -31.9068], [12.4000, -42.6456], [24.5796, -44.9731],
                       [16.4741, -54.3572], [28.6537, -56.6847], [41.0455, -56.2323], [44.2548, -44.2548],
                       [53.0229, -53.0229], [56.2323, -41.0455], [56.6847, -28.6537], [44.9731, -24.5796],
                       [54.3572, -16.4741], [42.6456, -12.4000]]
    for i in range(players):
        if i < len(xjhdexters_data):
            sx = float(xjhdexters_data[i][0]) * (float(home_world_distance) / 20.0)
            sy = float(xjhdexters_data[i][1]) * (float(home_world_distance) / 20.0)
            home_star_points.append((sx, sy))
    return home_star_points


# home_world_distance = 16 I assume because of 64p game, players = 32
def create_home_star_points_quad_flower_32(home_world_distance, players):
    home_star_points = []
    xjhdexters_data = [[11.3218, -2.2000], [3.1113, 0.0000], [7.5113, 0.0000], [11.3218, 2.2000], [11.9446, 6.5557],
                       [7.6945, 7.6945], [10.8058, 10.8058], [6.5557, 11.9446], [2.2000, 11.3218], [0.0000, 3.1113],
                       [0.0000, 7.5113], [-2.2000, 11.3218], [-6.5557, 11.9446], [-7.6945, 7.6945], [-10.8058, 10.8058],
                       [-11.9446, 6.5557], [-11.3218, 2.2000], [-3.1113, 0.0000], [-7.5113, 0.0000],
                       [-11.3218, -2.2000], [-11.9446, -6.5557], [-7.6945, -7.6945], [-10.8058, -10.8058],
                       [-6.5557, -11.9446], [-2.2000, -11.3218], [0.0000, -3.1113], [0.0000, -7.5113],
                       [2.2000, -11.3218], [6.5557, -11.9446], [7.6945, -7.6945], [10.8058, -10.8058],
                       [11.9446, -6.5557]]
    for i in range(players):
        if i < len(xjhdexters_data):
            sx = float(xjhdexters_data[i][0]) * (float(home_world_distance) / 10.0)
            sy = float(xjhdexters_data[i][1]) * (float(home_world_distance) / 10.0)
            home_star_points.append((sx, sy))
    return home_star_points


# home_star_distance = 16 for medium distance (divides distance by 2 within function)
def create_home_star_points_hexgrid(home_star_distance, players):
    home_star_points = []
    home_star_distance = float(home_star_distance) / 2
    angles = range(0, 360, 60)
    sx = 0
    sy = 0

    home_star_points.append((sx, sy))
    for player in range(players - 1):
        # find the next home star position
        # put it one homeStarDistance/2 step away from an existing home star
        # in a direction from the angles list
        found = False
        while not found:
            angle = float(random.choice(angles))
            if len(home_star_points):
                rs = random.choice(home_star_points)
                sx = rs[0]
                sy = rs[1]

            sx, sy = step_distance_angle(sx, sy, home_star_distance, math.radians(angle))

            overlap = False
            for hs in home_star_points:
                if math.isclose(sx, hs[0], abs_tol=0.1) and math.isclose(sy, hs[1], abs_tol=0.1):
                    overlap = True

            if not overlap:
                found = True

        home_star_points.append((sx, sy))

    return home_star_points


# Unfinished
def create_home_star_points_circle(distance, players):
    home_star_points = []
    # this is the circumradius of a regular n-gon
    circumradius = (float(distance) / 2) / (2 * math.sin(math.pi / len(players)))
    player_number = 0.0

    for player in players:
        # the next vertex of the regular n-gon that defines the "circle" of home stars
        sx = math.sin(player_number / len(players) * 2 * math.pi) * circumradius
        sy = math.cos(player_number / len(players) * 2 * math.pi) * circumradius

        home_star_points.append(Point(sx, sy, 0))
        player_number += 1

    return home_star_points


# Unfinished
def create_home_star_points_mega_circle(distance, players):
    home_star_points = []

    player_number = 0.0
    circle_number = 0.0

    circumradius = (float(distance) / 2) / (2 * math.sin(math.pi / 8))
    circumradius_circle = (float(distance) * 1.8) / (2 * math.sin(math.pi / 8))

    for player in players:

        csx = math.sin(circle_number / 4 * math.pi) * circumradius_circle
        csy = math.cos(circle_number / 4 * math.pi) * circumradius_circle

        sx = math.sin(player_number / 4 * math.pi) * circumradius
        sy = math.cos(player_number / 4 * math.pi) * circumradius

        sx += csx
        sy += csy

        home_star_points.append(Point(sx, sy, 0))
        player_number += 1

        if not player_number % 8:
            circle_number += 1

    return home_star_points


# Unfinished
def create_home_star_points_mega_grid(distance, players):
    home_star_points = []

    cords = [0, 1, 3, 4, 7, 8, 10, 11]
    scale = 0.66

    for i in cords[:]:
        for j in cords[:]:
            home_star_points.append(Point(i * distance * scale, j * distance * scale, 0))

    rotated_points = []
    a = 0.7853
    center = 4.5 * distance
    for p in home_star_points:
        nx = center + (p.x - center) * math.cos(a) - (p.y - center) * math.sin(a);
        ny = center + (p.x - center) * math.sin(a) + (p.y - center) * math.cos(a);
        rotated_points.append(Point(nx, ny, 0))

    return rotated_points


# Unfinished: hs = Home Star, hsd = Home Star Distance, spp = Stars Per Player
def create_player_stars_twin_ring(hs, hsd, spp):
    # note: we are going to generate the stars per player but this ignores the
    # players home star in the centre. Galaxies that use this scatter
    # technique will have an extra star per player.
    player_stars = []
    home_star_distance = float(hsd)

    inner_count = int(float(spp) / 3)
    outer_count = inner_count * 2

    inner_angles = list(frange(0, 360, 360.0 / inner_count))
    outer_angles = list(frange(0, 360, 360.0 / outer_count))

    for i in xrange(inner_count):
        x, y = step_distance_angle(hs.x, hs.y, home_star_distance / 10, math.radians(inner_angles[i]))
        player_stars.append(Point(x, y, 30))

    for i in xrange(outer_count):
        x, y = step_distance_angle(hs.x, hs.y, home_star_distance / 5, math.radians(outer_angles[i]))
        player_stars.append(Point(x, y, 10))

    return player_stars


# Unfinished: hs = Home Star, hsd = Home Star Distance, spp = Stars Per Player,
# kind = galaxy type, ss = Starting Stars
def create_player_stars_random_splatter(universe, hs, hsd, spp, kind, ss):
    player_stars = []
    if kind == "circular":
        circumradius = (float(hsd) / 2) / (2 * math.sin(math.pi / len(universe.players.values())))

    angles = range(0, 720, 5)
    random.shuffle(angles)

    hsd = float(hsd)

    distance_step = (hsd + 1.0) / 2.0 / float(spp)
    distances = range(150, int(hsd / 2.0 * 1000) + 1000, int(distance_step * 1000))

    from_center = False

    for i in range(spp - 1):
        if kind != "circular":
            # or if not circular
            from_center = False

        if len(player_stars) < ss:
            # while still making starting stars, we won't throw from the centre.
            from_center = False

        throw_angle = math.radians(random.choice(angles))

        if from_center:
            # every second star is thrown from the centre of the map, not from the home star.
            # the distance is 0 to 1.5 * the radius of the circle
            d = random.random() * circumradius * 1.5
            x, y = step_distance_angle(0, 0, d, throw_angle)
            from_center = False
        else:
            d = float(distances[len(player_stars)]) / 1000
            x, y = step_distance_angle(hs.x, hs.y, d, throw_angle)
            from_center = True

        player_stars.append((x, y))

        # first we must test against all stars created so far.
        # min_dist_squared = 0.01
        # add_star_ok = True
        # for s in universe.stars.values() + player_stars[:]:
        #     dist = abs(((s.x - x)*(s.x - x)) + ((s.y - y)*(s.y - y)))
        #     if dist < min_dist_squared:
        #         add_star_ok = False
        #         continue

        # if add_star_ok:

    return player_stars


# Find credentials for given game from credentials.json
def credentials(game_name):
    with open('game_data/credentials.json', 'r') as f:
        creds = json.load(f)[game_name]
        game_number = creds['game_num']
        api_key = creds['api_key']
        return game_number, api_key


# Add new game credentials to credentials.json file,
# also used to check if a game's creds are stored already
def add_new_credentials(game_number, api_key=None):
    name = call_api(game_number, api_key)['name'].lower().replace(' ', '_')
    if not os.path.exists('game_data/credentials.json'):
        with open('game_data/credentials.json', 'x') as f:
            blank_json = {}
            json.dump(blank_json, f)
    with open('game_data/credentials.json') as f:
        cred_json = json.load(f)
    if name not in cred_json:
        cred_json[name] = {'game_num': game_number, 'api_key': None}
        if api_key:
            cred_json[name]['api_key'] = api_key
        with open('game_data/credentials.json', 'w') as f:
            json.dump(cred_json, f, indent=4)
        return cred_json[name]
    else:
        return None
