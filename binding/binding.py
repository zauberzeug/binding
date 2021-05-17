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

def _get_parent_and_argument(method_name, nesting):

    sep = f'.{method_name}('
    expression = inspect.stack()[2].code_context[0].strip().split(sep)[0]
    callFrame = inspect.currentframe().f_back.f_back
    self_obj, self_name = _extract_object(expression, callFrame)

    for _ in range(nesting):
        callFrame = callFrame.f_back
    callNode = Source.executing(callFrame).node
    source = Source.for_frame(callFrame)
    expression = source.asttokens().get_text(callNode.args[0])
    other_obj, other_name = _extract_object(expression, callFrame)

    return self_obj, self_name, other_obj, other_name

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

def propagate(source_obj, source_name, visited=None):

    if visited is None:
        visited = set()
    visited.add((source_obj, source_name))
    for target_obj, target_name, transform in bindings[(source_obj, source_name)]:
        if (target_obj, target_name) in visited:
            continue
        target_value = transform(getattr(source_obj, source_name))
        if getattr(target_obj, target_name) != target_value:
            setattr(target_obj, target_name, target_value)
            propagate(target_obj, target_name, visited)

def reset():

    bindings.clear()

def _bind_to(*_, forward=lambda x: x, nesting=0):

    self_obj, self_name, other_obj, other_name = _get_parent_and_argument('bind_to', nesting)
    bindings[(self_obj, self_name)].append((other_obj, other_name, forward))
    propagate(self_obj, self_name)

def _bind_from(*_, backward=lambda x: x, nesting=0):

    self_obj, self_name, other_obj, other_name = _get_parent_and_argument('bind_from', nesting)
    bindings[(other_obj, other_name)].append((self_obj, self_name, backward))
    propagate(other_obj, other_name)

def _bind(*_, forward=lambda x: x, backward=lambda x: x, nesting=0):

    self_obj, self_name, other_obj, other_name = _get_parent_and_argument('bind', nesting)
    bindings[(self_obj, self_name)].append((other_obj, other_name, forward))
    bindings[(other_obj, other_name)].append((self_obj, self_name, backward))
    propagate(other_obj, other_name)

bindable_properties = set()

class BindableProperty:

    def __set_name__(self, _, name):

        self.name = name

    def __get__(self, owner, _=None):

        return getattr(owner, '_' + self.name)

    def __set__(self, owner, value):

        setattr(owner, '_' + self.name, value)

        bindable_properties.add((owner, self.name))

        propagate(owner, self.name)

for type_ in [type(None), bool, int, float, str, tuple, list, dict, set]:
    curse(type_, 'bind_to', _bind_to)
    curse(type_, 'bind_from', _bind_from)
    curse(type_, 'bind', _bind)
