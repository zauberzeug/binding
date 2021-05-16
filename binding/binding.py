#!/usr/bin/env python3
from collections import defaultdict
import inspect
from executing import Source

def get_argument():

    callFrame = inspect.currentframe().f_back.f_back
    callNode = Source.executing(callFrame).node
    source = Source.for_frame(callFrame)
    expression = source.asttokens().get_text(callNode.args[0])

    word, expression = expression.split('.', 1)
    obj = callFrame.f_locals[word]
    while '.' in expression:
        word, expression = expression.split('.', 1)
        obj = getattr(obj, word)

    return obj, expression

class Binding:

    b2b_bindings = defaultdict(list)  # NOTE: bindable to bindable properties
    b2n_bindings = defaultdict(list)  # NOTE: bindable to normal properties
    n2b_bindings = defaultdict(list)  # NOTE: normal to bindable properties

    @staticmethod
    def update():

        for (obj, name), targets in Binding.n2b_bindings.items():
            for target, transform in targets:
                value = transform(getattr(obj, name))
                if target.prop.__get__(target.owner) != value:
                    target.prop.__set__(target.owner, value)

    @staticmethod
    def reset():

        Binding.b2b_bindings.clear()
        Binding.b2n_bindings.clear()
        Binding.n2b_bindings.clear()

class BindableObject:

    def bind_to(self, target, forward=lambda x: x):

        value = forward(self.prop.__get__(self.owner).value)

        if isinstance(target, BindableObject):
            Binding.b2b_bindings[self.prop].append((target, forward))
            target.prop.__set__(target.owner, value)
        else:
            obj, name = get_argument()
            Binding.b2n_bindings[self.prop].append((obj, name, forward))
            setattr(obj, name, value)

    def bind_from(self, source, backward=lambda x: x):

        if isinstance(source, BindableObject):
            value = backward(source.prop.__get__(source.owner).value)
            Binding.b2b_bindings[source.prop].append((self, backward))
            self.prop.__set__(self.owner, value)
        else:
            obj, name = get_argument()
            Binding.n2b_bindings[(obj, name)].append((self, backward))
            self.prop.__set__(self.owner, backward(source))

    def bind_2way(self, other, forward=lambda x: x, backward=lambda x: x):

        value = forward(self.prop.__get__(self.owner).value)

        if isinstance(other, BindableObject):
            Binding.b2b_bindings[self.prop].append((other, forward))
            Binding.b2b_bindings[other.prop].append((self, backward))
            other.prop.__set__(other.owner, value)
        else:
            obj, name = get_argument()
            Binding.b2n_bindings[self.prop].append((obj, name, forward))
            Binding.n2b_bindings[(obj, name)].append((self, backward))
            setattr(obj, name, value)

class BindableProperty:

    def __set_name__(self, _, name):

        self.name = name

    def __get__(self, owner, _=None):

        value = getattr(owner, '_' + self.name)
        bindable = type('', (type(value), BindableObject), {})(value)
        bindable.value = value
        bindable.owner = owner
        vars(bindable)['prop'] = self
        return bindable

    def __set__(self, owner, value):

        setattr(owner, '_' + self.name, value)
        for target, forward in Binding.b2b_bindings[self]:
            if target.prop.__get__(target.owner) != forward(value):
                target.prop.__set__(target.owner, forward(value))
        for obj, name, forward in Binding.b2n_bindings[self]:
            if getattr(obj, name) != forward(value):
                setattr(obj, name, forward(value))
