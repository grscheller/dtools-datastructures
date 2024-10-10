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

"""### Stack type Data Structures

##### SplitEnd Stack types:

* **SE:** Singularly linked stack with shareable data nodes
* **Roots:** Common root nodes for a collection of SplitEnds

"""

from __future__ import annotations

from typing import Callable, cast, Generic, Iterator, Optional
from ..nodes import SL_Node as Node
from grscheller.fp.woException import MB

__all__ = [ 'SE', 'Roots' ]

class SE[D]():
    """#### Class SE - SplitEnd

    LIFO stacks which can safely share immutable data between themselves.

    * each SplitEnd is a very simple stateful (mutable) LIFO stack
      * top of the stack is the "top"
      * bottom of the stack is the "root" which cannot be removed
    * data can be pushed and popped to the stack
    * different mutable split ends can safely share the same "tail"
    * each SplitEnd sees itself as a singularly linked list
    * bush-like datastructures can be formed using multiple SplitEnds
    * len() returns the number of elements on the SplitEnd stack
    * in boolean context,
      * return false if split end consists of just a root
      * otherwise return true

    """
    __slots__ = '_count', '_head'

    def __init__(self, d: D, *ds: D) -> None:
        self._head = Node(d, MB())
        self._count: int = 1
        for d in ds:
            node: Node[D] = Node(d, MB(self._head))
            self._head, self._count = node, (self._count + 1)

    def __iter__(self) -> Iterator[D]:
        node: Node[D] = self._head
        while node:
            yield node._data
            node = node._next.get()
        yield node._data

    def __reversed__(self) -> Iterator[D]:
        return reversed(list(self))

    def __bool__(self) -> bool:
        # Returns true if not a root node
        return bool(self._head)

    def __len__(self) -> int:
        return self._count

    def __repr__(self) -> str:
        return 'SE(' + ', '.join(map(repr, reversed(self))) + ')'

    def __str__(self) -> str:
        return ('>< ' + ' -> '.join(map(str, self)) + ' ||')

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return False

        if self._count != other._count:
            return False

        left = self._head
        right = other._head
        for _ in range(self._count):
            if left is right:
                return True
            if not left.data_eq(right):
                return False
            left = left._next.get()
            right = right._next.get()

        return True

    def push(self, *ds: D) -> None:
        """Push data onto the top of the SplitEnd."""
        for d in ds:
            node = Node(d, MB(self._head))
            self._head, self._count = node, self._count+1

    def pop(self) -> D:
        """Pop data off of the top of the SplitEnd.

        * removes the data if not at the root
        * just returns the data if at the root

        """
        data = self._head._data
        if (next_node := self._head._next) != MB():
            self._head, self._count = next_node.get(), self._count-1
        return data

    def peak(self) -> D:
        """Return the data at the top of the SplitEnd, does not consume it."""
        return self._head._data

    def fold[T](self, f:Callable[[T, D], T], init: Optional[T]=None) -> T:
        """Reduce with a function.

        * folds in natural LIFO Order

        """
        acc: T
        node: Node[D]
        top: Node[D] = self._head
        if init is None:
            acc = cast(T, top._data)
            node = top._next.get()
        else:
            acc = init
            node = top

        while node:
            acc = f(acc, node._data)
            node = node._next.get()
        return acc

    def copy(self) -> SE[D]:
        """Return a copy of the SplitEnd.

        * O(1) space & time complexity.
        * returns a new instance

        """
        se = SE(self.peak())
        se._head, se._count = self._head, self._count
        return se
