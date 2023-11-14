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

"""Module grscheller.datastructure.clarray - constant length array

Module implementing a data structure with a fixed length and O(1) data
access. The arrays will have length > 0 and are guaranteed not to change size.

Note: None values are allowed in this data structures due to the
      fixed length size guarantees provided by the CLArray class.
"""

from __future__ import annotations

__all__ = ['CLArray']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

from typing import Any, Callable, Never, Union
from itertools import chain
from .core.iterlib import exhaust, merge

class CLArray():
    """Class implementing a stateful fixed length array data structure of
    length > 0.

    Guaranteed to be of length |size| for size != 0

    If size not indicated (or 0), size to data provided. Also when no data
    is provided, return array with a default value and a size = 1.

    If size > 0, pad data on right with a default or slice off trailing data.

    If size < 0, pad data on left with a default or slice off initial data.

    Permits storing None as a value.
    """
    def __init__(self, *ds, size: int = 0, default: Any=None):
        """Construct a fixed length array, None values allowed."""
        def swapNones(d: Any):
            if d is None:
                return default
            return d
        self._default = default
        dlist = list(map(swapNones, ds))
        dsize = len(dlist)
        match (size, abs(size) == dsize, abs(size) > dsize):
            case (0, _, _):
                # default to the size of the data given
                if dsize > 0:
                    self._size = dsize
                    self._list = dlist
                else:
                    # ensure CLArray not empty
                    self._size = 1
                    self._list = [default]
            case (_, True, _):
                # no size inconsistencies
                if dsize > 0:
                    self._size = dsize
                    self._list = dlist
                else:
                    # ensure CLArray not empty
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
        """Returns the size of the CLArray"""
        return self._size

    def __getitem__(self, index: int) -> Union[Any, Never]:
        size = self._size
        if not -size <= index < size:
            l = -size
            h = size - 1
            msg = f'CLArray index = {index} not between {l} and {h}'
            msg += ' while getting value'
            raise IndexError(msg)
        return self._list[index]

    def __setitem__(self, index: int, value: Any) -> Union[None, Never]:
        size = self._size
        if not -size <= index < size:
            l = -size
            h = size - 1
            msg = f'CLArray index = {index} not between {l} and {h}'
            msg += ' while setting value'
            raise IndexError(msg)
        self._list[index] = value

    def __iter__(self):
        """Iterate over the current dtate of the CLArray. Copy is made so
        original source can safely mutate.
        """
        for data in self._list.copy():
            yield data

    def __reversed__(self):
        """Reverse iterate over the current state of the CLArray. Copy is
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
        """Display data in the CLArray"""
        # __iter__ already makes a defensive copy
        return "[|" + ", ".join(map(repr, self)) + "|]"

    def __add__(self, other: CLArray) -> CLArray:
        """Add CLArray component-wise left to right."""
        if (lhs := self._size) != (rhs := other._size):
            msg = 'CLArray size mismatch: '
            msg += f'LHS size={lhs} but RHS size={rhs}'
            raise ValueError(msg)
        clarray = CLArray(size=lhs)
        for ii in range(lhs):
            clarray[ii] = self[ii] + other[ii]
        return clarray

    def copy(self) -> CLArray:
        """Return shallow copy of the CLArray in O(n) time & space complexity"""
        return CLArray(*self)

    def reverse(self) -> None:
        """Reversed the CLArray"""
        self._list.reverse()

    def map(self, f: Callable[[Any], Any], size: int=0) -> CLArray:
        """Apply function f over the CLArray contents. Return a new CLArray
        with the mapped contents. Use self._default if f teturns None.
        """
        return CLArray(*map(f, self), size=size, default=self._default)

    def mapSelf(self, f: Callable[[Any], Any]) -> None:
        """Mutate the CLArray by appling function over the CLArray contents."""
        self._list = CLArray(*map(f, self), default=self._default)._list

if __name__ == "__main__":
    pass
