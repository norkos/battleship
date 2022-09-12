from main import Cruiser


def test_is_hit():
    # given
    ship_size = 3
    ship = Cruiser()

    # when
    x = 2
    y = 3
    horizontal = True
    ship.move(x, y, horizontal)

    # then
    for dx in range(ship_size):
        assert ship.is_ship_still_alive()
        assert ship.hit(x + dx, y)

    assert ship.is_ship_still_alive() is False
    assert ship.hit(y, x) is False


def test_collision():
    # given
    first_ship = Cruiser()
    x = 1
    y = 1
    horizontal = False
    first_ship.move(x, y, horizontal)

    # when
    x = 0
    y = 2
    horizontal = True
    second_ship = Cruiser()
    second_ship.move(x, y, horizontal)

    # then
    assert first_ship.is_collision(second_ship)


def test_no_collision():
    # given
    first_ship = Cruiser()
    x = 1
    y = 1
    horizontal = False
    first_ship.move(x, y, horizontal)

    # when
    x = 2
    y = 1
    horizontal = False
    second_ship = Cruiser()
    second_ship.move(x, y, horizontal)

    # then
    assert first_ship.is_collision(second_ship) is False
