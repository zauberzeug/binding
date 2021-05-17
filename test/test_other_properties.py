from binding import BindableProperty, update

class A:

    x = BindableProperty()

    def __init__(self, x):

        self.x = x

class B:

    def __init__(self, x):

        self.x = x

def test_forward():

    a = A(10)
    b = B(20)

    a.x.bind_to(b.x)
    assert a.x == 10 and b.x == 10

    a.x += 1
    assert a.x == 11 and b.x == 11

    b.x += 1
    assert a.x == 11 and b.x == 12

def test_backward():

    a = A(10)
    b = B(20)

    a.x.bind_from(b.x)
    assert a.x == 20 and b.x == 20

    b.x += 1
    assert a.x == 20 and b.x == 21

    update()
    assert a.x == 21 and b.x == 21

    a.x += 1
    assert a.x == 22 and b.x == 21

    update()
    assert a.x == 21 and b.x == 21

def test_two_way():

    a = A(10)
    b = B(20)

    a.x.bind(b.x)
    assert a.x == 20 and b.x == 20

    a.x += 1
    assert a.x == 21 and b.x == 21

    b.x += 1
    assert a.x == 21 and b.x == 22

    update()
    assert a.x == 22 and b.x == 22
