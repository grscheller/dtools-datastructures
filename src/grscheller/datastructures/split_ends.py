# Copyright 2023-2024 Geoffrey R. Scheller
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

"""Module split_ends

LIFO stacks which can safely share immutable data between themselves.

* top of each stack is a "split end" of a hair that can share common roots
* each SplitEnd containing a count of elements and a top node
* once created, nodes are immutable and can be shared between hairs
* multiple ends can share the same tail, hence the name "split_ends"
* hairs themselves are mutable objects where nodes can be pushed and popped
* functional interfaces are provided so hairs can be treated as immutable

"""
from __future__ import annotations

__all__ = ['SplitEnd']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023-2024 Geoffrey R. Scheller"
__license__ = "Apache License 2.0"

from typing import Callable, Generic, Iterator, Optional, TypeVar
from itertools import chain
from grscheller.circular_array.circular_array import CircularArray
from grscheller.fp.iterators import exhaust, merge
from .core.nodes import SL_Node as Node

_T = TypeVar('_T')
_S = TypeVar('_S')

class SplitEnd(Generic[_T]):
    """Class implementing a stack type data structures called a "thread". Each
    thread is a very simple stateful object containing a count of the number of
    elements on it and a reference to an immutable node of a linear tree of
    singularly linked nodes. Different stack objects can safely share the same
    data by each pointing to the same node.

    """
    __slots__ = '_head', '_count'

    def __init__(self, *ds: _T):
        """Construct a LIFO Stack"""
        self._head: Optional[Node[_T]] = None
        self._count: int = 0
        for d in ds:
            node: Node[_T] = Node(d, self._head)
            self._head = node
            self._count += 1

    def __iter__(self) -> Iterator[_T]:
        """Iterator yielding data stored on the stack, starting at the head"""
        node = self._head
        while node:
            yield node._data
            node = node._next

    def __reversed__(self) -> Iterator[_T]:
        """Reverse iterate over the contents of the stack"""
        return reversed(CircularArray(*self))

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(' + ', '.join(map(repr, reversed(self))) + ')'

    def __bool__(self) -> bool:
        """Returns true if stack is not empty"""
        return self._count > 0

    def __len__(self) -> int:
        """Returns current number of values on the stack"""
        return self._count

    def __eq__(self, other: object) -> bool:
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

    def __str__(self) -> str:
        """Display the data in the `Stack,` left to right starting at bottom."""
        return '|| ' + ' <- '.join(reversed(CircularArray(*self).map(repr))) + ' ><'

    def copy(self) -> SplitEnd[_T]:
        """Return a copy of a `Stack` in O(1) time & space complexity."""
        stack: SplitEnd[_T] = SplitEnd()
        stack._head, stack._count = self._head, self._count
        return stack

    def reverse(self) -> SplitEnd[_T]:
        """Return shallow reversed copy of a `Stack`.

        * Returns a new `Stack` object with shallow copied new data
        * O(1) space & time complexity

        """
        return SplitEnd(*self)

    def push(self, *ds: Optional[_T]) -> None:
        """Push data that is not `None` onto top of the `Stack`."""
        for d in ds:
            if d is not None:
                node = Node(d, self._head)
                self._head, self._count = node, self._count+1

    def pop(self, default: Optional[_T]=None) -> Optional[_T]:
        """Pop data off of top of stack."""
        if self._head is None:
            return None
        else:
            data = self._head._data
            self._head, self._count = self._head._next, self._count-1
            return data

    def peak(self, default: Optional[_T]) -> Optional[_T]:
        """Returns the data at the top of the `Stack`. Does not consume the data.

        If `Stack` is empty, data does not exist so in that case return default.

        """
        if self._head is None:
            return default
        return self._head._data

    def head(self, default: Optional[_T]=None) -> Optional[_T]:
        """Returns the data at the top of the `SplitEnd`.

        * does not consume the data
        * for an empty `SplitEnd`, head does not exist, so return default.

        """
        if self._head is None:
            return default
        return self._head._data

    def tail(self, default: Optional[SplitEnd[_T]]=None) -> Optional[SplitEnd[_T]]:
        """Return tail of the `FStack`.

        If `FStack` is empty, tail does not exist, so return a default of type
        `FStack` instead. If default is not given, return an empty `FStack`.

        """
        if self._head:
            fstack: SplitEnd[_T] = SplitEnd()
            fstack._head = self._head._next
            fstack._count = self._count - 1
            return fstack
        elif default is None:
            return SplitEnd()
        else:
            return default

    def cons(self, d: _T) -> SplitEnd[_T]:
        """Return a new `FStack` with data as head and self as tail.

        Constructing an `FStack` using a non-existent value as head results in
        a non-existent `FStack`. In that case, return a copy of the `FStack`.

        """
        if d is not None:
            stack: SplitEnd[_T] = SplitEnd()
            stack._head = Node(d, self._head)
            stack._count = self._count + 1
            return stack
        else:
            return self.copy()

    def map(self, f: Callable[[_T], _S]) -> SplitEnd[_S]:
        """Maps a function (or callable object) over the values on the `Stack`.

        * Returns a new `Stack` object with shallow copied new data
        * O(n) complexity

        """
        return SplitEnd(*map(f, reversed(self)))

    def flatMap(self, f: Callable[[_T], SplitEnd[_S]]) -> SplitEnd[_S]:
        """Monadically bind `f` to the `FStack` sequentially"""
        return SplitEnd(*chain(*map(reversed, map(f, reversed(self)))))

    def mergeMap(self, f: Callable[[_T], SplitEnd[_S]]) -> SplitEnd[_S]:
        """Monadically bind f to the `FStack` sequentially until first exhausted"""
        return SplitEnd(*merge(*map(reversed, map(f, reversed(self)))))

    def exhaustMap(self, f: Callable[[_T], SplitEnd[_S]]) -> SplitEnd[_S]:
        """Monadically bind f to the `FStack` merging until all exhausted"""
        return SplitEnd(*exhaust(*map(reversed, map(f, reversed(self)))))
