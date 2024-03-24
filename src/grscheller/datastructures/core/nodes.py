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

from typing import Any

class SL_Node():
    """Class implementing nodes that can be linked together
    to form singularly linked graphs of nodes.

    * this type of node always contain data
    * it has a reference to the next node in the list
    * the next node can be `None` to indicate the end of the list
    * more than one node can point to the same node forming bush like graphs
    * circular graphs are possible
    """
    __slots__ = '_data', '_next'

    def __init__(self, data: Any, next: SL_Node|None):
        """Construct an element of a linked list"""
        self._data = data
        self._next = next

    def __bool__(self):
        # Even if self._data is None
        return True

class BT_Node():
    """**Binary Tree Nodes**

    Class implementing nodes that can be linked together to form tree-like
    graph data structures where data lives in the nodes.

    * this type of node always contain data, even if that data is None
    * originally intended to implement binary tree graphs
    * other use cases possible, like doubly linked lists
    """
    __slots__ = '_data', '_left', '_right'

    def __init__(self, data: Any, left: BT_Node|None, right: LT_Node|None):
        """Construct a data containing node element of some type of graph.
        Usually walked via recursion.
        """
        self._data = data
        self._left = left
        self._right = right

    def __bool__(self):
        # Even if self._data is None
        return True

class LT_Node():
    """**Leaf Tree Nodes**

    Class implementing nodes that can be linked together to form tree-like
    data structures where data lives "on the leaves." 

    * this type of node never contain data
    * both self._left & self._right reference either data or other LT_Nodes
    * while self._root references the node's parent node
    * therefore, to store an LT_Node as data requires a container for it
    """
    __slots__ = '_root', '_left', '_right'

    def __init__(self, left: Any, right: Any, root: LT_Node=None):
        """Construct a node element which contains no data of some type of graph.
        Can be arbitrarily walked.
        """
        self._root = root
        self._left = left
        self._right = right

    def __bool__(self):
        # Return True if the LT_Node has no leaves
        return LT_Node == type(self._left) == type(self._right)

if __name__ == "__main__":
    pass
