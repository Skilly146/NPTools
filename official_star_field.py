import random
import math
import logging
import json

# import urllib
# from google.appengine.api import urlfetch
# 
# import star_field_custom
#
# from starnames import *
# from star import *
# from fleet import *
# from player import *
# from utils import *

from collections import namedtuple

Point = namedtuple('Point', 'x y z')


def frange(start, stop = None, step = 1):
    """frange generates a set of floating point values over the
    range [start, stop) with step size step

    frange([start,] stop [, step ])"""

    if stop is None:
        for x in _xrange(int(ceil(start))):
            yield x
    else:
        # create a generator expression for the index values
        indices = (i for i in xrange(0, int((stop-start)/step)))
        # yield results
        for i in indices:
            yield start + step*i


def center_galaxy(universe, with_offset=True):
    # center the map in the universe
    min_x = 1000
    min_y = 1000
    max_x = -1000
    max_y = -1000
    for s in universe.stars.values():
        if s.x < min_x:
            min_x = s.x
        if s.y < min_y:
            min_y = s.y
        if s.x > max_x:
            max_x = s.x
        if s.y > max_y:
            max_y = s.y

    mid_x = (max_x + min_x) / 2
    mid_y = (max_y + min_y) / 2

    if with_offset:
        mid_x += random.randint(-2, 2)
        mid_y += random.randint(-2, 2)

    dif_x = 0 - mid_x
    dif_y = 0 - mid_y

    for s in universe.stars.values():
        s.x += dif_x
        s.y += dif_y
    for f in universe.fleets.values():
        f.x += dif_x
        f.y += dif_y


def create_wormholes(universe, count, mirror):
    if mirror:
        return

    gate_count = 0
    all_stars = []

    for star in universe.stars.values():
        # make sure we don't build wormholes in the players starting empire.
        if star.player is None:
            all_stars.append(star)

    while gate_count < count:
        star = random.choice(all_stars)
        target = random.choice(all_stars)
        dist = distance(star.x, star.y, target.x, target.y)
        if (dist > 2):
            star.wormhole = target
            target.wormhole = star

            star.resources = 5
            target.resources = 5

            all_stars.remove(star)
            all_stars.remove(target)

            if len(all_stars) < 2:
                return

            gate_count += 1


def init_all_stars(universe):
    for star in universe.stars.values():
        star.update_scanned()


def set_resources(star, level, fixed=0):
    if fixed > 0:
        star.resources = fixed
        star.natural = star.resources
        return star

    star.resources = random.choice([5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 10, 10, 10, 10, 10, 10, 10, 10, 20, 20, 20, 20, 20, 20,  30, 30, 30, 30, 40, 40, 50, 60, 70])
    star.natural = star.resources
    return star


def test_warpgate(star, chance):
    if chance:
        gateRoll = random.randint(0, 99)
        if chance == 1 and gateRoll < 10:
            star.gate = 1
        if chance == 2 and gateRoll < 30:
            star.gate = 1
    return star


