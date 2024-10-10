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

* **FSE:** Stack with shareable data nodes and functional interface
* **FRoots:** Common root nodes for a collection of SplitEnds

"""

from __future__ import annotations

from typing import Callable, cast, Generic, Hashable, Iterator, Optional, TypeVar
from ..nodes import SL_Node as Node

__all__ = [ 'FSE', 'FRoots' ]

D = TypeVar('D', bound=Hashable)
T = TypeVar('T')

class FRoots(Generic[D]):
    # TODO: has-a roots and dict of tails
    """#### Class for SplitEnd root storage.

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

class FSE(Generic[D]):
    # TODO: has-a SE or just a pointer to a head???
    # TODO: cons will add it to the dict of tails in FROOTS
    """#### Class FSE - Functional SplitEnd

    LIFO stacks which can safely share immutable data between themselves.

    * each FSE is an immutable reference to the top of a LIFO stack
      * top of the stack is the "head"
      * the rest of the stack is the "tail"
      * bottom of the stack is the "root" which cannot be removed
    * different `FSE` can safely share the same "tail"
    * each SplitEnd sees itself as a singularly linked list
    * bush-like datastructures can be formed using multiple SplitEnds
    * len() returns the number of elements on the stack
    * in boolean context,
      * return false if split end consists of just a root
      * otherwise return true

    """
    __slots__ = '_root_nodes',

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
