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

"""Module grscheller.datastructure.flArray - Double sided queue

Implements fixed length arrays of values of arbitrary types. O(1) data access
which will store None values. The arrays must have length > 0.
"""

from __future__ import annotations

__all__ = ['FLArray']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

from typing import Any, Callable, Never, Self, Union
from .iterlib import mapIter, concatIters, mergeIters

class FLArray():
    """Class representing a fixed length array data structure of length > 0.
    Permits storing None as a value.
    """
    def __init__(self, *ds, size: int = 0, default: Any = None):
        """Construct a fixed length array
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
                    # ensure flArray not empty
                    self._size = 1
                    self._list = [default]
            case (_, True, _):
                # no size inconsistencies
                self._size = dsize
                self._list = dlist
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
        """Returns true if not all values evaluate as False"""
        for ii in range(self._size):
            if self._list[ii]:
                return True
        return False

    def __len__(self) -> int:
        """Returns the size of the flArray"""
        return self._size

    def __getitem__(self, index: int) -> Union[Any, Never]:
        # TODO: Does not like being given a slice ... research
        cnt = self._size
        if not -cnt <= index < cnt:
            l = -cnt
            h = cnt - 1
            msg = f'fdArray index = {index} not between {l} and {h} while getting value'
            raise IndexError(msg)
        return self._list[index]

    def __setitem__(self, index: int, value: Any) -> Union[None, Never]:
        cnt = self._size
        if not -cnt <= index < cnt:
            l = -cnt
            h = cnt - 1
            msg = f'fdArray index = {index} not between {l} and {h} while getting value'
            raise IndexError(msg)
        self._list[index] = value

    def __iter__(self):
        """Iterator yielding data currently stored in flArray"""
        currList = self._list.copy()
        for pos in range(self._size):
            yield currList[pos]

    def __reversed__(self):
        """Reverse iterate over the current state of the flArray"""
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
        """Display data in flArray"""
        listStrs = []
        for data in self:
            listStrs.append(repr(data))
        return "[| " + ", ".join(listStrs) + " |]"

    def copy(self) -> FLArray:
        """Return shallow copy of the flArray in O(n) time & space complexity"""
        return FLArray(*self)

    def map(self, f: Callable[[Any], Any]) -> FLArray:
        """Apply function over flArray contents, returns new instance"""
        return FLArray(*mapIter(iter(self), f))

    def mapSelf(self, f: Callable[[Any], Any]) -> Self:
        """Apply function over flArray contents"""
        for idx in range(self._size):
            self._list[idx] = f(self._list[idx])
        return self

    def flatMap(self, f: Callable[[Any], FLArray]) -> FLArray:
        """Apply function and flatten result, returns new instance"""
        return FLArray(
            *concatIters(
                *mapIter(mapIter(iter(self), f), lambda x: iter(x))
            )
        )

    def flatMapSelf(self, f: Callable[[Any], FLArray]) -> Self:
        """Apply function to contents and flatten result"""
        donor = self.flatMap(f)
        self._size = donor._size
        self._list = donor._list
        return self

    def mergeMap(self, f: Callable[[Any], FLArray]) -> FLArray:
        """Apply function and flatten result, returns new instance"""
        return FLArray(
            *mergeIters(
                *mapIter(mapIter(iter(self), f), lambda x: iter(x))
            )
        )

    def mergeMapSelf(self, f: Callable[[Any], FLArray]) -> Self:
        """Apply function and merge to flatten result, returns new instance"""
        donor = self.mergeMap(f)
        self._size = donor._size
        self._list = donor._list
        return self
if __name__ == "__main__":
    pass
