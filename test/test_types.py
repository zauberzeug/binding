from binding import BindableProperty

class A:

    x = BindableProperty()
    y = BindableProperty()

    def __init__(self, x, y):

        self.x = x
        self.y = y

def test_types():

    a = A(True, False)
    # a.x.bind_to(a.y) # TODO: not working
    # assert a.x == a.y
