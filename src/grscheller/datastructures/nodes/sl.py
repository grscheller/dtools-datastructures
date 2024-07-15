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

"""Singularly link nodes for graph-like data structures."""

from __future__ import annotations

__all__ = ['SL_Node']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023-2024 Geoffrey R. Scheller"
__license__ = "Apache License 2.0"

from typing import Generic, Optional, TypeVar

_T = TypeVar('_T')

class SL_Node(Generic[_T]):
    """Class for singularly link nodes for graph-like data structures.

    * this type of node always contain data, even if that data is None
    * more than one node can point to the same node forming bush like graphs
    * circular graphs are possible
    """
    __slots__ = '_data', '_next'

    def __init__(self, data: _T, next: Optional[SL_Node[_T]]):
        self._data = data
        self._next = next

    def __bool__(self) -> bool:
        """Singularly linked nodes always contain data.

        * always returns true
        * this type of node always contain data, even if that data is None
        """
        return True
