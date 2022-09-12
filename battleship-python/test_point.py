from main import Point


def test_point_to_set():
    # given
    a = Point(1, 2)
    b = Point(1, 2)
    c = Point(1, 3)
    d = Point(2, 2)

    # when
    result = {a, b, c, d}

    # then
    assert 3 == len(result)
