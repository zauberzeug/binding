import pytest
from binding import BindableProperty, Binding

class Temperature:

    c = BindableProperty()
    f = BindableProperty()

    def __init__(self):

        self.c = 0.0
        self.f = 0.0
        self.k = 0.0

def test_forward():

    t = Temperature()
    t.c.bind_to(t.f, forward=lambda c: c * 1.8 + 32)
    assert t.c == 0.0 and t.f == 32.0

    t.c = 20.0
    assert t.c == 20.0 and t.f == 68.0

    t.f = 32.0
    assert t.c == 20.0 and t.f == 32.0

def test_backward():

    t = Temperature()
    t.c.bind_from(t.f, backward=lambda f: (f - 32) / 1.8)
    assert t.c == pytest.approx(-17.77778) and t.f == 0.0

    t.f = 68.0
    assert t.c == 20.0 and t.f == 68.0

    t.c = 0.0
    assert t.c == 0.0 and t.f == 68.0

def test_2way():

    t = Temperature()
    t.c.bind_2way(t.f, forward=lambda c: c * 1.8 + 32, backward=lambda f: (f - 32) / 1.8)
    assert t.c == 0.0 and t.f == 32.0

    t.f = 68.0
    assert t.c == 20.0 and t.f == 68.0

    t.c = 0.0
    assert t.c == 0.0 and t.f == 32.0

def test_forward_normal():

    t = Temperature()
    t.c.bind_to(t.k, forward=lambda c: c + 273.15)
    assert t.c == 0.0 and t.k == 273.15

    t.c = 20.0
    assert t.c == 20.0 and t.k == 293.15

    t.k = 0
    assert t.c == 20.0 and t.k == 0.0

def test_backward_normal():

    t = Temperature()
    t.c.bind_from(t.k, backward=lambda k: k - 273.15)
    assert t.c == -273.15 and t.k == 0.0

    t.k = 293.15
    assert t.c == -273.15 and t.k == 293.15

    Binding.update()
    assert t.c == 20.0 and t.k == 293.15

    t.c = 0.0
    assert t.c == 0.0 and t.k == 293.15

def test_2way_normal():

    Binding.reset()  # TODO: how to avoid this line?

    t = Temperature()
    t.c.bind_2way(t.k, forward=lambda c: c + 273.15, backward=lambda k: k - 273.15)
    assert t.c == 0.0 and t.k == 273.15

    t.c = 20.0
    assert t.c == 20.0 and t.k == 293.15

    t.k = 0.0
    assert t.c == 20.0 and t.k == 0.0

    Binding.update()
    assert t.c == -273.15 and t.k == 0.0
