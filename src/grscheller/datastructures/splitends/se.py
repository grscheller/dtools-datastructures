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

from typing import Callable, cast, Generic, Hashable, Iterator, Optional, TypeVar
from ..nodes import SL_Node as Node
from grscheller.fp.woException import MB

__all__ = [ 'SE', 'Roots' ]

D = TypeVar('D', bound=Hashable)
T = TypeVar('T')

class Roots(Generic[D]):
    """#### Class for SplitEnd root storage.

    * allows multiple SplitEnds to share a collection of roots

    """
    __slots__ = '_roots', '_permit_new_roots'

    def __init__(self, *roots: D, permit_new_roots: bool=True) -> None:
        self._permit_new_roots = permit_new_roots
        self._roots: dict[D, Node[D]] = {}
        for root in roots:
            self._roots[root] = Node(root, MB())

    def get_root_node(self, root: D) -> Node[D]:
        if root not in self._roots:
            if self._permit_new_roots:
                self._roots[root] = Node(root, MB())
            else:
                msg = "SplitEnd: permit_new_roots set to False"
                raise ValueError(msg)
        return self._roots[root]

    def new_root_node(self, root: D) -> None:
        if root not in self._roots:
            self._roots[root] = Node(root, MB())

class SE(Generic[D]):
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
    __slots__ = '_count', '_root_nodes', '_head', '_root'

    def __init__(self, root_nodes: Roots[D], root: D, *ds: D) -> None:
        self._root_nodes = root_nodes
        self._root: Node[D] = root_nodes.get_root_node(root)
        self._head = self._root
        self._count: int = 1
        for d in ds:
            node: Node[D] = Node(d, MB(self._head))
            self._head = node
            self._count += 1

    def __iter__(self) -> Iterator[D]:
        node: Node[D]|None = self._head
        while node is not None:
            yield node._data
            node = node._next.get()

    def __reversed__(self) -> Iterator[D]:
        data = list(self)
        return reversed(data)

    def __bool__(self) -> bool:
        # Returns true if not a root node
        return self._head is not self._root

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

        left: Node[D] = self._head
        right: Node[D] = other._head
        nn = self._count
        while nn > 0:
            if left is right:
                return True
            if left == MB() or right == MB():
                return True
            if left._data != right._data:
                return False
            left = left._next.get()
            right = right._next.get()
            nn -= 1
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

    def root(self) -> D:
        """Return the data at the root of the SplitEnd."""
        return self._root._data

    def fold(self, f:Callable[[T, D], T], init: Optional[T]=None) -> T:
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
        se = SE(self._root_nodes, self._root._data)
        se._head, se._count = self._head, self._count
        return se
