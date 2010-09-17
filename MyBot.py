from planetwars import BaseBot, Game
from planetwars.universe2 import Universe2
from planetwars.planet2 import Planet2
from planetwars.universe import player
from logging import getLogger, sys
import copy
from copy import copy
import random


log = getLogger(__name__)

# template/example of a new bot
# ready to go - just customize do_turn()

class MyBot(BaseBot):


    def do_turn(self):
        log.info("I'm starting my turn %s" % self.universe.game.turn_count)

        for p in self.universe.my_planets:
            if p.ship_count > 50 and len(self.universe.not_my_planets) > 0:
                log.debug("Attacking from %s" % p)
                p.send_fleet(random.choice(list(self.universe.not_my_planets)), p.ship_count / 2)


Game(MyBot, universe_class=Universe2, planet_class=Planet2)
