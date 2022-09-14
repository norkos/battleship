from abc import abstractmethod, ABC
from random import randrange, choice
import pprint
import logging

logging.basicConfig(level=logging.INFO)


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y


class Ship(ABC):

    def __init__(self, size: int) -> None:
        self.squares = size
        self.points = set()
        self.health_check = size

    def hit(self, x: int, y: int) -> bool:
        if Point(x, y) in self.points:
            self.health_check -= 1
            return True

        return False

    def is_ship_still_alive(self) -> bool:
        return self.health_check != 0

    def is_collision(self, ship: int) -> bool:
        return bool(self.points & ship.points)

    def move(self, x: int, y: int, is_horizontal: bool) -> None:
        dx = 1 if is_horizontal else 0
        dy = 0 if is_horizontal else 1

        for i in range(self.squares):
            self.points.add(Point(x + i * dx, y + i * dy))

    def undock(self) -> None:
        self.points.clear()

    @abstractmethod
    def bye_bye(self) -> str:
        pass


class Cruiser(Ship):

    def __init__(self) -> None:
        super().__init__(3)

    def bye_bye(self) -> str:
        return "Cruiser is down !"


class Battleship(Ship):

    def __init__(self) -> None:
        super().__init__(5)

    def bye_bye(self) -> str:
        return "Battleship is down !"


class Destroyer(Ship):

    def __init__(self) -> None:
        super().__init__(4)

    def bye_bye(self) -> str:
        return "Destroyer is down !"


class Ocean:

    def __init__(self, size: int) -> None:
        self.size = size
        self.ships = []

    def attack(self, x: int, y: int) -> bool:
        for ship in self.ships:
            if ship.hit(x, y):
                if not ship.is_ship_still_alive():
                    logging.info(ship.bye_bye())
                return True

        return False

    def add_ship(self, ship: Ship, x: int, y: int, is_horizontal: bool) -> bool:

        if is_horizontal and x + ship.squares >= self.size:
            logging.debug(f"No place for the ship horizontally: {x} {y}")
            return False

        if not is_horizontal and y + ship.squares >= self.size:
            logging.debug(f"No place for the ship vertically: {x} {y}")
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
    def __init__(self, size: int) -> None:
        self.matrix = [[0] * size for _ in range(size)]

    def hit(self, x: int, y: int):
        self.matrix[y][x] = 1

    def miss(self, x: int, y: int):
        self.matrix[y][x] = -1

    def print(self) -> None:
        pprint.pprint(self.matrix)


class Game:

    def __init__(self, size: int) -> None:
        self.size = size
        self.ocean = Ocean(size)
        self.grid = Grid(size)

    def add_ship_randomly(self, ship: Ship) -> bool:
        retries = 10
        for i in range(retries):
            x = randrange(self.size)
            y = randrange(self.size)
            is_horizontal = choice([True, False])
            if self.ocean.add_ship(ship, x, y, is_horizontal):
                logging.debug(f"Ship moved at {x}, {y}")
                return True

        logging.warning(f"Cannot add ship after {retries} retries")
        return False

    def start(self) -> bool:
        return self.add_ship_randomly(Destroyer()) \
               and self.add_ship_randomly(Destroyer()) \
               and self.add_ship_randomly(Battleship())

    def hit(self, x: int, y: int) -> None:
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

    print(f"Welcome to the Battleship game, your grid is {grid_size}x{grid_size}")
    while started:
        try:
            x, y = [int(a) for a in input("Please enter X Y or type 'end' to finish: ").split()]
            g.hit(x, y)
        except ValueError:
            print("Thank you and bye bye")
            started = False
        except:
            print("Wrong input, try again like: 2 2")

