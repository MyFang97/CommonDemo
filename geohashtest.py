import geohash2

# Forward and reverse base 32 map
BASESEQUENCE = '0123456789bcdefghjkmnpqrstuvwxyz'
BASE32MAP = dict((k, count) for count, k in enumerate(BASESEQUENCE))
BASE32MAPR = dict((count, k) for count, k in enumerate(BASESEQUENCE))


def adjacent(geohash, direction):
    """Return the adjacent geohash for a given direction."""
    # Based on an MIT licensed implementation by Chris Veness from:
    #   http://www.movable-type.co.uk/scripts/geohash.html
    assert direction in 'nsew', "Invalid direction: %s" % direction
    assert geohash, "Invalid geohash: %s" % geohash
    neighbor = {
        'n': ['p0r21436x8zb9dcf5h7kjnmqesgutwvy', 'bc01fg45238967deuvhjyznpkmstqrwx'],
        's': ['14365h7k9dcfesgujnmqp0r2twvyx8zb', '238967debc01fg45kmstqrwxuvhjyznp'],
        'e': ['bc01fg45238967deuvhjyznpkmstqrwx', 'p0r21436x8zb9dcf5h7kjnmqesgutwvy'],
        'w': ['238967debc01fg45kmstqrwxuvhjyznp', '14365h7k9dcfesgujnmqp0r2twvyx8zb']
    }
    border = {
        'n': ['prxz', 'bcfguvyz'],
        's': ['028b', '0145hjnp'],
        'e': ['bcfguvyz', 'prxz'],
        'w': ['0145hjnp', '028b']
    }
    last = geohash[-1]
    parent = geohash[0:-1]
    t = len(geohash) % 2
    # Check for edge cases
    if (last in border[direction][t]) and (parent):
        parent = adjacent(parent, direction)
    return parent + BASESEQUENCE[neighbor[direction][t].index(last)]


def neighbors(geohash):
    """Return all neighboring geohashes."""
    return {
        'n': adjacent(geohash, 'n'),
        'ne': adjacent(adjacent(geohash, 'n'), 'e'),
        'e': adjacent(geohash, 'e'),
        'se': adjacent(adjacent(geohash, 's'), 'e'),
        's': adjacent(geohash, 's'),
        'sw': adjacent(adjacent(geohash, 's'), 'w'),
        'w': adjacent(geohash, 'w'),
        'nw': adjacent(adjacent(geohash, 'n'), 'w'),
        'c': geohash
    }


def neighborsfit(centroid, points):
    centroid = geohash2.encode(centroid)
    points = map(geohash2.encode, points)
    for i in range(1, len(centroid)):
        g = centroid[0:i]
        n = set(neighbors(g).values())
        unbounded = [point for point in points if (point[0:i] not in n)]
        if unbounded:
            break
    return g[0:-1]


class MyGeohash():

    def ahead(self, geohashstr, index):
        return geohashstr[0:index]

    def myencode(self, latitude, longitude):
        return geohash2.encode(latitude, longitude)

    def mydecode(self, geohashstr):
        return geohash2.decode(geohashstr)

    def getneighbors(self, geohashstr):
        return neighbors(geohashstr)


if __name__ == '__main__':
    myTestGeohash = MyGeohash()
    # wx4g340--
    print(myTestGeohash.getneighbors('wx4g340'))
    print('Geohash for 42.6, -5.6:', geohash2.encode(42.6, -5.6))
    # Geohash for 42.6, -5.6: ezs42e44yx96
    print('Geohash for 42.6, -5.6:', geohash2.encode(42.6, -5.6, precision=5))
    # Geohash for 42.6, -5.6: ezs42
    print('Coordinate for Geohash ezs42:', geohash2.decode('ezs42'))
    # Coordinate for Geohash ezs42: ('42.6', '-5.6')
