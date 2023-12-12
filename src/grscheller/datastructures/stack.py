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

"""Module grscheller.datastructure.stack - Stateful & Functional LIFO stacks:

   Module implementing a LIFO stacks using singularly linked linear trees of
   nodes. The nodes can be safely shared between different stack instances and
   are an implementation detail hidden from client code.
"""

from __future__ import annotations

__all__ = ['Stack', 'FStack']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

from typing import Any, Callable
from .core.stack_base import StackBase
from .core.nodes import SL_Node as Node
from .core.circular_array import CircularArray
from .core.fp import FP_rev

class Stack(StackBase):
    """Class implementing a mutable Last In, First Out (LIFO) stack data structure
    pointing to a singularly linked list of nodes. This class is designed to share
    nodes with other Stack instances.

    Stacks are stateful objects, values can be pushed on & popped off.

    A Stack points to either the top node in the list, or to None which indicates
    an empty stack.

    A Stack keeps a count of the number of objects currently on it. Pushing to,
    popping from, getting the length and copying the Stack are all O(1) operations.

    None represents the absence of a value and ignored if pushed on a Stack.
    """
    def __str__(self):
        """Display the data in the Stack, left to right starting at bottom"""
        return '|| ' + ' <- '.join(reversed(CircularArray(*self).map(repr))) + ' ><'

    def copy(self) -> Stack:
        """Return shallow copy of a Stack in O(1) time & space complexity"""
        stack = Stack()
        stack._head, stack._count = self._head, self._count
        return stack

    def reverse(self) -> None:
        """Return shallow copy of a Stack in O(1) time & space complexity"""
        stack = Stack(reversed(self))
        self._head, self._count = stack._head, stack._count

    def push(self, *ds: Any) -> None:
        """Push data that is not NONE onto top of stack,
        return the stack being pushed.
        """
        for d in ds:
            if d is not None:
                node = Node(d, self._head)
                self._head, self._count = node, self._count+1

    def pop(self) -> Any:
        """Pop data off of top of stack"""
        if self._head is None:
            return None
        else:
            data = self._head._data
            self._head, self._count = self._head._next, self._count-1
            return data

    def peak(self, default: Any=None) -> Any:
        """Returns the data at the top of the stack. Does not consume the data.
        If stack is empty, data does not exist so in that case return default.
        """
        if self._head is None:
            return default
        return self._head._data

    def map(self, f: Callable[[Any], Stack]) -> None:
        """Maps a function (or callable object) over the values on the Stack.
        Mutates the Stack object. O(n).
        """
        newStack = Stack(*map(f, reversed(self)))
        self._head, self._count = newStack._head, newStack._count

class FStack(StackBase, FP_rev):
    """Class implementing an immutable Last IN, First Out (LIFO) data structure
    pointing to a singularly linked list of nodes. This class is designed to share
    nodes with other FStack instances.

    FStack stacks are immutable objects.

    An FStack points to either the top node in the list, or to None which indicates
    an empty FStack.

    An Fstack keeps a count of the number of objects currently on it. Getting the head,
    tail, length, copying and creating a new Fstack with cons are all O(1) operations.

    None represents the absence of a value and ignored if pushed on an FStack.
    """
    def __init__(self, *ds):
        super().__init__(*ds)

    def __str__(self):
        """Display the data in the FStack, left to right starting at bottom"""
        return '| ' + ' <- '.join(reversed(CircularArray(*self).map(repr))) + ' ><'

    def copy(self) -> FStack:
        """Return shallow copy of a FStack in O(1) time & space complexity"""
        fstack = FStack()
        fstack._head = self._head
        fstack._count = self._count
        return fstack

    def reverse(self) -> FStack:
        return FStack(reversed(self))

    def head(self, default: Any=None) -> Any:
        """Returns the data at the top of the FStack. Does not consume the data.
        If the FStack is empty, head does not exist so in that case return default.
        """
        if self._head is None:
            return default
        return self._head._data

    def tail(self, default=None) -> FStack:
        """Return tail of the FStack. If FStack is empty, tail does not exist, so
        return a default of type FStack instead. If default is not given, return
        an empty FStack.
        """
        if self._head:
            fstack = FStack()
            fstack._head = self._head._next
            fstack._count = self._count - 1
            return fstack
        elif default is None:
            return FStack()
        else:
            return default

    def cons(self, d: Any) -> FStack:
        """Return a new FStack with data as head and self as tail. Constructing
        an FStack using a non-existent value as head results in a non-existent
        FStack. In that case, just return a copy of the FStack.
        """
        if d is not None:
            fstack = FStack()
            fstack._head = Node(d, self._head)
            fstack._count = self._count + 1
            return fstack
        else:
            return self.copy()

if __name__ == "__main__":
    pass
