#!/usr/bin/env python3
from collections import defaultdict
import inspect
from executing import Source
from forbiddenfruit import curse

def _extract_object(expression, callFrame):

    words = expression.split('.')
    obj = callFrame.f_locals[words.pop(0)]
    while len(words) > 1:
        obj = getattr(obj, words.pop(0))
    return obj, words[0]

def _get_argument():

    callFrame = inspect.currentframe().f_back.f_back
    callNode = Source.executing(callFrame).node
    source = Source.for_frame(callFrame)
    expression = source.asttokens().get_text(callNode.args[0])
    return _extract_object(expression, callFrame)

def _get_argument():

    callFrame = inspect.currentframe().f_back.f_back
    callNode = Source.executing(callFrame).node
    source = Source.for_frame(callFrame)
    expression = source.asttokens().get_text(callNode.args[0])

    words = expression.split('.')
    obj = callFrame.f_locals[words.pop(0)]
    while len(words) > 1:
        obj = getattr(obj, words.pop(0))

    return obj, words[0]

bindings = defaultdict(list)

def update():

    for source, targets in bindings.items():
        if source in bindable_properties:
            continue
        source_obj, source_name = source
        for target_obj, target_name, transform in targets:
            value = transform(getattr(source_obj, source_name))
            if getattr(target_obj, target_name) != value:
                setattr(target_obj, target_name, value)

def reset():

    bindings.clear()

def _bind_to(self, _, forward=lambda x: x):

    expression = inspect.stack()[1].code_context[0].strip().split('.bind_to(')[0]
    callFrame = inspect.currentframe().f_back
    self_obj, self_name = _extract_object(expression, callFrame)
    other_obj, other_name = _get_argument()

    setattr(other_obj, other_name, forward(self))
    bindings[(self_obj, self_name)].append((other_obj, other_name, forward))

def _bind_from(_, other, backward=lambda x: x):

    expression = inspect.stack()[1].code_context[0].strip().split('.bind_from(')[0]
    callFrame = inspect.currentframe().f_back
    self_obj, self_name = _extract_object(expression, callFrame)
    other_obj, other_name = _get_argument()

    setattr(self_obj, self_name, backward(other))
    bindings[(other_obj, other_name)].append((self_obj, self_name, backward))

def _bind_2way(self, _, forward=lambda x: x, backward=lambda x: x):

    expression = inspect.stack()[1].code_context[0].strip().split('.bind_2way(')[0]
    callFrame = inspect.currentframe().f_back
    self_obj, self_name = _extract_object(expression, callFrame)
    other_obj, other_name = _get_argument()

    setattr(other_obj, other_name, forward(self))
    bindings[(self_obj, self_name)].append((other_obj, other_name, forward))
    bindings[(other_obj, other_name)].append((self_obj, self_name, backward))

bindable_properties = set()

class BindableProperty:

    def __set_name__(self, _, name):

        self.name = name

    def __get__(self, owner, _=None):

        return getattr(owner, '_' + self.name)

    def __set__(self, owner, value):

        setattr(owner, '_' + self.name, value)

        bindable_properties.add((owner, self.name))

        for obj, name, transform in bindings[(owner, self.name)]:
            if getattr(obj, name) != transform(value):
                setattr(obj, name, transform(value))

for type_ in [type(None), bool, int, float, str, tuple, list, dict, set]:
    curse(type_, 'bind_to', _bind_to)
    curse(type_, 'bind_from', _bind_from)
    curse(type_, 'bind_2way', _bind_2way)
