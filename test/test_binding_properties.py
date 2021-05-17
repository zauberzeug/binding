from binding import BindableProperty

class Car:

    age = BindableProperty()
    color = BindableProperty()
    weight = BindableProperty()

    def __init__(self, age, color, weight):

        self.age = age
        self.color = color
        self.weight = weight

def test_bindables():

    car1 = Car(10, 'red', 1200)
    car2 = Car(20, 'blue', 1500)
    assert(car1.age == 10 and car2.age == 20)
    assert(car1.color == 'red' and car2.color == 'blue')
    assert(car1.weight == 1200 and car2.weight == 1500)

    car1.age += 1
    assert(car1.age == 11 and car2.age == 20)

    car1.age.bind_to(car2.age)
    assert(car1.age == 11 and car2.age == 11)

    car1.age += 1
    assert(car1.age == 12 and car2.age == 12)

    car1.color.bind_from(car2.color)
    assert(car1.color == 'blue' and car2.color == 'blue')

    car1.weight.bind(car2.weight)
    assert(car1.weight == 1500 and car2.weight == 1500)

    car2.weight = 1000
    assert(car1.weight == 1000 and car2.weight == 1000)

    car1.weight = 1400
    assert(car1.weight == 1400 and car2.weight == 1400)
