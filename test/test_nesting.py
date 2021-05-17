from binding import BindableProperty

class A:

    x = BindableProperty()

    def __init__(self, x):

        self.x = x

    def bind_x_to(self, target):

        self.x.bind_to(target, nesting=1)

class B:

    y = BindableProperty()

    def __init__(self, y):

        self.y = y

def test_nesting():

    a = A(1)
    b = B(2)

    a.bind_x_to(b.y)
    assert a.x == 1 and b.y == 1
