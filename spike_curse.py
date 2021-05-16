#!/usr/bin/env python3
from collections import defaultdict
from forbiddenfruit import curse
import inspect
from executing import Source

bindings = defaultdict(list)

def extract_object(expression, callFrame):

    words = expression.split('.')
    obj = callFrame.f_locals[words.pop(0)]
    while len(words) > 1:
        obj = getattr(obj, words.pop(0))
    return obj, words[0]

def get_argument():

    callFrame = inspect.currentframe().f_back.f_back
    callNode = Source.executing(callFrame).node
    source = Source.for_frame(callFrame)
    expression = source.asttokens().get_text(callNode.args[0])
    return extract_object(expression, callFrame)

def bind_to(self, target):

    expression = inspect.stack()[1].code_context[0].strip().split('.bind_to(')[0]
    callFrame = inspect.currentframe().f_back
    source_obj, source_name = extract_object(expression, callFrame)

    target_obj, target_name = get_argument()
    setattr(target_obj, target_name, self)
    bindings[(source_obj, source_name)].append((target_obj, target_name))

class BindableProperty:

    def __set_name__(self, _, name):

        self.name = name

    def __get__(self, owner, _=None):

        return getattr(owner, '_' + self.name)

    def __set__(self, owner, value):

        setattr(owner, '_' + self.name, value)

        for obj, name in bindings[(owner, self.name)]:
            if getattr(obj, name) != value:
                setattr(obj, name, value)

curse(bool, 'bind_to', bind_to)
curse(type(None), 'bind_to', bind_to)

class A:

    x = BindableProperty()
    y = BindableProperty()

    def __init__(self, x, y):

        self.x = x
        self.y = y

a = A(True, False)
assert a.x == True and a.y == False

a.x.bind_to(a.y)
assert a.x == True and a.y == True

a.x = False
assert a.x == False and a.y == False

b = A(None, False)
assert b.x == None and b.y == False

b.x.bind_to(b.y)
assert b.x == None and b.y == None