def create_home_star_points_quad_flower_64(distance, players):
    home_star_points = []
    xjhdexters_data = [[31.9068,-6.2000],[8.7681,0.0000],[21.1681,0.0000],[31.9068,6.2000],[42.6456,12.4000],[44.9731,24.5796],[54.3572,16.4741],[56.6847,28.6537],[56.2323,41.0455],[44.2548,44.2548],[53.0229,53.0229],[41.0455,56.2323],[28.6537,56.6847],[24.5796,44.9731],[16.4741,54.3572],[12.4000,42.6456],[6.2000,31.9068],[0.0000,8.7681],[0.0000,21.1681],[-6.2000,31.9068],[-12.4000,42.6456],[-24.5796,44.9731],[-16.4741,54.3572],[-28.6537,56.6847],[-41.0455,56.2323],[-44.2548,44.2548],[-53.0229,53.0229],[-56.2323,41.0455],[-56.6847,28.6537],[-44.9731,24.5796],[-54.3572,16.4741],[-42.6456,12.4000],[-31.9068,6.2000],[-8.7681,0.0000],[-21.1681,0.0000],[-31.9068,-6.2000],[-42.6456,-12.4000],[-44.9731,-24.5796],[-54.3572,-16.4741],[-56.6847,-28.6537],[-56.2323,-41.0455],[-44.2548,-44.2548],[-53.0229,-53.0229],[-41.0455,-56.2323],[-28.6537,-56.6847],[-24.5796,-44.9731],[-16.4741,-54.3572],[-12.4000,-42.6456],[-6.2000,-31.9068],[0.0000,-8.7681],[0.0000,-21.1681],[6.2000,-31.9068],[12.4000,-42.6456],[24.5796,-44.9731],[16.4741,-54.3572],[28.6537,-56.6847],[41.0455,-56.2323],[44.2548,-44.2548],[53.0229,-53.0229],[56.2323,-41.0455],[56.6847,-28.6537],[44.9731,-24.5796],[54.3572,-16.4741],[42.6456,-12.4000]]
    for i in xrange(len(players)):
        if i < len(xjhdexters_data):
            sx = float(xjhdexters_data[i][0]) * (float(distance) / 20.0)
            sy = float(xjhdexters_data[i][1]) * (float(distance) / 20.0)
            home_star_points.append(Point(sx, sy, 0))
    return home_star_points


def create_home_star_points_quad_flower_32(distance, players):
    home_star_points = []
    xjhdexters_data = [[11.3218,-2.2000],[3.1113,0.0000],[7.5113,0.0000],[11.3218,2.2000],[11.9446,6.5557],[7.6945,7.6945],[10.8058,10.8058],[6.5557,11.9446],[2.2000,11.3218],[0.0000,3.1113],[0.0000,7.5113],[-2.2000,11.3218],[-6.5557,11.9446],[-7.6945,7.6945],[-10.8058,10.8058],[-11.9446,6.5557],[-11.3218,2.2000],[-3.1113,0.0000],[-7.5113,0.0000],[-11.3218,-2.2000],[-11.9446,-6.5557],[-7.6945,-7.6945],[-10.8058,-10.8058],[-6.5557,-11.9446],[-2.2000,-11.3218],[0.0000,-3.1113],[0.0000,-7.5113],[2.2000,-11.3218],[6.5557,-11.9446],[7.6945,-7.6945],[10.8058,-10.8058],[11.9446,-6.5557]]
    for i in xrange(len(players)):
        if i < len(xjhdexters_data):
            sx = float(xjhdexters_data[i][0]) * (float(distance) / 10.0)
            sy = float(xjhdexters_data[i][1]) * (float(distance) / 10.0)
            home_star_points.append(Point(sx, sy, 0))
    return home_star_points


def create_home_star_points_hexgrid(distance, players):
    home_star_points = []
    distance = float(distance) / 2
    angles = range(0, 360, 60)
    sx = 0
    sy = 0

    home_star_points.append(Point(0, 0, 0))
    for player in players:
        # find the next home star position
        # put it one homeStarDistance/2 step away from an existing home star
        # in a direction from the angles list
        found = False
        while not found:
            angle = float(random.choice(angles))
            if len(home_star_points):
                rs = random.choice(home_star_points)
                sx = rs.x
                sy = rs.y

            sx, sy = step_distance_angle(sx, sy, distance, math.radians(angle))

            overlap = False
            for hs in home_star_points:
                if (floats_nearly_equal(sx, hs.x)) and (floats_nearly_equal(sy, hs.y)):
                    overlap = True

            if not overlap:
                found = True

        home_star_points.append(Point(sx, sy, 0))

    return home_star_points


