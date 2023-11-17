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

__all__ = ['Stack']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

from typing import Any
from .nodes import SL_Node as Node
from .carray import CArray

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
                node = Node(d, self._head)
                self._head = node
                self._count += 1

    def __iter__(self):
        """Iterator yielding data stored on the stack, starting at the head"""
        node = self._head
        while node:
            yield node._data
            node = node._next

    def __reversed__(self):
        """Reverse iterate over the contents of the stack"""
        return reversed(CArray(*self))

    def __repr__(self):
        return f'{self.__class__.__name__}(' + ', '.join(map(repr, reversed(self))) + ')'

    def __bool__(self):
        """Returns true if stack is not empty"""
        return self._count > 0

    def __len__(self):
        """Returns current number of values on the stack"""
        return self._count

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

if __name__ == "__main__":
    pass
