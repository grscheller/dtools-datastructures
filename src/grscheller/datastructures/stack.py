# Copyright 2023 Geoffrey R. Scheller
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Module grscheller.datastructure.stack - LIFO stack:

   Module implementing a LIFO stack using a singularly linked linear tree of
   nodes. The nodes can be safely shared between different Stack instances and
   are an implementation detail hidden from client code.

   Pushing to, popping from, and getting the length of the stack are all O(1)
   operations.

Classes:
  grscheller.datastructure.PStack - LIFO stack, mutable, procedural interface
  grscheller.datastructure.FStack - LIFO stack, immutable, functional interface
"""

from __future__ import annotations

__all__ = ['PStack', 'FStack']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

from typing import Any, Callable, Self
from itertools import chain
from .core.iterlib import merge, exhaust
from .core.carray import CArray

class _Node():

    """Class implementing nodes that can be linked together to form a singularly
    linked list. A node always contain data. It either has a reference to the
    next _Node object or None to indicate the bottom of the linked list.

    Nodes can safely be shared between different Stack instances.
    """
    def __init__(self, data: Any, nodeNext: _Node|None):
        """Construct an element of a linked list, semantically immutable.

        Note: It is the Stack class's responsibility that the _data property is
        never set to None.
        """
        self._data = data
        self._next = nodeNext

    def __bool__(self):
        """Always return true, None will return as false"""
        return True

class Stack():
    """Abstract base class for the purposes of DRY inheritance of classes
    implementing stack type data structures. Each stack is a very simple
    stateful object containing a count of the number of elements on it and
    a reference to an immutable node of a linear tree of singularly linked
    nodes. Different stack objects can safely share the same data by each
    pointing to the same node. Each stack class ensures None values do not
    get pushed onto the the stack.
    """
    def __init__(self, *ds):
        """Construct a LIFO Stack"""
        self._head = None
        self._count = 0
        for d in ds:
            if d is not None:
                node = _Node(d, self._head)
                self._head = node
                self._count += 1

    def copy(self) -> Stack:
        raise NotImplementedError

    def __bool__(self) -> bool:
        """Returns true if stack is not empty"""
        return self._count > 0

    def __len__(self) -> int:
        """Returns current number of values on the stack"""
        return self._count

    def __iter__(self):
        """Iterator yielding data stored on the stack, starting at the head"""
        node = self._head
        while node:
            yield node._data
            node = node._next

    def __reversed__(self):
        """Reverse iterate over the contents of the stack"""
        return reversed(CArray(*self))

    def __eq__(self, other: Any):
        """Returns True if all the data stored on the two stacks are the same
        and the two stacks are of the same subclass. Worst case is O(n) behavior
        which happens when all the corresponding data elements on the two stacks
        are equal, in whatever sense they equality is defined, and none of the
        nodes are shared.
        """
        if not isinstance(other, type(self)):
            return False

        if self._count != other._count:
            return False

        left = self._head
        right = other._head
        nn = self._count
        while nn > 0:
            if left is right:
                return True
            if left is None or right is None:
                return True
            if left._data != right._data:
                return False
            left = left._next
            right = right._next
            nn -= 1
        return True


class PStack(Stack):
    """Class implementing a Last In, First Out (LIFO) stack data structure. The
    stack contains a singularly linked list of nodes. Class designed to share
    nodes with other PStack instances.

    PStacks stacks are stateful objects, values can be pushed on & popped off.

    A stack points to either the top node of a singlely linked list, or to
    None which indicates an empty stack.

    A stack keeps a count of the number of objects currently on it.

    None represents the absence of a value and ignored if pushed on a stack.
    """
    def __init__(self, *ds):
        """Construct a stateful LIFO Stack"""
        super().__init__(*ds)

    def __repr__(self):
        """Display the data in the stack, left to right starting at bottom"""
        return '|| ' + ' <- '.join(reversed(CArray(*self).map(repr))) + ' ><'

    def copy(self) -> PStack:
        """Return shallow copy of a PStack in O(1) time & space complexity"""
        pstack = PStack()
        pstack._head = self._head
        pstack._count = self._count
        return pstack

    def push(self, *ds: Any) -> Self:
        """Push data that is not NONE onto top of stack,
        return the stack being pushed.
        """
        for d in ds:
            if d is not None:
                node = _Node(d, self._head)
                self._head = node
                self._count += 1
        return self

    def pop(self) -> Any:
        """Pop data off of top of stack"""
        if self._head is None:
            return None
        else:
            data = self._head._data
            self._head = self._head._next
            self._count -= 1
            return data

    def peak(self, default: Any=None) -> Any:
        """Returns the data at the top of the stack. Does not consume the data.
        If stack is empty, data does not exist so in that case return default.
        """
        if self._head is None:
            return default
        return self._head._data

    def map(self, f: Callable[[Any], PStack]) -> None:
        """Maps a function (or callable object) over the values on the stack.

        Returns a new stack with new nodes.  None values surpressed.
        """
        newPStack = PStack(*map(f, reversed(self)))
        self._head = newPStack._head
        self._count = newPStack._count

    def flatMap(self, f: Callable[[Any], PStack]) -> None:
        """Apply function and flatten result, returns new instance.

        Merge the stacks produced sequentially front-to-back.
        """
        newPStack = PStack(*chain(*map(reversed, map(f, reversed(self)))))
        self._head = newPStack._head
        self._count = newPStack._count

    def mergeMap(self, f: Callable[[Any], PStack]) -> None:
        """Apply function and flatten result, returns new instance.

        Round Robin Merge the stacks produced until first cached stack is
        exhausted.
        """
        newPStack = PStack(*merge(*map(reversed, map(f, reversed(self)))))
        self._head = newPStack._head
        self._count = newPStack._count

    def exhaustMap(self, f: Callable[[Any], PStack]) -> None:
        """Apply function and flatten result, returns new instance

        Round Robin Merge the stacks produced until all the cached stacks are
        exhausted.
        """
        newPStack = PStack(*exhaust(*map(reversed, map(f, reversed(self)))))
        self._head = newPStack._head
        self._count = newPStack._count


class FStack(Stack):
    """Class implementing an immutable singularly linked stack data
    structure consisting of a singularly linked list of nodes. This
    class is designed to share nodes with other FStack instances.

    FStack stacks are immutable objects.

    A functional stack points to either the top node in the list, or to None
    which indicates an empty stack.

    A functional stack has the count of the number of objects on it.

    None represents the absence of a value and ignored if pushed on an FStack.
    """
    def __init__(self, *ds):
        """Construct an immutable LIFO Stack"""
        super().__init__(*ds)

    def __repr__(self):
        """Display the data in the stack, left to right starting at bottom"""
        return '| ' + ' <- '.join(reversed(CArray(*self).map(repr))) + ' ><'

    def copy(self) -> FStack:
        """Return shallow copy of a FStack in O(1) time & space complexity"""
        fstack = FStack()
        fstack._head = self._head
        fstack._count = self._count
        return fstack

    def head(self, default: Any=None) -> Any:
        """Returns the data at the top of the stack. Does not consume the data.
        If stack is empty, head does not exist so in that case return default.
        """
        if self._head is None:
            return default
        return self._head._data

    def tail(self, default=None) -> FStack:
        """Return tail of the stack. If Stack is empty, tail does not exist, so
        return a default of type FStack instead. If default is not given, return
        an empty FStack.
        """
        if self._head:
            stack = FStack()
            stack._head = self._head._next
            stack._count = self._count - 1
            return stack
        elif default is None:
            return FStack()
        else:
            return default

    def cons(self, data: Any) -> FStack:
        """Return a new stack with data as head and self as tail. Constructing
        a stack using a non-existent value as head results in a non-existent
        stack. In that case, just return a copy of the stack.
        """
        if data is not None:
            stack = FStack()
            stack._head = _Node(data, self._head)
            stack._count = self._count + 1
            return stack
        else:
            return self.copy()

    def map(self, f: Callable[[Any], FStack]) -> FStack:
        """Maps a function (or callable object) over the values on the stack.

        Returns a new stack with new nodes. None values surpressed.
        """
        return FStack(*map(f, reversed(self)))

    def flatMap(self, f: Callable[[Any], FStack]) -> FStack:
        """Apply function and flatten result, returns new instance

        Merge the stacks produced sequentially front-to-back.
        """
        return FStack(*chain(*map(reversed, map(f, reversed(self)))))

    def mergeMap(self, f: Callable[[Any], FStack]) -> FStack:
        """Apply function and flatten result, returns new instance

        Round Robin Merge the stacks produced until first cached stack is
        exhausted.
        """
        return FStack(*merge(*map(reversed, map(f, reversed(self)))))

    def exhaustMap(self, f: Callable[[Any], FStack]) -> FStack:
        """Apply function and flatten result, returns new instance

        Round Robin Merge the stacks produced until all the cached stacks are
        exhausted.
        """
        return FStack(*exhaust(*map(reversed, map(f, reversed(self)))))


if __name__ == "__main__":
    pass
