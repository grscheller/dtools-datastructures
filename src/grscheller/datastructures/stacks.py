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

##### Stack types:

* **SplitEnd:** Singularly linked stack with shareable data nodes
  * **SplitEndRoots:** Common root nodes for a collection of SplitEnds
* **SplitEndMut:** Singularly linked stack with shareable data nodes
  * **SplitEndRootsMut:** Common root nodes for a collection of SplitEndMuts

"""

from __future__ import annotations

from typing import Callable, cast, Generic, Hashable, Iterator, Optional, TypeVar
from .nodes import SL_Node as Node

__all__ = [ 'SplitEndBase', 'Roots',
            'SplitEnd', 'SplitEndRoots',
            'SplitEndMut', 'SplitEndMutRoots' ]

D = TypeVar('D', bound=Hashable)
T = TypeVar('T')

class Roots(Generic[D]):
    """#### Base Class for SplitEnd & SplitEndMut root storage.

    * allows multiple SplitEnds to share a collection of roots

    """
    __slots__ = '_roots', '_permit_new_roots'

    def __init__(self, *roots: D, permit_new_roots: bool=True) -> None:
        self._permit_new_roots = permit_new_roots
        self._roots: dict[D, Node[D]] = {}
        for root in roots:
            self._roots[root] = Node(root, None)

    def get_root_node(self, root: D) -> Node[D]:
        if root not in self._roots:
            if self._permit_new_roots:
                self._roots[root] = Node(root, None)
            else:
                msg = "SplitEnd: permit_new_roots set to False"
                raise ValueError(msg)
        return self._roots[root]

    def new_root_node(self, root: D) -> None:
        if root not in self._roots:
            self._roots[root] = Node(root, None)

class SplitEndRoots(Roots[D]):
    """#### Class for SplitEnd root storage."""
    __slots__ = ()

class SplitEndMutRoots(Roots[D]):
    """#### Class for SplitEndMut root storage."""
    __slots__ = ()

class SplitEndBase(Generic[D]):
    __slots__ = '_count', '_root_nodes', '_head', '_root'

    def __init__(self, root_nodes: Roots[D], root: D, *ds: D) -> None:
        self._root_nodes = root_nodes
        self._root: Node[D] = root_nodes.get_root_node(root)
        self._head = self._root
        self._count: int = 1
        for d in ds:
            node: Node[D] = Node(d, self._head)
            self._head = node
            self._count += 1

    def __iter__(self) -> Iterator[D]:
        node: Node[D]|None = self._head
        while node is not None:
            yield node._data
            node = node._next

    def __reversed__(self) -> Iterator[D]:
        data = list(self)
        return reversed(data)

    def __bool__(self) -> bool:
        # Returns true if not a root node
        return self._head is not self._root

    def __len__(self) -> int:
        return self._count

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return False

        if self._count != other._count:
            return False

        left: Optional[Node[D]] = self._head
        right: Optional[Node[D]] = other._head
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

    def root(self) -> D:
        """Return the data at the root of the SplitEnd."""
        return self._root._data

    def fold(self, f:Callable[[T, D], T], init: Optional[T]=None) -> T:
        """Reduce with a function.

        * folds in natural LIFO Order

        """
        acc: T
        node: Optional[Node[D]]
        top: Node[D] = self._head
        if init is None:
            acc = cast(T, top._data)
            node = top._next
        else:
            acc = init
            node = top

        while node:
            acc = f(acc, node._data)
            node = node._next
        return acc

class SplitEnd(SplitEndBase[D]):
    """#### SplitEnd

    LIFO stacks which can safely share immutable data between themselves.

    * each `SplitEnd` is an immutable reference to the top of a LIFO stack
      * top of the stack is the "head"
      * bottom of the stack is the "root" which cannot be removed
    * different `SplitEnds` can safely share the same "tail"
    * each split end sees itself as a singularly linked list
    * bush-like datastructures can be formed using multiple split ends
    * len() returns the number of elements on the stack
    * in boolean context,
      * return false if split end consists of just a root
      * otherwise return true

    """
    __slots__ = '_root_nodes',

    def __init__(self, root_nodes: SplitEndRoots[D], root: D, *ds: D) -> None:
        super().__init__(root_nodes, root, *ds)

    def __repr__(self) -> str:
        return 'SplitEnd(' + ', '.join(map(repr, reversed(self))) + ')'

    def __str__(self) -> str:
        return ('>< ' + ' -> '.join(map(str, self)) + ' ||')

    def head(self) -> D:
        """Return the data at the top of the SplitEnd, does not consume it."""
        return self._head._data

    def tail(self) -> SplitEnd[D]:
        """Get tail of the SplitEnd, where the tail of a root is itself.

        * SplitEnds must always contain a root
          * to make this method total, a tail of a root is itself

        """
        if self._head is self._root:
            return self
        else:
            root_nodes = cast(SplitEndRoots[D], self._root_nodes)
            se: SplitEnd[D] = SplitEnd(root_nodes, self._root._data)
            se._head, se._count = cast(Node[D], self._head._next), self._count-1
            return se

    def cons(self, head: D) -> SplitEnd[D]:
        """Cons SplitEnd with a head.

        * return a new SplitEnd instance by appending head to itself
        * does not mutate original SplitEnd

        """
        root_nodes = cast(SplitEndRoots[D], self._root_nodes)
        se: SplitEnd[D] = SplitEnd(root_nodes, self._root._data)
        se._head, se._count = Node(head, self._head), self._count + 1
        return se

class SplitEndMut(SplitEndBase[D]):
    """#### SplitEndMut

    LIFO stacks which can safely share immutable data between themselves.

    * each `SplitEndMut` is a very simple stateful (mutable) LIFO stack
      * top of the stack is the "top"
      * bottom of the stack is the "root" which cannot be removed
    * data can be pushed and popped to the stack
    * different mutable split ends can safely share the same "tail"
    * each split end sees itself as a singularly linked list
    * bush-like datastructures can be formed using multiple split ends
    * len() returns the number of elements on the stack
    * in boolean context,
      * return false if split end consists of just a root
      * otherwise return true

    """
    __slots__ = ()

    def __init__(self, root_nodes: SplitEndMutRoots[D], root: D, *ds: D) -> None:
        super().__init__(root_nodes, root, *ds)

    def __repr__(self) -> str:
        return 'SplitEndMut(' + ', '.join(map(repr, reversed(self))) + ')'

    def __str__(self) -> str:
        return ('>< ' + ' -> '.join(map(str, self)) + ' ||')

    def push(self, *ds: D) -> None:
        """Push data onto the top of the SplitEnd."""
        for d in ds:
            node = Node(d, self._head)
            self._head, self._count = node, self._count+1

    def pop(self) -> D:
        """Pop data off of the top of the SplitEnd.

        * removes the data if not at the root
        * just returns the data if at the root

        """
        data = self._head._data
        if (next_node := self._head._next) is not None:
            self._head, self._count = next_node, self._count-1
        return data

    def peak(self) -> D:
        """Return the data at the top of the SplitEnd, does not consume it."""
        return self._head._data

    def copy(self) -> SplitEndMut[D]:
        """Return a swallow copy of the SplitEnd.

        * O(1) space & time complexity.

        """
        root_nodes = cast(SplitEndMutRoots[D], self._root_nodes)
        se: SplitEndMut[D] = SplitEndMut(root_nodes, self._root._data)
        se._head, se._count = self._head, self._count
        return se
