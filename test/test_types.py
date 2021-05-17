from binding import BindableProperty

class A:

    x = BindableProperty()
    y = BindableProperty()

    def __init__(self, x, y):

        self.x = x
        self.y = y

def test_none():

    a = A(None, None)
    a.x.bind(a.y)
    assert a.x == a.y

def test_bool():

    a = A(True, False)
    a.x.bind(a.y)
    assert a.x == a.y

def test_int():

    a = A(1, 2)
    a.x.bind(a.y)
    assert a.x == a.y

def test_float():

    a = A(1.0, 2.0)
    a.x.bind(a.y)
    assert a.x == a.y

def test_str():

    a = A('1', '2')
    a.x.bind(a.y)
    assert a.x == a.y

def test_tuple():

    a = A((1,), (2,))
    a.x.bind(a.y)
    assert a.x == a.y

def test_list():

    a = A([1], [2])
    a.x.bind(a.y)
    assert a.x == a.y

def test_dict():

    a = A({1: 1}, {2: 2})
    a.x.bind(a.y)
    assert a.x == a.y

def test_set():

    a = A({1}, {2})
    a.x.bind(a.y)
    assert a.x == a.y
