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

    a.x.bind_2way(a.z)
    a.y.bind_2way(a.z)

    assert a.x == 2 and a.y == 2 and a.z == 2
