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

from typing import Any, Callable, Union

__all__ = ['Stack']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

from .iterlib import concatIters, mergeIters, mapIter
from .carray import CArray

class _Node():
    """Class implementing nodes that can be linked together to form a singularly
    linked list. A node always contain data. It either has a reference to the
    next _Node object or None to indicate the bottom of the linked list.
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

class Stack():
    """Class implementing a Last In, First Out (LIFO) stack datastructure. The
    stack contains a singularly linked list of nodes. Class designed to share
    nodes with other Stack instances.

    - The stack points to either the top node in the list, or to None which
      indicates an empty stack.
    - Stacks are stateful objects where values can be pushed on & popped off.
    - None represents the absence of a value and are ignored if pushed on the
      stack. Use a grscheller.functional.Maybe to indicate an assent value or
      another sentital value such as the empty tuple ().
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
        return iter(Stack(*self))

    def __eq__(self, other: Any):
        """Returns True if all the data stored on the two stacks are the same.
        Worst case is O(n) behavior which happens when all the corresponding
        data elements on the two stacks are equal, in whatever sense they
        define equality, and none of the nodes are shared.
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
            if left.peak() != right.peak():
                return False
            left = left.tail()
            right = right.tail()
            nn -= 1
        return True

    def __repr__(self):
        """Display the data in the stack, left to right starting at bottom"""
        carrayData = CArray(*self)
        carrayData.map_update(lambda x: repr(x)) 
        repStr = '|| ' + carrayData.popR()
        while carrayData:
            repStr = repStr + ' <- ' + carrayData.popR()
        repStr += ' ><'
        return repStr

    def copy(self) -> Stack:
        """Return shallow copy of the stack in O(1) time & space complexity"""
        stack = Stack()
        stack._head = self._head
        stack._count = self._count
        return stack

    def push(self, *ds: Any) -> None:
        """Push data that is not NONE onto top of stack,
        return the stack being pushed.
        """
        for d in ds:
            if d is not None:
                node = _Node(d, self._head)
                self._head = node
                self._count += 1

    def pop(self) -> Union[Any, None]:
        """Pop data off of top of stack"""
        if self._head is None:
            return None
        else:
            data = self._head._data
            self._head = self._head._next
            self._count -= 1
            return data

    def peak(self) -> Union[Any, None]:
        """Returns the data at the head of stack. Does not consume the data.

        Note: If stack is empty, return None.
        """
        if self._head is None:
            return None
        return self._head._data

    def peakOrElse(self, default: Any) -> Any:
        """Returns the data at the head of stack. Does not consume the data.

        Note: If stack is empty, return default value.
        """
        value = self.peak()
        if value is None:
            value = default
        return value

    def tail(self) -> Union[Stack, None]:
        """Return tail of the stack.

        Note: The tail of an empty stack does not exist,
              hence return None.
        """
        if self._head:
            stack = Stack()
            stack._head = self._head._next
            stack._count = self._count - 1
            return stack
        return None

    def tailOrElse(self, default: Union[Stack, None] = None) -> Stack:
        """Return tail of the stack.

        Note: If stack is empty, return default value of type Stack.
              If default value not give, return a new empty stack.
        """
        stack = self.tail()
        if stack is None:
            if default is None:
                stack = Stack()
            else:
                stack = default
        return stack

    def cons(self, data: Any) -> Stack:
        """Return a new stack with data as head and self as tail.

        Note: Trying to push None on the stack results in a shallow
              copy of the original stack.
        """
        if data is not None:
            stack = Stack()
            stack._head = _Node(data, self._head)
            stack._count = self._count + 1
            return stack
        else:
            return self.copy()

    def map(self, f: Callable[[Any], Stack]) -> Stack:
        """Maps a function (or callable object) over the values of the stack.

        Returns a new stack with new nodes so not to affect nodes shared
        by other Stack objects.
        """
        return Stack(*mapIter(reversed(self), f))

    def flatMap(self, f: Callable[[Any], Stack]) -> Stack:
        """Apply function and flatten result, returns new instance"""
        return Stack(
            *concatIters(
                *mapIter(mapIter(reversed(self), f), lambda x: reversed(x))
            )
        )

    def mergeMap(self, f: Callable[[Any], Stack]) -> Stack:
        """Apply function and flatten result, returns new instance"""
        return Stack(
            *mergeIters(
                *mapIter(mapIter(reversed(self), f), lambda x: reversed(x))
            )
        )

if __name__ == "__main__":
    pass
