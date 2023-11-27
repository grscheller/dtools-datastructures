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

"""Module grscheller.datastructure.fclarray - constant length array.

Module implementing a mutable fixed length, single queueable array data
structure with O(1) data access.
    
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

from typing import Any, Callable, Never, Union, Iterator
from .core.fp import Some
from .core.carray import CArray
from .core.utils import infiniteEmptyTPs

class CLArray():
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
    def __init__(self, *ds, size: int|None=None, noneSwap: Iterator|None=None):

        self._sizeMB = Some(size)
        self._swNoneIterMB = Some(noneSwap)
        self._swap = self._swNoneIterMB.get(infiniteEmptyTPs())
        swap = self._swap

        ca = CArray()
        for d in ds:
            if d is not None:
                ca.pushR(d)
            else:
                ca.pushR(next(swap))
        ds_size = len(ca)

        if size is None:
            abs_size = size = ds_size
        else:
            abs_size = abs(size)

        if abs_size == ds_size:
            # no size inconsistencies
            self._ca, self._sizeMB = ca, Some(ds_size)
        elif abs_size > ds_size:
            if size > 0:
                # pad higher indexes (on "right")
                for _ in range(size-ds_size):
                    ca.pushR(next(swap))
                self._ca, self._sizeMB = ca, Some(size)
            else:
                # pad lower indexes (on "left")
                for _ in range(-size - ds_size):
                    ca.pushL(next(swap))
                self._ca, self._sizeMB = ca, Some(-size)
        else:
            if size > 0:
                # ignore extra data at end
                for _ in range(size - ds_size):
                    ca.popR()
                self._ca, self._sizeMB = ca, Some(size)
            else:
                # ignore extra data at beginning
                for _ in range(ds_size + size):
                    ca.popL()
                self._ca, self._sizeMB = ca, Some(-size)

    def __iter__(self):
        """Iterate over the current state of the CLArray. Copy is made
        so original source can safely mutate.
        """
        for data in self._ca.copy():
            yield data

    def __reversed__(self):
        """Reverse iterate over the current state of the CLArray. Copy is made
        so original source can safely mutate.
        """
        for data in reversed(self._ca.copy()):
            yield data

    def __repr__(self):
        # TODO: rethink this one?
        repr1 = f'{self.__class__.__name__}('
        repr2 = ', '.join(map(repr, self))
        if repr2 == '':
            repr3 = f'default={self._swNoneIterMB.get()})'
        else:
            repr3 = f', default={self._swNoneIterMB.get()})'
        return repr1 + repr2 + repr3

    def __str__(self):
        return '[[[' + ', '.join(map(repr, self)) + ']]]'

    def __bool__(self):
        """Return true only if there exists an array value not equal to the
        empty tuple (). Empty arrays always return false.
        """
        for value in self:
            if value != ():
                return True
        return False

    def __len__(self) -> int:
        """Returns the size of the CLArray"""
        return self._sizeMB.get()

    def __getitem__(self, index: int) -> Union[Any,Never]:
        return self._ca[index]

    def __setitem__(self, index: int, value: Any) -> Union[None,Never]:
        if value is not None:
            self._ca[index] = value
        else:
            # TODO: need to handle "StopIteration"
            self._ca[index] = next(self._swap)

    def __eq__(self, other: Any):
        """Returns True if all the data stored in both compare as equal. Worst
        case is O(n) behavior for the true case. The default value play no role
        in determining equality.
        """
        if not isinstance(other, type(self)):
            return False
        return self._ca == other._ca

    def copy(self, noneSwap: Any=None) -> CLArray:
        """Return shallow copy of the CLArray in O(n) complexity."""
        if noneSwap is None:
            noneSwap = self._swNoneIterMB.get(infiniteEmptyTPs())
        return CLArray(*self, noneSwap=noneSwap)

    def reverse(self) -> None:
        """Reverse the elements of the CLArray. Mutates the CLArray."""
        self._ca = self._ca.reverse()

    def map(self, f: Callable[[Any], Any]) -> None:
        """Mutate the CLArray by appling function over the CLArray contents."""
        # Is sharing this iterator what I want to do???
        self._ca = CLArray(*map(f, self), self._swap)._ca

    def resize(self, size: int):
        self._sizeMB, self._ca = Some(size), CLArray(
            *self, size=size, noneSwap=self._swNoneIterMB.get(infiniteEmptyTPs()))._ca
        
if __name__ == "__main__":
    pass