def create_home_star_points_circle(distance, players):
    home_star_points = []
    # this is the circumradius of a regular n-gon
    circumradius = (float(distance) / 2)/(2*math.sin(math.pi/len(players)))
    player_number = 0.0

    for player in players:
        # the next vertex of the regular n-gon that defines the "circle" of home stars
        sx = math.sin(player_number/len(players)*2*math.pi)*circumradius
        sy = math.cos(player_number/len(players)*2*math.pi)*circumradius

        home_star_points.append(Point(sx, sy, 0))
        player_number += 1

    return home_star_points


def create_home_star_points_mega_circle(distance, players):
    home_star_points = []

    player_number = 0.0
    circle_number = 0.0

    circumradius = (float(distance) / 2)/(2*math.sin(math.pi/8))
    circumradius_circle = (float(distance) * 1.8 )/(2*math.sin(math.pi/8))

    for player in players:

        csx = math.sin(circle_number/4*math.pi)*circumradius_circle
        csy = math.cos(circle_number/4*math.pi)*circumradius_circle

        sx = math.sin(player_number/4*math.pi)*circumradius
        sy = math.cos(player_number/4*math.pi)*circumradius

        sx += csx
        sy += csy

        home_star_points.append(Point(sx, sy, 0))
        player_number += 1

        if not player_number % 8:
            circle_number += 1

    return home_star_points


def create_home_star_points_mega_grid(distance, players):
    home_star_points = []

    cords = [0, 1,  3, 4,   7, 8,  10, 11]
    scale = 0.66

    for i in cords[:]:
        for j in cords[:]:
            home_star_points.append(Point(i*distance*scale, j*distance*scale, 0))

    rotated_points = []
    a = 0.7853
    center = 4.5 * distance
    for p in home_star_points:
        nx = center + (p.x-center)*math.cos(a) - (p.y-center)*math.sin(a);
        ny = center + (p.x-center)*math.sin(a) + (p.y-center)*math.cos(a);
        rotated_points.append(Point(nx, ny, 0))

    return rotated_points


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
        x, y = step_distance_angle(hs.x, hs.y, home_star_distance / 5 , math.radians(outer_angles[i]))
        player_stars.append(Point(x, y, 10))

    return player_stars


def create_player_stars_random_splatter(universe, hs, hsd, spp, kind, ss):
    player_stars = []
    if kind == "circular":
        circumradius = (float(hsd)/2)/(2*math.sin(math.pi/len(universe.players.values())))

    angles = range(0, 720, 5)
    random.shuffle(angles)

    hsd = float(hsd)

    distance_step = (hsd + 1.0) / 2.0 / float(spp)
    distances = range(150, int(hsd / 2.0 * 1000) + 1000, int(distance_step * 1000))

    from_center = False

    for i in xrange(spp-1):
        if kind != "circular":
            # or if not circular
            from_center = False

        if len(player_stars) < ss:
            # while still making starting stars, we wont throw from the centre.
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

        player_stars.append(Point(x, y, 0))

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


def create_name_list(config):
    names = []

    if True:
        raw_starnames = list(starnames)
        selection_pool = list(starnames)
        prependor = list(preplacenames)

    names = []
    names_required = (config["starsPerPlayer"] + 1 ) * (config["players"] + 1)
    if config["mirror"]:
        names_required *= 2

    while len(names) < names_required:
        if not len(selection_pool):
            selection_pool = list(raw_starnames)
        new_name = random.choice(selection_pool)
        selection_pool.remove(new_name)
        if new_name not in names:
            names.append(new_name)
            continue
        else:
            new_name =  random.choice(prependor)  + " " + new_name
            if new_name not in names:
                names.append(new_name)

    random.shuffle(names)
    return names


