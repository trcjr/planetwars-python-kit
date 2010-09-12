# vim:ts=4:shiftwidth=4:et
from planetwars.player import PLAYER_MAP
from planetwars.util import Point, TypedSetBase
from math import ceil, sqrt
from copy import copy
import player

class Planet(object):
    def __init__(self, universe, id, x, y, owner, ship_count, growth_rate):
        self.universe = universe
        self.id = int(id)
        self.position = Point(float(x), float(y))
        self.owner = PLAYER_MAP.get(int(owner))
        self.ship_count = int(ship_count)
        self.growth_rate = int(growth_rate)

    def __repr__(self):
        return "<P(%d)@%s #%d +%d>" % (self.id, self.position, self.ship_count, self.growth_rate)

    def update(self, owner, ship_count):
        self.owner = PLAYER_MAP.get(int(owner))
        self.ship_count = int(ship_count)

    def distance(self, other):
        dx = self.position.x - other.position.x
        dy = self.position.y - other.position.y
        return int(ceil(sqrt(dx ** 2 + dy ** 2)))

    __sub__ = distance

    @property
    def attacking_fleets(self):
        """Hostile (as seen from this planets owner) fleets en-route to this planet."""
        return self.universe.find_fleets(destination=self, owner=player.EVERYBODY - self.owner)

    @property
    def reinforcement_fleets(self):
        """Friendly (as seen from this planets owner) fleets en-route to this planet."""
        return self.universe.find_fleets(destination=self, owner=self.owner)

    @property
    def sent_fleets(self):
        """Fleets owned by this planets owner sent from this planet."""
        return self.universe.find_fleets(source=self, owner=self.owner)

    def send_fleet(self, target, ship_count):
        """Sends a fleet to target. Also accepts a set of targets."""
        if isinstance(target, set):
            if self.ship_count >= ship_count * len(target):
                self.universe.send_fleet(self, target, ship_count)
            return
        if self.ship_count >= ship_count:
            self.universe.send_fleet(self, target, ship_count)

    def in_future(self, turns=1):
        """Calculates state of planet in `turns' turns."""
        planet = copy(self)

        arriving_fleets = self.universe.find_fleets(destination=self)

        for i in range(1, turns+1):
            # account planet growth
            if planet.owner != player.NOBODY:
                planet.ship_count = planet.ship_count + self.growth_rate

            # get fleets which will arrive in that turn
            fleets = [ x for x in arriving_fleets if x.turns_remaining == i ]

            # assuming 2-player scenario!
            ships = []
            for id in [1,2]:
                count = sum( [ x.ship_count for x in fleets if x.owner == PLAYER_MAP.get(int(id)) ] )
                if PLAYER_MAP[id] == planet.owner:
                    count += planet.ship_count

                if count > 0:
                    ships.append({'player':PLAYER_MAP.get(id), 'ships':count})

            # neutral planet has own fleet
            if planet.owner == player.NOBODY:
                ships.append({'player':player.NOBODY,'ships':planet.ship_count})

            # calculate outcome
            if len(ships) > 1:
                s = sorted(ships, key=lambda s : s['ships'], reverse=True)

                winner = s[0]
                second = s[1]

                if winner['ships'] == second['ships']:
                    planet.owner=player.NOBODY
                    planet.ship_count=0
                else:
                    planet.owner=winner['player']
                    planet.ship_count=winner['ships'] - second['ships']

        return planet

class Planets(TypedSetBase):
    accepts = (Planet, )
