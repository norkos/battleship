import pytest

from main import MyGrid, EnemyGrid, Destroyer


def test_my_grid_hit():
    # given
    grid = MyGrid()
    x = 3
    y = 2

    # when
    grid.hit(x, y)

    # then
    assert 1 == grid.matrix[y][x]
    assert 0 == grid.matrix[x][y]


def test_my_grid_miss():
    # given
    grid = MyGrid()
    x = 3
    y = 2

    # when
    grid.miss(x, y)

    # then
    assert -1 == grid.matrix[y][x]
    assert 0 == grid.matrix[x][y]


def test_enemy_grid_add_ship_horizontally():
    # given
    grid = EnemyGrid()
    ship = Destroyer()
    x = 3
    y = 3

    # when
    result = grid.add_ship_horizontally(ship, x, y)

    # then
    for dx in range(ship.squares):
        assert 1 == grid.matrix[y][x + dx]

    assert result


def test_enemy_grid_no_space_to_add_ship_horizontally():
    # given
    grid = EnemyGrid()
    ship = Destroyer()
    x = 3
    y = 3
    grid.add_ship_horizontally(ship, x, y)

    # when
    x = x + 1
    result = grid.add_ship_horizontally(ship, x, y)

    # then
    assert 0 == grid.matrix[y][x + ship.squares]
    assert False == result


def test_enemy_grid_add_ship_vertically():
    # given
    grid = EnemyGrid()
    ship = Destroyer()
    x = 3
    y = 3

    # when
    result = grid.add_ship_vertically(ship, x, y)

    # then
    for dy in range(ship.squares):
        assert 1 == grid.matrix[y + dy][x]


def test_enemy_grid_no_space_to_add_ship_vertically():
    # given
    grid = EnemyGrid()
    ship = Destroyer()
    x = 3
    y = 3
    grid.add_ship_vertically(ship, x, y)

    # when
    y = y + 1
    result = grid.add_ship_vertically(ship, x, y)

    # then
    assert 0 == grid.matrix[y + ship.squares][x]
    assert False == result


def test_hit_and_miss():
    # given
    grid = EnemyGrid()
    ship = Destroyer()
    x = 0
    y = 0
    grid.add_ship_horizontally(ship, x, y)

    # when
    hit = grid.hit(x, y)
    miss = grid.hit(x, y + 1)

    # then
    assert hit
    assert -1 == grid.matrix[y][x]
    assert False == miss
    assert 0 == grid.matrix[y + 1][x]


def test_is_over():
    # given
    grid = EnemyGrid()
    ship = Destroyer()
    x = 0
    y = 0
    grid.add_ship_horizontally(ship, x, y)

    # when
    for dx in range(ship.squares):
        grid.hit(x + dx, y)

    assert grid.is_over()
