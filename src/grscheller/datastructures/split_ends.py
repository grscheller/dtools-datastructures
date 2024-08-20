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

"""
### Stack type Data Structures

##### SplitEnd

LIFO stacks which can safely share immutable data between themselves.

---

"""

from __future__ import annotations

from typing import Callable, cast, Generic, Iterator, Optional, overload, TypeVar
from grscheller.fp.iterables import FM, concat, exhaust, merge
from grscheller.fp.nada import Nada, nada
from .nodes import SL_Node as Node

__all__ = ['SplitEnd']

D = TypeVar('D')
S = TypeVar('S')
T = TypeVar('T')

class SplitEnd(Generic[D, S]):
    """
    #### SplitEnd
    
    Class implementing a stack type data structures called a *split end*.

    * each *split end* is a very simple stateful LIFO stack
    * contains a count of nodes & reference to first node of a linked list
    * different *split ends* can safely share the same *tail*
    * each *split end* sees itself as a singularly linked list
    * bush-like datastructures can be formed using multiple *split ends*
    * len() returns the number of elements on the stack
    * in a boolean context, return `True` if SplitEnd is not empty

    """
    __slots__ = '_head', '_count', '_sentinel'

    @overload
    def __init__(self, *ds: D, s: S) -> None:
        ...
    @overload
    def __init__(self, *ds: D, s: Nada) -> None:
        ...
    @overload
    def __init__(self, *ds: D) -> None:
        ...
    def __init__(self, *ds: D, s: S|Nada=nada) -> None:
        self._head: Optional[Node[D]] = None
        self._count: int = 0
        self._sentinel = s
        for d in ds:
            node: Node[D] = Node(d, self._head)
            self._head = node
            self._count += 1

    def __iter__(self) -> Iterator[D]:
        node = self._head
        while node:
            yield node._data
            node = node._next

    def reverse(self) -> SplitEnd[D, S]:
        """
        ##### Return a Reversed SplitEnd

        Return shallow reversed copy of a SplitEnd.

        * Returns a new Stack object with shallow copied new data
        * creates all new nodes
        * O(1) space & time complexity

        """
        return SplitEnd(*self, s=self._sentinel)

    def __reversed__(self) -> Iterator[D]:
        return iter(self.reverse())

    def __repr__(self) -> str:
        if self._sentinel is nada:
            return 'SplitEnd(' + ', '.join(map(repr, reversed(self))) + ')'
        elif self:
            return ('SplitEnd('
                    + ', '.join(map(repr, reversed(self)))
                    + ', s=' + repr(self._sentinel) + ')')
        else:
            return ('SplitEnd('
                    + 's=' + repr(self._sentinel) + ')')


    def __str__(self) -> str:
        """Display the data in the Stack, left to right."""
        if self._sentinel is nada:
            return ('>< '
                    + ' -> '.join(map(str, self))
                    + ' ||')
        else:
            return ('>< '
                    + ' -> '.join(map(str, self))
                    + ' |' + repr(self._sentinel) + '|')

    def __bool__(self) -> bool:
        return self._count > 0

    def __len__(self) -> int:
        return self._count

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return False

        if self._count != other._count:
            return False
        if self._sentinel is not other._sentinel:
            if self._sentinel != other._sentinel:
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

    def copy(self) -> SplitEnd[D, S]:
        """
        ##### Shallow Copy

        Return a swallow copy of the SplitEnd in O(1) space & time complexity.

        """
        stack: SplitEnd[D, S] = SplitEnd(s=self._sentinel)
        stack._head, stack._count = self._head, self._count
        return stack

    def push(self, *ds: D) -> None:
        """
        ##### Push Data

        Push data onto top of the SplitEnd.

        * ignore "non-existent" Nothing() values pushed on the SplitEnd

        """
        for d in ds:
            if d is not nada:
                node = Node(d, self._head)
                self._head, self._count = node, self._count+1

    @overload
    def pop(self, default: D) -> D|S:
        ...
    @overload
    def pop(self) -> D|S:
        ...
    def pop(self, default: D|Nada=nada) -> D|S|Nada:
        """
        ##### Pop Data

        Pop data off of the top of the SplitEnd.

        * if empty, return a default value
        * if empty and a default value not given, return the sentinel value

        """
        if self._head is None:
            if default is nada:
                return self._sentinel
            else:
                return default
        else:
            data = self._head._data
            self._head, self._count = self._head._next, self._count-1
            return data

    @overload
    def peak(self, default: D) -> D:
        ...
    @overload
    def peak(self) -> D|S:
        ...
    def peak(self, default: D|Nada=nada) -> D|S|Nada:
        """
        ##### Peak at top of SplitEnd

        Returns the data at the top of the SplitEnd.

        * does not consume the data
        * if empty, data does not exist, so in that case return default
        * if empty and no default given, return nothing: Nothing

        """
        if self._head is None:
            return default
        return self._head._data

    @overload
    def head(self, default: D|S) -> D|S:
        ...
    @overload
    def head(self) -> D|S:
        ...
    def head(self, default: D|S|Nada=nada) -> D|S|Nada:
        """
        ##### Head of SplitEnd

        Returns the data at the top of the SplitEnd.

        * does not consume the data
        * for an empty SplitEnd, head does not exist, so return default
        * otherwise return the sentinel value
        * the sentinel value cannot be overridden by nada
          * of course self._sentinel can always be set to nada

        """
        if self._head is None:
            if default is nada:
                return self._sentinel
            else:
                return default
        return self._head._data

    @overload
    def tail(self, default: S) -> SplitEnd[D, S]|S:
        ...
    @overload
    def tail(self) -> SplitEnd[D, S]|S:
        ...
    def tail(self, default: S|Nada=nada) -> SplitEnd[D, S]|S|Nada:
        """
        ##### Tail of SplitEnd
        
        Returns the tail of the SplitEnd if it exists, otherwise returns the
        sentinel value, or a default value of the same type as the sentinel
        value.

        * optional default needs to be of the same type as the sentinel value
          * example:
            * sentinel: tuple(int) = (0,)
            * default: tuple(int) = (42,)
          * decided not to let default: SplitEnd[D, S] as a return option
            * made end code more confusing to reason about
              * not worth cognitive overload when used in client code
              * tended to hide the occurrence of an unusual event occurring
        * the sentinel value cannot be overridden by nada
          * of course self._sentinel can always be set to nada

        """
        if self._head:
            se: SplitEnd[D, S] = SplitEnd(s=self._sentinel)
            se._head = self._head._next
            se._count = self._count - 1
            return se
        else:
            return default

    @overload
    def cons(self, d: D) -> SplitEnd[D, S]: 
        ...
    @overload
    def cons(self, d: Nada) -> Nada: 
        ...
    def cons(self, d: D|Nada) -> SplitEnd[D, S]|Nada:
        """
        ##### Cons SplitEnd with a Head

        Return a new SplitEnd with data as head and self as tail.

        Constructing a SplitEnd using a non-existent value as head results in
        a non-existent SplitEnd. In that case, return sentinel: _S.

        """
        if d is nada:
            return nada
        else:
            stack: SplitEnd[D, S] = SplitEnd(s=self._sentinel)
            stack._head = Node(cast(D, d), self._head)
            stack._count = self._count + 1
            return stack

    def fold(self, f:Callable[[D, D], D]) -> Optional[D]:
        """
        ##### Reduce with `f`

        * returns a value of the of type _T if self is not empty
        * returns None if self is empty
        * folds in natural LIFO Order
        * TODO: consolidate fold & fold1

        """
        node: Optional[Node[D]] = self._head
        if not node:
            return None
        acc: D = node._data
        while node:
            if (node := node._next) is None:
                break
            acc = f(acc, node._data)
        return acc

    def fold1(self, f:Callable[[T, D], T], s: T) -> T:
        """Reduce with f.

        * returns a value of type ~T
        * type ~T can be same type as ~D
        * folds in natural LIFO Order
        * TODO: consolidate fold & fold1

        """
        node: Optional[Node[D]] = self._head
        if not node:
            return s
        acc: T = s
        while node:
            acc = f(acc, node._data)
            node = node._next
        return acc

    def flatMap(self, f: Callable[[D], SplitEnd[T, S]], type: FM=FM.CONCAT) -> SplitEnd[T, S]:
        """
        ##### Bind function to SplitEnd

        Bind function `f` to the SplitEnd.

        * type = CONCAT: sequentially concatenate iterables one after the other
        * type = MERGE: merge iterables together until one is exhausted
        * type = Exhaust: merge iterables together until all are exhausted

        """
        match type:
            case FM.CONCAT:
                return SplitEnd(*concat(*map(lambda x: iter(x), map(f, self))), s=self._sentinel)
            case FM.MERGE:
                return SplitEnd(*merge(*map(lambda x: iter(x), map(f, self))), s=self._sentinel)
            case FM.EXHAUST:
                return SplitEnd(*exhaust(*map(lambda x: iter(x), map(f, self))), s=self._sentinel)
            case '*':
                raise ValueError('Unknown FM type')

    def map(self, f: Callable[[D], T]) -> SplitEnd[T, S]:
        """
        ##### Map `f` over the SplitEnd

        Maps a function (or callable object) over the values on the SplitEnd Stack.

        * TODO: Redo in "natural" order?
        * Returns a new Stack object with shallow copied new data
        * O(n) complexity

        """
        return self.flatMap(lambda a: SplitEnd(f(a)))
