# Binding

This package brings property binding to Python.
It allows you to bind attributes of one object to other attributes of itself or other objects like so:

```Python
label.text.bind(model.value)
```

That means, whenever `model.value` is changed, `label.text` changes as well.

# Installation

This package can be installed using the Python package installer [pip](https://pypi.org/project/pip/):

```bash
python3 -m pip install binding
```

Alternatively you can find the [source code](https://github.com/zauberzeug/binding) on GitHub.

# Usage

You can apply binding in two different ways: automatic updates using bindable properties or by calling an update functional explicitely.
Furthermore, you can specify the binding direction as well as converter functions.

The following examples give a more detailed explanation.
The code snippets build upon each other and are meant to be called in succession.

## Bindable properties

If you have control over the class implementation, you can introduce a `BindableProperty` for the respective attributes. It will intercept each write access the attribute and propagate the changed value to bound properties:

```python
from binding import BindableProperty

class Person:

    name = BindableProperty()

    def __init__(self, name=None):

        self.name = name

class Car:

    driver = BindableProperty()

    def __init__(self, driver=None):

        self.driver = driver

person = Person('Robert')
car = Car()
car.driver.bind(person.name)
assert car.driver == person.name == 'Robert'

person.name = 'Bob'
assert car.driver == person.name == 'Bob'
```

## Binding with non-bindable attributes

Suppose you have a class which you cannot or don't want to change.
That means it has no `BindableProperty` to observe value changes.
You can bind its attributes nevertheless:

```python
class License:

    def __init__(self, name=None):

        self.name = name

license = License()
license.name.bind(person.name)
person.name = 'Todd'
assert license.name == person.name == 'Todd'
```

But if the license name is changed, there is no `BindableProperty` to notice write access to its value.
We have to manually trigger the propagation to bound objects.

```python
from binding import update

license.name = 'Ben'
assert person.name != license.name == 'Ben'

update()
assert person.name == license.name == 'Ben'
```

## One-way binding

The `.bind()` method registers two-way binding.
But you can also specify one-way binding using `.bind_from()` or `.bind_to()`, respectively.
In the following example `car` receives updates `person`, but not the other way around.

```python
person = Person('Ken')
car = Car()

car.driver.bind_from(person.name)
assert car.driver == person.name == 'Ken'

person.name = 'Sam'
assert car.driver == person.name == 'Sam'

car.driver = 'Seth'
assert car.driver != person.name == 'Sam'
```

Likewise you can specify forward binding to let `person` be updated when `car` changes:

```python
person = Person('Keith')
car = Car()

car.driver.bind_to(person.name)
assert car.driver == person.name == None

car.driver = 'Kent'
assert car.driver == person.name == 'Kent'

person.name = 'Grant'
assert car.driver != person.name == 'Grant'
```

## Converters

For all types of binding - forward, backward, two-way, via bindable properties or non-bindable attributes - you can define converter functions that translate values from one side to another.
The following example demonstrates the conversion between Celsius and Fahrenheit.

```python
class Temperature:

    c = BindableProperty()
    f = BindableProperty()

    def __init__(self):

        self.c = 0.0
        self.f = 0.0

t = Temperature()
t.f.bind(t.c, forward=lambda f: (f - 32) / 1.8, backward=lambda c: c * 1.8 + 32)
assert t.c == 0.0 and t.f == 32.0

t.f = 68.0
assert t.c == 20.0 and t.f == 68.0

t.c = 100.0
assert t.c == 100.0 and t.f == 212.0
```

Note that `bind_to()` only needs a `forward` converter.
Similarly `bind_from` has only a `backward` converter.

# Implementation and dependencies

To achieve such a lean API we utilize three main techniques:

- For extending basic types with `bind()`, `bind_to()` and `bind_from()` methods we use `curse` from the [forbiddenfruit](https://pypi.org/project/forbiddenfruit/) package.

- For intercepting write access to attributes we implement `BindableProperties` as [descriptors](https://docs.python.org/3/howto/descriptor.html).

- For finding the object and attribute name of the caller and the argument of our `bind()` methods we use inspection tools from the [inspect](https://docs.python.org/3/library/inspect.html) and [executing](https://pypi.org/project/executing/) packages.
