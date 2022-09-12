from abc import abstractmethod, ABC
from random import randrange, choice
import pprint
import logging

logging.basicConfig(level=logging.INFO)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Ship(ABC):

    def __init__(self, size):
        self.squares = size
        self.points = set()
        self.health_check = size

    def hit(self, x, y):
        if Point(x, y) in self.points:
            self.health_check -= 1
            return True

        return False

    def is_ship_still_alive(self):
        return self.health_check != 0

    def is_collision(self, ship):
        return len(self.points.intersection(ship.points)) > 0

    def move(self, x, y, is_horizontal):
        dx = 1 if is_horizontal else 0
        dy = 0 if is_horizontal else 1

        for i in range(self.squares):
            self.points.add(Point(x + i * dx, y + i * dy))

    def undock(self):
        self.points.clear()

    @abstractmethod
    def bye_bye(self):
        pass


class Cruiser(Ship):

    def __init__(self):
        super(Cruiser, self).__init__(3)

    def bye_bye(self):
        return "Cruiser is down !"


class Battleship(Ship):

    def __init__(self):
        super(Battleship, self).__init__(5)

    def bye_bye(self):
        return "Battleship is down !"


class Destroyer(Ship):

    def __init__(self):
        super(Destroyer, self).__init__(4)

    def bye_bye(self):
        return "Destroyer is down !"


class Ocean:

    def __init__(self, size):
        self.size = size
        self.ships = []

    def attack(self, x, y):
        for ship in self.ships:
            if ship.hit(x, y):
                if not ship.is_ship_still_alive():
                    logging.info(ship.bye_bye())
                return True

        return False

    def add_ship(self, ship, x, y, is_horizontal):

        if is_horizontal and x + ship.squares >= self.size:
            logging.debug("No place for the ship horizontally: {} {}".format(x, y))
            return False

        if not is_horizontal and y + ship.squares >= self.size:
            logging.debug("No place for the ship vertically: {} {}".format(x, y))
            return False

        ship.move(x, y, is_horizontal)

        for other_ships in self.ships:
            if other_ships.is_collision(ship):
                logging.debug("Cannot add overlapping ship, undocking")
                ship.undock()
                return False

        self.ships.append(ship)

        return True


class Grid:
    def __init__(self, size):
        self.matrix = [[0] * size for _ in range(size)]

    def hit(self, x, y):
        self.matrix[y][x] = 1

    def miss(self, x, y):
        self.matrix[y][x] = -1

    def print(self):
        pprint.pprint(self.matrix)


class Game:

    def __init__(self, size):
        self.size = size
        self.ocean = Ocean(size)
        self.grid = Grid(size)

    def add_ship_randomly(self, ship):
        retries = 10
        for i in range(retries):
            x = randrange(self.size)
            y = randrange(self.size)
            is_horizontal = choice([True, False])
            if self.ocean.add_ship(ship, x, y, is_horizontal):
                logging.debug("Ship moved at {}, {}".format(x, y))
                return True

        logging.warning("Cannot add ship after {} retries".format(retries))
        return False

    def start(self):
        return self.add_ship_randomly(Destroyer()) \
               and self.add_ship_randomly(Destroyer()) \
               and self.add_ship_randomly(Battleship())

    def hit(self, x, y):
        if self.ocean.attack(x, y):
            print("Hit !")
            self.grid.hit(x, y)
        else:
            print("Miss !")
            self.grid.miss(x, y)

        self.grid.print()


if __name__ == '__main__':
    grid_size = 10
    g = Game(grid_size)
    started = g.start()
    if not started:
        logging.warning("Terminated")

    while started:
        var = input("Please enter XY or end to finish: ")
        g.hit(int(var[0]), int(var[1]))
        if var == 'end':
            started = False