def create_starfield(universe, config):

    if config["starfield"] == "custom":
        custom = None
        try:
            custom = json.loads(config["customStarfield"])
            star_field_custom.create(universe, custom)
            init_all_stars(universe)

        except Exception:
            logging.error("Failed to Create Custom Star-field")
            logging.error(config["customStarfield"])
            return False
        return True

    universe.stars = {}
    names = create_name_list(config)

    players = universe.players.values()
    random.shuffle(players)

    # create a list of points for each players home star
    home_star_points = []
    if config["starfield"] == "mega_circle":
        home_star_points = create_home_star_points_mega_circle(config["homeStarDistance"], players)

    if config["starfield"] == "mega_grid":
        home_star_points = create_home_star_points_mega_grid(config["homeStarDistance"], players)

    if config["starfield"] == "circular":
        home_star_points = create_home_star_points_circle(config["homeStarDistance"], players)

    if config["starfield"] == "hexgrid":
        home_star_points = create_home_star_points_hexgrid(config["homeStarDistance"], players)

    if config["starfield"] == "xjhdexters-quad_flower":
        home_star_points = create_home_star_points_quad_flower_64(config["homeStarDistance"], players)

    # create a star object for each point.
    name_index = 0
    home_stars = []
    for player in players:
        r = 50
        e = config["startingInfEconomy"]
        i = config["startingInfIndustry"]
        s = config["startingInfScience"]
        st = config["startingShips"]
        n = names[name_index]
        x = home_star_points[name_index].x
        y = home_star_points[name_index].y

        new_star = universe.create_star(n, x,  y, player, r, e, s, i, st)
        home_stars.append(new_star)
        name_index += 1

        player.home = new_star

    # center the home stars on the origin
    center_galaxy(universe, with_offset=False)

    # for each home star, sprinkle stars around
    for hs in home_stars:
        points = []
        if config["starScatter"] == "twin_ring":
            hsd = config["homeStarDistance"]
            spp = config["starsPerPlayer"]
            points = create_player_stars_twin_ring(hs, hsd, spp)
        else:
            hsd = config["homeStarDistance"]
            spp = config["starsPerPlayer"]
            kind = config["starfield"]
            ss = config["startingStars"] + 1
            points = create_player_stars_random_splatter(universe, hs, hsd, spp, kind, ss)

        for point in points:
            n = names[name_index]
            name_index += 1

            new_star = universe.create_star(n, point.x, point.y, None, 0, 0, 0, 0, 0)
            set_resources(new_star, config["naturalResources"], point.z)
            test_warpgate(new_star, config["randomGates"])

            if config["mirror"]:
                n = names[name_index]
                name_index += 1
                mirror_star = universe.create_star(n, -point.x, -point.y, None, 0, 0, 0, 0, 0)
                mirror_star.natural = new_star.natural
                mirror_star.resources = new_star.resources
                mirror_star.gate = new_star.gate

    # kill all starts that are too close to one another.
    starts_to_remove = []
    min_dist_squared = 0.01
    for star in universe.stars.values():
        for other in universe.stars.values():
            if star == other:
                continue
            dist = abs(((star.x - other.x)*(star.x - other.x)) + ((star.y - other.y)*(star.y - other.y)))
            if dist < min_dist_squared:
                if star not in starts_to_remove:
                    starts_to_remove.append(star)
                if other not in starts_to_remove:
                    starts_to_remove.append(other)

    for star in starts_to_remove:
        if star in home_stars:
            continue
        del universe.stars[star.uid]
    del starts_to_remove

    # for each home star, sort the stars by distance and give the x nearest to the player
    for hs in home_stars:
        starting_star_resource_selection = [20, 10, 30, 40, 10, 40, 10, 20, 40, 50]
        starting_star_counter = 0
        sorted_stars = sorted(universe.stars.values(), key=lambda s: (abs(((s.x - hs.x)*(s.x - hs.x)) + ((s.y - hs.y)*(s.y - hs.y)))), reverse=False)

        sorted_stars = sorted_stars[1:config["startingStars"]]
        for close_star in sorted_stars:
            close_star.player = hs.player
            close_star.strength = config["startingShips"]

            if config["starScatter"] != "twin_ring":
                close_star.resources = starting_star_resource_selection[starting_star_counter]
                close_star.natural = close_star.resources

            starting_star_counter += 1

    center_galaxy(universe)
    create_wormholes(universe, len(universe.players) / 2, config["mirror"])
    init_all_stars(universe)
