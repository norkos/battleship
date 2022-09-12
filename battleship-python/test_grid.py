from main import Cruiser, Battleship, Ocean


def test_add_ships_without_overlapping():
    #   given
    a = Cruiser()
    b = Battleship()
    c = Battleship()
    grid = Ocean(10)

    #   when
    assert grid.add_ship(a, 0, 0, True)
    assert grid.add_ship(b, 3, 0, True)
    assert grid.add_ship(c, 4, 0, False) is False


def test_cannot_add_vertically():
    #   given
    a = Cruiser()
    grid = Ocean(10)

    #   when
    assert grid.add_ship(a, 9, 0, True) is False


def test_cannot_add_horizontally():
    #   given
    a = Cruiser()
    grid = Ocean(10)

    #   when
    assert grid.add_ship(a, 0, 9, False) is False
