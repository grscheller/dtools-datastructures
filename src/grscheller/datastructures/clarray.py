# Copyright 2023 Geoffrey R. Scheller
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

"""Module grscheller.datastructure.clarray - constant length array.

Module implementing a mutable fixed length  O(1) array data structure
with O(1) data access.
    
None values are not allowed in this data structures. A default iterator can be
defined to swap out None values if stored to the CLArray. If no such function or
iterator is defined, or is exhausted, the data structure defaults back to an
infinite iterator which supplies an infinite steam of empty tuples ().
"""

from __future__ import annotations

__all__ = ['CLArray']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

from typing import Any, Callable, Iterator
from .core.clarray_base import CLArrayBase

class CLArray(CLArrayBase):
    """Constant Length Array

    Class implementing a mutable fixed length array data structure. None values
    are not permitted to be stored to this data structure. A default iterator
    can be defined to swap out None values if stored to the CLArray. If no such
    iterator is defined, or is exhausted, the data structure defaults back to an
    infinite iterator which supplies an infinite stream of empty tuples ().

    Unless specifically resized, this data structure is guaranteed to remain
    a fixed length.

    If size set to None, size to data provided. If size > 0, pad data on right
    with default values or slice off trailing data. If size < 0, pad data on
    left with default value or slice off initial data.
    """
    def __init__(self, *ds,
                 size: int|None=None,
                 noneIter: Iterator|None=None,
                 noneSwap: Any|None=tuple()):

        super().__init__(*ds, size=size, noneIter=noneIter, noneSwap=noneSwap)

    def __str__(self):
        return '[[[' + ', '.join(map(repr, self)) + ']]]'

    def copy(self, noneIter: Iterator|None=None) -> CLArray:
        """Return shallow copy of the CLArray in O(n) complexity."""
        if noneIter is None:
            noneIter = self._none
        return CLArray(*self, noneIter=noneIter)

    def mapSelf(self, f: Callable[[Any], Any]) -> None:
        """Mutate the CLArray by appling function over the CLArray contents."""
        self._ca = CLArray(*map(f, self), noneIter=self._none)._ca

if __name__ == "__main__":
    pass
