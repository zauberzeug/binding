from binding import BindableProperty

class A:

    x = BindableProperty()

    def __init__(self, x, y):

        self.x = x
        self.y = y

    @property
    def x(self):

        return self._x

    @x.setter
    def x(self, x):

        self._x = x

def test_nesting():

    a1 = A(1, 2)
    a1.x.bind_to(a1.y)
    assert a1.x == 1 and a1.y == 1

    a2 = A(1, 2)
    a2.x.bind_from(a2.y)
    assert a2.x == 2 and a2.y == 2

    a3 = A(1, 2)
    a3.x.bind(a3.y)
    assert a3.x == 2 and a3.y == 2
