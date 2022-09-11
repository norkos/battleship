import pprint
from random import randrange, choice

DIM = 10


class Battleship:
    squares = 5


class Destroyer:
    squares = 4


class MyGrid:
    def __init__(self):
        self.matrix = [[0] * DIM for _ in range(DIM)]

    def hit(self, x, y):
        self.matrix[y][x] = 1

    def miss(self, x, y):
        self.matrix[y][x] = -1

    def print(self):
        pprint.pprint(self.matrix)


class EnemyGrid:
    def __init__(self):
        self.matrix = [[0] * DIM for _ in range(DIM)]

    def add_ship_horizontally(self, ship, x, y):
        if x + ship.squares >= DIM:
            return self.add_ship(ship)

        for dx in range(ship.squares):
            if self.matrix[y][x + dx] == 1:
                return False

        for dx in range(ship.squares):
            self.matrix[y][x + dx] = 1

        return True

    def add_ship_vertically(self, ship, x, y):
        if y + ship.squares >= DIM:
            return self.add_ship(ship)

        for dy in range(ship.squares):
            if self.matrix[y + dy][x] == 1:
                return False

        for dy in range(ship.squares):
            self.matrix[y + dy][x] = 1

    def add_ship(self, ship):
        x = randrange(DIM)
        y = randrange(DIM)
        horizontal = choice([True, False])

        if horizontal:
            return self.add_ship_horizontally(ship, x, y)
        else:
            return self.add_ship_vertically(ship, x, y)

    def hit(self, x, y):
        if x > DIM or y > DIM:
            return False

        if self.matrix[y][x] == 1:
            self.matrix[y][x] = -1
            return True

        return False

    def is_over(self):
        if not any(1 in x for x in self.matrix):
            return True
        return False

    def print(self):
        pprint.pprint(self.matrix)


class Game:
    enemy = EnemyGrid()
    my_grid = MyGrid()

    def start(self):
        #todo: check if cannot be added
        self.enemy.add_ship(Destroyer())
        self.enemy.add_ship(Destroyer())
        self.enemy.add_ship(Battleship())

    def hit(self, x, y):
        hit = self.enemy.hit(x, y)

        if hit:
            print("Yeah !!")
            self.my_grid.hit(x, y)

            if self.enemy.is_over():
                print("You won, congratulation !")
        else:
            print("Not this time !!")
            self.my_grid.miss(x, y)

        self.my_grid.print()


if __name__ == '__main__':
    g = Game()
    g.start()
    while True:
        var = input("Please enter XY or end to finish: ")
        g.hit(int(var[0]), int(var[1]))
        if var == 'end':
            break
