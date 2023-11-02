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
"""

from __future__ import annotations

__all__ = ['FStack', 'PStack']
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
    def __init__(self, data, nodeNext: _Node | None):
        """Construct an element of a linked list, semantically immutable.

        Note: It is the Stack class's responsibility that the _data property is
        never set to None.
        """
        self._data = data
        self._next = nodeNext

    def __bool__(self):
        """Always return true, None will return as false"""
        return True

class _Stack():
    """Base class for the PStack & FStack classes"""
    def __init__(self, *ds):
        """Construct a LIFO Stack"""
        self._head = None
        self._count = 0
        for d in ds:
            if d is not None:
                node = _Node(d, self._head)
                self._head = node
                self._count += 1

    def __bool__(self) -> bool:
        """Returns true if stack is not empty"""
        return self._count > 0

    def __len__(self) -> int:
        """Returns current number of values on the stack"""
        return self._count

    def __iter__(self):
        """Iterator yielding data stored in the stack, starting at the head"""
        node = self._head
        while node:
            yield node._data
            node = node._next

    def __reversed__(self):
        """Reverse iterate over the current state of the stack"""
        return reversed(CArray(*self))

    def _tail(self, stack):
        """Return tail of the stack."""
        if self._head:
            stack._head = self._head._next
            stack._count = self._count - 1
            return stack
        return None

    def __eq__(self, other: Any):
        """Returns True if all the data stored on the two stacks are the same
        and the two stacks are of the same subclass. Worst case is O(n) behavior
        which happens when all the corresponding data elements on the two stacks
        are equal, in whatever sense they define equality, and none of the nodes
        are shared.
        """
        if not isinstance(other, type(self)):
            return False

        if self._count != other._count:
            return False

        left = self
        right = other
        nn = self._count
        while nn > 0:
            if left is None or right is None:
                return True
            if left._head is right._head:
                return True
            if left._getHead() != right._getHead():
                return False
            left = left._tail(self._getStack())
            right = right._tail(self._getStack())
            nn -= 1
        return True

    def copy(self) -> _Stack:
        """Return shallow copy of the stack in O(1) time & space complexity"""
        stack = self._getStack()
        stack._head = self._head
        stack._count = self._count
        return stack

    def _getHead(self) -> Any|None:
        raise NotImplemented

    def _getStack(self) -> _Stack:
        raise NotImplemented

class PStack(_Stack):
    """Class implementing a Last In, First Out (LIFO) stack data structure. The
    stack contains a singularly linked list of nodes. Class designed to share
    nodes with other Stack instances.

    - Stacks are stateful objects where values can be pushed on & popped off.
    - A stack points to either the top node of a singlely linked list, or to
      None which indicates an empty stack.
    - A stack keeps a count of the number of objects currently on it.
    - None represents the absence of a value and are ignored if pushed on the
      stack. Use a grscheller.functional.Maybe to indicate an assent value or
      another sentital value such as the empty tuple ().
    """
    def __init__(self, *ds):
        """Construct a stateful LIFO Stack"""
        _Stack.__init__(self, *ds)

    def __repr__(self):
        """Display the data in the stack, left to right starting at bottom"""
        return '|| ' + ' <- '.join(reversed(CArray(*self).map(lambda x: repr(x)))) + ' ><'

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

    def pop(self) -> Any|None:
        """Pop data off of top of stack"""
        if self._head is None:
            return None
        else:
            data = self._head._data
            self._head = self._head._next
            self._count -= 1
            return data

    def peak(self) -> Any|None:
        """Returns the data at the top of stack. Does not consume the data.

        Note: If stack is empty, return None.
        """
        if self._head is None:
            return None
        return self._head._data

    def peakOr(self, default: Any) -> Any:
        """Returns the data at the head of stack. Does not consume the data.

        Note: If stack is empty, return default value.
        """
        value = self.peak()
        if value is None:
            value = default
        return value

    def map(self, f: Callable[[Any], PStack]) -> PStack:
        """Maps a function (or callable object) over the values on the stack.

        Returns a new stack with new nodes.  None values surpressed.
        """
        return PStack(*map(f, reversed(self)))

    def flatMap(self, f: Callable[[Any], PStack]) -> PStack:
        """Apply function and flatten result, returns new instance

        Merge the stacks produced sequentially front-to-back.
        """
        return PStack(*chain(
            *map(reversed, map(f, reversed(self)))
        ))

    def mergeMap(self, f: Callable[[Any], PStack]) -> PStack:
        """Apply function and flatten result, returns new instance

        Round Robin Merge the stacks produced until first cached stack is
        exhausted.
        """
        return PStack(*merge(
            *map(reversed, map(f, reversed(self)))
        ))

    def exhaustMap(self, f: Callable[[Any], PStack]) -> PStack:
        """Apply function and flatten result, returns new instance

        Round Robin Merge the stacks produced until all the cached stacks are
        exhausted.
        """
        return PStack(*exhaust(
            *map(reversed, map(f, reversed(self)))
        ))

    def _getHead(self) -> Any|None:
        return self.peak()

    def _getStack(self) -> PStack:
        return PStack()

class FStack(_Stack):
    """Class implementing an immutable singularly linked stack data
    structure consisting of a singularly linked list of nodes. This class
    designed to share nodes with other Stack instances.

    - Functional stacks are immutable objects.
    - A functional stack points to either the top node in the list, or to None
      which indicates an empty stack.
    - A functional stack has the count of the number of objects on it.
    - None represents the absence of a value and are ignored if pushed on the
      stack. Use a grscheller.functional.Maybe to indicate an assent value or
      another sentital value such as the empty tuple ().
    """
    def __init__(self, *ds):
        """Construct an immutable LIFO Stack"""
        _Stack.__init__(self, *ds)

    def __repr__(self):
        """Display the data in the stack, left to right starting at bottom"""
        return '| ' + ' <- '.join(reversed(CArray(*self).map(lambda x: repr(x)))) + ' ><'

    def head(self) -> Any|None:
        """Returns the data at the head of stack. Does not consume the data.

        Note: If stack is empty, return None.
        """
        if self._head is None:
            return None
        return self._head._data

    def headOr(self, default: Any) -> Any:
        """Returns the data at the head of stack. Does not consume the data.

        Note: If stack is empty, return default value.
        """
        value = self.head()
        if value is None:
            value = default
        return value

    def tail(self) -> FStack|None:
        """Return tail of the stack.

        Note: The tail of an empty stack does not exist,
              hence return None.
        """
        return self._tail(FStack())

    def tailOr(self, default: FStack|None = None) -> FStack:
        """Return tail of the stack.

        Note: If stack is empty, return default value of type Stack.
              If default value not give, return a new empty stack.
        """
        stack = self._tail(FStack())
        if stack is None:
            if default is None:
                stack = FStack()
            else:
                stack = default
        return stack

    def cons(self, data: Any) -> FStack|None:
        """Return a new stack with data as head and self as tail.

        Note: Constructing a stack using a non-existent value as head results
        in a non-existent stack.
        """
        if data is not None:
            stack = FStack()
            stack._head = _Node(data, self._head)
            stack._count = self._count + 1
            return stack
        else:
            return None

    def map(self, f: Callable[[Any], FStack]) -> FStack:
        """Maps a function (or callable object) over the values on the stack.

        Returns a new stack with new nodes. None values surpressed.
        """
        return FStack(*map(f, reversed(self)))

    def flatMap(self, f: Callable[[Any], FStack]) -> FStack:
        """Apply function and flatten result, returns new instance

        Merge the stacks produced sequentially front-to-back.
        """
        return FStack(*chain(
            *map(reversed, map(f, reversed(self)))
        ))

    def mergeMap(self, f: Callable[[Any], FStack]) -> FStack:
        """Apply function and flatten result, returns new instance

        Round Robin Merge the stacks produced until first cached stack is
        exhausted.
        """
        return FStack(*merge(
            *map(reversed, map(f, reversed(self)))
        ))

    def exhaustMap(self, f: Callable[[Any], FStack]) -> FStack:
        """Apply function and flatten result, returns new instance

        Round Robin Merge the stacks produced until all the cached stacks are
        exhausted.
        """
        return FStack(*exhaust(
            *map(reversed, map(f, reversed(self)))
        ))

    def _getHead(self) -> Any|None:
        return self.head()

    def _getStack(self) -> FStack:
        return FStack()

if __name__ == "__main__":
    pass
