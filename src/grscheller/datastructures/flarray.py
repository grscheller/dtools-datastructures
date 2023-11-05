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

"""Module grscheller.datastructure.flarray - Fixed length array

Implements fixed length arrays of values of arbitrary types. O(1) data access
which will store None values. The arrays must have length > 0 and are
guarnteed not to change size.
"""

from __future__ import annotations

__all__ = ['FLArray']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

from typing import Any, Callable, Never, Self, Union
from itertools import chain
from .core.iterlib import exhaust, merge

class FLArray():
    """Class implementing a stateful fixed length array data structure of
    length > 0. Permits storing None as a value.
    """
    def __init__(self, *ds, size: int = 0, default: Any = None):
        """Construct a fixed length array, do not "swallow" None values.
           - guarnteed to be of length |size| for size != 0
           - if size not indicated (or 0), size to data provided
             - if no data provided, return array with default value of size = 1
           - assign missing values the default value
           - if size < 0, pad provided data on left or slice it on the right
        """
        dlist = list(ds)
        dsize = len(dlist)
        match (size, abs(size) == dsize, abs(size) > dsize):
            case (0, _, _):
                # default to the size of the data given
                if dsize > 0:
                    self._size = dsize
                    self._list = dlist
                else:
                    # ensure FLArray not empty
                    self._size = 1
                    self._list = [default]
            case (_, True, _):
                # no size inconsistencies
                if dsize > 0:
                    self._size = dsize
                    self._list = dlist
                else:
                    # ensure FLArray not empty
                    self._size = 1
                    self._list = [default]
            case (_, _, True):
                if size > 0:
                    # pad higher indexes (on "right")
                    self._size = size
                    self._list = dlist + [default]*(size - dsize)
                else:
                    # pad lower indexes (on "left")
                    dlist.reverse()
                    dlist += [default]*(-size - dsize)
                    dlist.reverse()
                    self._size = -size
                    self._list = dlist + [default]*(size - dsize)
            case _:
                if size > 0:
                    # take left slice, ignore extra data at end
                    self._size = size
                    self._list = dlist[0:size]
                else:
                    # take right slice, ignore extra data at beginning
                    self._size = -size
                    self._list = dlist[dsize+size:]

    def __bool__(self):
        """Return true if all stored values are not None."""
        for value in self:
            if value is not None:
                return True
        return False

    def __len__(self) -> int:
        """Returns the size of the flarray"""
        return self._size

    def __getitem__(self, index: int) -> Union[Any, Never]:
        size = self._size
        if not -size <= index < size:
            l = -size
            h = size - 1
            msg = f'FLArray index = {index} not between {l} and {h}'
            msg += ' while getting value'
            raise IndexError(msg)
        return self._list[index]

    def __setitem__(self, index: int, value: Any) -> Union[None, Never]:
        size = self._size
        if not -size <= index < size:
            l = -size
            h = size - 1
            msg = f'FLArray index = {index} not between {l} and {h}'
            msg += ' while setting value'
            raise IndexError(msg)
        self._list[index] = value

    def __iter__(self):
        """Iterate over the current dtate of the flarray. Copy is made so
        original source can safely mutate.
        """
        for data in iter(self._list.copy()):
            yield data

    def __reversed__(self):
        """Reverse iterate over the current state of the flarray. Copy is
        made so original source can safely mutate.
        """
        for data in reversed(self._list.copy()):
            yield data

    def __eq__(self, other):
        """Returns True if all the data stored in both compare as equal.
        Worst case is O(n) behavior for the true case.
        """
        if not isinstance(other, type(self)):
            return False
        return self._list == other._list

    def __repr__(self):
        """Display data in flarray"""
        # __iter__ already makes a defensive copy
        return "[|" + ", ".join(map(lambda x: repr(x), iter(self))) + "|]"

    def __add__(self, other: FLArray) -> FLArray:
        """Add FLArrays component-wise left to right."""
        if (lhs := self._size) != (rhs := other._size):
            msg = 'FLArray size mismatch: '
            msg += f'LHS size={lhs} but RHS size={rhs}'
            raise ValueError(msg)
        flarray = FLArray(size=lhs)
        for ii in range(lhs):
            flarray[ii] = self[ii] + other[ii]
        return flarray

    def copy(self) -> FLArray:
        """Return shallow copy of the flarray in O(n) time & space complexity"""
        return FLArray(*self)

    def reverse(self) -> None:
        """Reversed the FLArray"""
        self._list.reverse()

    def map(self, f: Callable[[Any], Any], mut: bool=True) -> Self|FLArray:
        """Apply function over flarray contents.

        Return new FLArray if mut=False (the default)
        otherwise mutate the data structure and return self.
        """
        newFLArray  = FLArray(*map(f, iter(self)))
        if mut:
            self._list = newFLArray._list
            return self
        return newFLArray

    def flatMap(self, f: Callable[[Any], FLArray]) -> FLArray:
        """Apply function and flatten result, returns only a
        new instance since size may change.

        Merge the flarrays produced sequentially left-to-right.
        """
        return FLArray(*chain(
            *map(lambda x: iter(x), map(f, iter(self)))
        ))

    def mergeMap(self, f: Callable[[Any], FLArray]) -> FLArray:
        """Apply function and flatten result, returns only a instance
        since size may change.

        Round Robin Merge the flarrays produced until first cached
        flarray is exhausted.
        """
        return FLArray(*merge(
            *map(lambda x: iter(x), map(f, iter(self)))
        ))

    def exhaustMap(self, f: Callable[[Any], FLArray]) -> FLArray:
        """Apply function and flatten result, returns new instance
        only since size may change.

        Round Robin Merge the flarrays produced until all cached
        flarrays are exhausted.
        """
        return FLArray(*exhaust(
            *map(lambda x: iter(x), map(f, iter(self)))
        ))

if __name__ == "__main__":
    pass
