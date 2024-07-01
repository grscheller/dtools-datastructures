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

"""Various types of nodes for graph-like data structures.

* heap based nodes for for tree-like data structures
* data structures should make nodes inaccessible to client code
* making nodes inaccessible promotes data sharing between data structures
"""
from __future__ import annotations

__all__ = ['SL_Node', 'BT_Node', 'LT_Node']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023-2024 Geoffrey R. Scheller"
__license__ = "Apache License 2.0"

from typing import Any, Generic, Optional, TypeVar

_T = TypeVar('_T')

class SL_Node(Generic[_T]):
    """Class implementing nodes that can be linked together
    to form singularly linked graphs of nodes.

    * this type of node always contain data
    * it has a reference to the next node in the list
    * the next node can be `None` to indicate the end of the list
    * more than one node can point to the same node forming bush like graphs
    * circular graphs are possible
    """
    __slots__ = '_data', '_next'

    def __init__(self, data: _T, next: Optional[SL_Node[_T]]):
        """Construct an element of a linked list"""
        self._data = data
        self._next = next

    def __bool__(self) -> bool:
        """singularly linked nodes always contain data.

        * always returns true
        * this type of node always contain data, even if that data is None

        """
        return True

class BT_Node(Generic[_T]):
    """**Binary Tree Nodes**

    Class implementing nodes that can be linked together to form tree-like
    graph data structures where data lives in the nodes.

    * this type of node always contain data, even if that data is None
    * originally intended to implement binary tree graphs
    * other use cases possible, like doubly linked lists
    """
    __slots__ = '_data', '_left', '_right'

    def __init__(self, data: _T, left: Optional[BT_Node[_T]], right: Optional[BT_Node[_T]]):
        """Construct a data containing node element of some type of graph.

        * usually walked via recursion.
        """
        self._data = data
        self._left = left
        self._right = right

    def __bool__(self) -> bool:
        """binary tree nodes always contain data.

        * always returns true
        * this type of node always contain data, even if that data is None

        """
        return True

if __name__ == "__main__":
    pass
