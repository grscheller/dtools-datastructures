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

"""Module grscheller.datastructure.pstack - Stateful LIFO stack:

   Module implementing a LIFO stack using a singularly linked linear tree of
   nodes. The nodes can be safely shared between different Stack instances and
   are an implementation detail hidden from client code.

   Pushing to, popping from, and getting the length of the PStack are all O(1)
   operations.
"""

from __future__ import annotations

__all__ = ['PStack']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

from typing import Any, Callable
from .core.stack import Stack
from .core.nodes import SL_Node as Node
from .core.carray import CArray

class PStack(Stack):
    """Class implementing a Last In, First Out (LIFO) stack data structure. The
    stack contains a singularly linked list of nodes. Class designed to share
    nodes with other PStack instances.

    PStacks stacks are stateful objects, values can be pushed on & popped off.

    A stack points to either the top node of a singlely linked list, or to
    None which indicates an empty stack.

    A stack keeps a count of the number of objects currently on it.

    None represents the absence of a value and ignored if pushed on a PStack.
    """
    def __init__(self, *ds):
        """Construct a stateful LIFO Stack"""
        super().__init__(*ds)

    def __str__(self):
        """Display the data in the stack, left to right starting at bottom"""
        return '|| ' + ' <- '.join(reversed(CArray(*self).map(repr))) + ' ><'

    def copy(self) -> PStack:
        """Return shallow copy of a PStack in O(1) time & space complexity"""
        pstack = PStack()
        pstack._head = self._head
        pstack._count = self._count
        return pstack

    def reverse(self) -> None:
        """Return shallow copy of a PStack in O(1) time & space complexity"""
        pstack = PStack(reversed(self))
        self._head = pstack._head
        self._count = pstack._count

    def push(self, *ds: Any) -> None:
        """Push data that is not NONE onto top of stack,
        return the stack being pushed.
        """
        for d in ds:
            if d is not None:
                node = Node(d, self._head)
                self._head = node
                self._count += 1

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

    def map(self, f: Callable[[Any], Stack]) -> None:
        """Maps a function (or callable object) over the values on the Stack.
        Mutates the Stack object. O(n).
        """
        newStack = Stack(*map(f, reversed(self)))
        self._head = newStack._head
        self._count = newStack._count

if __name__ == "__main__":
    pass
