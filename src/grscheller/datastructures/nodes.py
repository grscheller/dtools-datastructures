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
### Nodes for Graphs

Node classes used with graph-like data structures.

"""
from __future__ import annotations
from typing import Generic, Hashable, Optional
from grscheller.fp.woException import MB

__all__ = ['SL_Node', 'DL_Node']

class SL_Node[D]():
    """
    #### Singularly Linked Node

    Singularly link nodes for graph-like data structures.

    * this type of node always contain data, even if that data is None
      * in a Boolean context return true if not last node
    * more than one node can point to the same node forming bush like graphs
    * circular graphs are possible

    """
    __slots__ = '_data', '_next'

    def __init__(self, data: D, next: MB[SL_Node[D]]):
        self._data = data
        self._next = next

    def __bool__(self) -> bool:
        return self._next != MB()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return False

        if self._next is not other._next:
            return False
        if self._data is other._data:
            return True
        elif self._data == other._data:
            return True

        return False

    def data_eq(self, other: SL_Node[D]) -> bool:
        if self._data is other._data:
            return True
        if self._data == other._data:
            return True
        return False

class DL_Node[D]():
    """
    #### Doubly Linked Node

    Doubly linked nodes for graph-like data structures.

    * this type of node always contain data, even if that data is None
      * in a Boolean context return true if not at the start or end node
    * doubly link lists possible
    * circular graphs are possible
    * recursive binary trees possible

    """
    __slots__ = '_data', '_next', '_prev'

    def __init__(self, data: D,
                 prev_node: MB[DL_Node[D]],
                 next_node: MB[DL_Node[D]]):
        self._data = data
        self._prev = prev_node
        self._next = next_node

    def __bool__(self) -> bool:
        if self._next == MB() or self._prev == MB():
            return False
        return True

    def is_start(self) -> bool:
        return self._prev == MB()

    def is_end(self) -> bool:
        return self._next == MB()

class Tree_Node[D]():
    """
    #### Binary Tree Node

    Nodes useful for walking binary trees

    * this type of node always contain data, even if that data is None
      * in a Boolean context return true if not at the top of the tree
    """
    __slots__ = '_data', '_left', '_right', '_up'

    def __init__(self, data: D,
                 up: MB[Tree_Node[D]],
                 left: MB[Tree_Node[D]],
                 right: MB[Tree_Node[D]]):
        self._data = data
        self._up = up
        self._left = left
        self._right = right

    def __bool__(self) -> bool:
        if self._up == MB():
            return False
        else:
            return True

    def is_top(self) -> bool:
        return self._up == MB()
