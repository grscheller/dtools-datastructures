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

* designed to be "tinker-toyed" together in a variety of ways
* passive data structures manipulated by the classes containing them

"""
from __future__ import annotations
from typing import Generic, Optional, TypeVar

__all__ = ['SL_Node', 'DL_Node']

T = TypeVar('T')

class SL_Node(Generic[T]):
    """
    #### Singularly Linked Node

    Class implements singularly link nodes for graph-like data structures.

    * this type of node always contain data, even if that data is None
      * in a Boolean context always returns true
    * more than one node can point to the same node forming bush like graphs
    * circular graphs are possible

    """
    __slots__ = '_data', '_next'

    def __init__(self, data: T, next: Optional[SL_Node[T]]):
        self._data = data
        self._next = next

    def __bool__(self) -> bool:
        return True

class DL_Node(Generic[T]):
    """
    #### Doubly Linked Node

    Class implements doubly linked nodes for graph-like data structures.

    * this type of node always contain data, even if that data is None
      * in a Boolean context always returns true
    * recursive binary trees possible
    * doubly link lists possible
    * circular graphs are possible

    """
    __slots__ = '_data', '_left', '_right'

    def __init__(self, left: Optional[DL_Node[T]], data: T, right: Optional[DL_Node[T]]):
        self._data = data
        self._left = left
        self._right = right

    def __bool__(self) -> bool:
        return True
