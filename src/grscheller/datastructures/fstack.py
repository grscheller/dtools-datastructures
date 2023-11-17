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

"""Module grscheller.datastructure.fstack - Functional LIFO stack:

   Module implementing a LIFO stack using a singularly linked linear tree of
   nodes. The nodes can be safely shared between different FStack instances and
   are an implementation detail hidden from client code.

   Getting the head, tail, creating a new stack with cons, and getting the
   length of the FStack are all O(1) operations.
"""

from __future__ import annotations

__all__ = ['FStack']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

from typing import Any
from .core.stack import Stack
from .core.fp import FP_rev
from .core.nodes import SL_Node as Node
from .core.carray import CArray

class FStack(Stack, FP_rev):
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
        super().__init__(*ds)

    def __str__(self):
        """Display the data in the stack, left to right starting at bottom"""
        return '| ' + ' <- '.join(reversed(CArray(*self).map(repr))) + ' ><'

    def copy(self) -> FStack:
        """Return shallow copy of a FStack in O(1) time & space complexity"""
        fstack = FStack()
        fstack._head = self._head
        fstack._count = self._count
        return fstack

    def reverse(self) -> FStack:
        return FStack(reversed(self))

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
            stack._head = Node(data, self._head)
            stack._count = self._count + 1
            return stack
        else:
            return self.copy()

if __name__ == "__main__":
    pass
