from binding import BindableProperty, update


def test_propagation():

    class A:

        x = BindableProperty()
        y = BindableProperty()
        z = BindableProperty()

        def __init__(self, x, y, z):

            self.x = x
            self.y = y
            self.z = z

    a = A(1, 2, 3)

    a.x.bind_from(a.y)
    a.y.bind_from(a.z)

    assert a.x == a.y == a.z == 3

    a.z = 4

    assert a.x == a.y == a.z == 4


def test_propagation_after_update():

    class A:

        def __init__(self, x, y, z):

            self.x = x
            self.y = y
            self.z = z

    a = A(1, 2, 3)

    a.x.bind_from(a.y)
    a.y.bind_from(a.z)

    assert a.x == a.y == a.z == 3

    a.z = 4

    assert a.x == a.y == 3 and a.z == 4

    update()

    assert a.x == a.y == a.z == 4
