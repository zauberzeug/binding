from binding import BindableProperty

class A:

    x = BindableProperty()
    y = BindableProperty()

    def __init__(self, x, y, z):

        self.x = x
        self.y = y
        self.z = z
        self.a = 0

def test_propagation():

    a = A(1, 2, 3)

    a.x.bind(a.z)
    a.y.bind(a.z)

    assert a.x == 3 and a.y == 3 and a.z == 3
