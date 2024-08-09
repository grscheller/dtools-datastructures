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

"""Module of LIFO stacks that can safely share immutable data between themselves."""

from __future__ import annotations

__all__ = ['SplitEnd']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023-2024 Geoffrey R. Scheller"
__license__ = "Apache License 2.0"

from typing import Callable, cast, Generic, Iterator, Optional, overload, TypeVar
from grscheller.fp.iterables import concat, exhaust, merge
from grscheller.untyped.nothing import Nothing, nothing
from .core.nodes import SL_Node as Node
from .core.enums import FM

_D = TypeVar('_D')
_S = TypeVar('_S')
_T = TypeVar('_T')

class SplitEnd(Generic[_D, _S]):
    """Class implementing a stack type data structures called a "split end".

    * each "split end" is a very simple LIFO stateful data structure
    * contains a count of nodes & reference to first node of a linked list
    * different "split ends" can safely share the same "tail"
    * each "split end" sees itself as a singularly linked list
    * bush-like datastructures can be formed using multiple "split ends"

    """
    __slots__ = '_head', '_count', '_s'

    @overload
    def __init__(self, *ds: _D, s: _S) -> None:
        ...
    @overload
    def __init__(self, *ds: _D, s: Nothing) -> None:
        ...
    @overload
    def __init__(self, *ds: _D) -> None:
        ...
    def __init__(self, *ds: _D, s: _S|Nothing=nothing, storable:bool=True) -> None:
        """Construct a LIFO Stack"""
        self._head: Optional[Node[_D]] = None
        self._count: int = 0
        self._s = s
        for d in ds:
            node: Node[_D] = Node(d, self._head)
            self._head = node
            self._count += 1

    def __iter__(self) -> Iterator[_D]:
        """Iterator yielding data stored on the stack, starting at the head"""
        node = self._head
        while node:
            yield node._data
            node = node._next

    def reverse(self) -> SplitEnd[_D, _S]:
        """Return shallow reversed copy of a SplitEnd.

        * Returns a new Stack object with shallow copied new data
        * creates all new nodes
        * O(1) space & time complexity

        """
        return SplitEnd(*self, s=self._s)

    def __reversed__(self) -> Iterator[_D]:
        """Reverse iterate over the contents of the stack"""
        return iter(self.reverse())

    def __repr__(self) -> str:
        if self._s == nothing:
            return 'SplitEnd(' + ', '.join(map(repr, reversed(self))) + ')'
        else:
            return ('SplitEnd('
                    + ', '.join(map(repr, reversed(self)))
                    + ', s=' + repr(self._s) + ')')

    def __str__(self) -> str:
        """Display the data in the Stack, left to right."""
        if self._s == nothing:
            return ('>< '
                    + ' -> '.join(map(str, self))
                    + ' ||')
        else:
            return ('>< '
                    + ' -> '.join(map(str, self))
                    + ' |' + repr(self._s) + '|')

    def __bool__(self) -> bool:
        """Returns true if stack is not empty"""
        return self._count > 0

    def __len__(self) -> int:
        return self._count

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return False

        if self._count != other._count:
            return False
        if self._s != other._s:
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

    def copy(self) -> SplitEnd[_D, _S]:
        """Return a copy of a Stack in O(1) space & time complexity."""
        stack: SplitEnd[_D, _S] = SplitEnd(s=self._s)
        stack._head, stack._count = self._head, self._count
        return stack

    def push(self, *ds: _D) -> None:
        """Push data onto top of the SplitEnd.

        * ignore "non-existent" Nothing() values pushed on SplitEnd

        """
        for d in ds:
            if d is not nothing:
                node = Node(d, self._head)
                self._head, self._count = node, self._count+1

    @overload
    def pop(self, default: _D) -> _D|_S:
        ...
    @overload
    def pop(self) -> _D|_S:
        ...
    def pop(self, default: _D|Nothing=nothing) -> _D|_S|Nothing:
        """Pop data off of top of the SplitEnd.

        * if empty, return a default value
        * if empty and a default value not given, return the sentinel value

        """
        if self._head is None:
            if default is nothing:
                return self._s
            else:
                return default
        else:
            data = self._head._data
            self._head, self._count = self._head._next, self._count-1
            return data

    @overload
    def peak(self, default: _D) -> _D:
        ...
    @overload
    def peak(self) -> _D|_S:
        ...
    def peak(self, default: _D|Nothing=nothing) -> _D|_S|Nothing:
        """Returns the data at the top of the SplitEnd.

        * does not consume the data
        * if empty, data does not exist, so in that case return default
        * if empty and no default given, return nothing: Nothing

        """
        if self._head is None:
            return default
        return self._head._data

    @overload
    def head(self, default: _D) -> _D|_S:
        ...
    @overload
    def head(self) -> _D|_S:
        ...
    def head(self, default: _D|Nothing=nothing) -> _D|_S|Nothing:
        """Returns the data at the top of the SplitEnd.

        * does not consume the data
        * for an empty SplitEnd, head does not exist, so return default
        * otherwise return the sentinel value

        """
        if self._head is None:
            if default is nothing:
                return self._s
            else:
                return default
        return self._head._data

    @overload
    def tail(self, default: SplitEnd[_D, _S]) -> SplitEnd[_D, _S]:
        ...
    @overload
    def tail(self) -> SplitEnd[_D, _S]:
        ...
    def tail(self, default: SplitEnd[_D, _S]|Nothing=nothing) -> SplitEnd[_D, _S]|Nothing:
        """Return tail of the SplitEnd.

        * if SplitEnd is empty, tail does not exist, so return sentinel: _S

        """
        if self._head:
            se: SplitEnd[_D, _S] = SplitEnd(s=self._s)
            se._head = self._head._next
            se._count = self._count - 1
            return se
        else:
            return default

    @overload
    def cons(self, d: _D) -> SplitEnd[_D, _S]: 
        ...
    @overload
    def cons(self, d: Nothing) -> SplitEnd[_D, nothing]: 
        ...
    def cons(self, d: _D|Nothing) -> SplitEnd[_D, _S]|Nothing:
        """Return a new SplitEnd with data as head and self as tail.

        Constructing a SplitEnd using a non-existent value as head results in
        a non-existent SplitEnd. In that case, return sentinel: _S.

        """
        if d is nothing:
            return nothing
        else:
            stack: SplitEnd[_D, _S] = SplitEnd(s=self._s)
            stack._head = Node(cast(_D, d), self._head)
            stack._count = self._count + 1
            return stack

    def fold(self, f:Callable[[_D, _D], _D]) -> Optional[_D]:
        """Reduce with f.

        * returns a value of the of type _T if self is not empty
        * returns None if self is empty
        * folds in natural LIFO Order
        * TODO: consolidate fold & fold1

        """
        node: Optional[Node[_D]] = self._head
        if not node:
            return None
        acc: _D = node._data
        while node:
            if (node := node._next) is None:
                break
            acc = f(acc, node._data)
        return acc

    def fold1(self, f:Callable[[_T, _D], _T], s: _T) -> _T:
        """Reduce with f.

        * returns a value of type _T
        * type _T can be same type as _D
        * folds in natural LIFO Order
        * TODO: consolidate fold & fold1

        """
        node: Optional[Node[_D]] = self._head
        if not node:
            return s
        acc: _T = s
        while node:
            acc = f(acc, node._data)
            node = node._next
        return acc

    def flatMap(self, f: Callable[[_D], SplitEnd[_T, _S]], type: FM=FM.CONCAT) -> SplitEnd[_T, _S]:
        """Bind function f to the FTuple:

        * sequentially one after the other
        * merging together until first one exhausted
        * merging together until all are exhausted

        """
        match type:
            case FM.CONCAT:
                return SplitEnd(*concat(*map(lambda x: iter(x), map(f, self))), s=self._s)
            case FM.MERGE:
                return SplitEnd(*merge(*map(lambda x: iter(x), map(f, self))), s=self._s)
            case FM.EXHAUST:
                return SplitEnd(*exhaust(*map(lambda x: iter(x), map(f, self))), s=self._s)

    def map(self, f: Callable[[_D], _T]) -> SplitEnd[_T, _S]:
        """Maps a function (or callable object) over the values on the Stack.

        * TODO: Redo in "natural" order?
        * Returns a new Stack object with shallow copied new data
        * O(n) complexity

        """
        return self.flatMap(lambda a: SplitEnd(f(a)))
