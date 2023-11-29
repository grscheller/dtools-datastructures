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

Module implementing an mutable fixed length data structure with O(1) data
access. All mutating methods are guaranteed not to change the length of the
data structure.

None values are not allowed in this data structures. An immutable default value
is set upon instantiating. If no default value is given, the empty tuple () is
used in lieu of None, but is not set as the default value. Method which return
new FCLArray values can set a different default value for the new instance.
"""

from __future__ import annotations

__all__ = ['FCLArray']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

from typing import Any, Callable, Never, Union, Iterator
from itertools import chain, cycle
from .core.iterlib import merge, exhaust
from .core.fp import FP
from .core.carray import CArray

class FCLArray(FP):
    """Functional Constant Length Array

    Class implementing a mutable fixed length array data structure whose
    mutaing methods are guaranteed not to change the length of the data
    structure.

    If size set to None, size to data provided.
    If size > 0, pad data on right with default value or slice off trailing data.
    If size < 0, pad data on left with default value or slice off initial data.

    Does not permits storing None as a value. If a default value is not set, the
    empty tuple () is used in lieu of None, but () is not set as the default
    value.
    """
    def __init__(self, *ds,
                 size: int|None=None,
                 noneIter: Iterator|None=None,
                 noneSwap: Any|None=tuple()):

        match (noneIter, noneSwap):
            case (None, None):
                raise ValueError("noneIter & noneSwap both cannot be None")
            case (None, swap):
                self._none = cycle((swap,))
            case (none, None):
                self._none = none  # could throw StopIteration exception
            case (none, swap):
                self._none = chain(none, cycle((swap,)))

        ca = CArray()
        none = self._none
        
        for d in ds:
            if d is None:
                ca.pushR(next(none))
            else:
                ca.pushR(d)

        ds_size = len(ca)

        if size is None:
            abs_size = size = ds_size
        else:
            abs_size = abs(size)

        if abs_size > ds_size:
            if size > 0:
                # pad higher indexes (on "right")
                for _ in range(size-ds_size):
                    ca.pushR(next(none))
            else:
                # pad lower indexes (on "left")
                for _ in range(-size - ds_size):
                    ca.pushL(next(none))
        else:
            if size > 0:
                # ignore extra data at end
                for _ in range(size - ds_size):
                    ca.popR()
            else:
                # ignore extra data at beginning
                for _ in range(ds_size + size):
                    ca.popL()
        self._ca = ca

    def __iter__(self):
        """Iterate over the current state of the FCLArray. Copy is made
        so original source can safely mutate.
        """
        for data in self._ca.copy():
            yield data

    def __reversed__(self):
        """Reverse iterate over the current state of the FCLArray. Copy is made
        so original source can safely mutate.
        """
        for data in reversed(self._ca.copy()):
            yield data

    def __repr__(self):
        repr1 = f'{self.__class__.__name__}('
        repr2 = ', '.join(map(repr, self))
        if repr2 == '':
            repr3 = f'noneIter={self._none})'
        else:
            repr3 = f', noneIter={self._none}'
        return repr1 + repr2 + repr3

    def __str__(self):
        return '[|' + ', '.join(map(repr, self)) + '|]'

    def __bool__(self):
        """Return true only if there exists an array value not equal to the
        empty tuple (). Empty arrays always return false.
        """
        for value in self:
            if value != ():
                return True
        return False

    def __len__(self) -> int:
        """Returns the size of the FCLArray"""
        return len(self._ca)

    def __getitem__(self, index: int) -> Union[Any,Never]:
        return self._ca[index]

    def __setitem__(self, index: int, value: Any) -> Union[None,Never]:
        if value is None:
            self._ca[index] = next(self._none)
        else:
            self._ca[index] = value

    def __eq__(self, other: Any):
        """Returns True if all the data stored in both compare as equal. Worst
        case is O(n) behavior for the true case. The default value play no role
        in determining equality.
        """
        if not isinstance(other, type(self)):
            return False
        return self._ca == other._ca

    def reverse(self) -> None:
        """Reverse the elements of the CLArray. Mutates the CLArray."""
        self._ca = self._ca.reverse()

    def copy(self, noneIter: Iterator|None=None) -> FCLArray:
        """Return shallow copy of the CLArray in O(n) complexity."""
        if noneIter is None:
            noneIter = self._none
        return FCLArray(*self, noneIter=noneIter)

    def mapSelf(self, f: Callable[[Any], Any]) -> None:
        """Mutate the FCLArray by appling function over the FCLArray contents."""
        self._ca = FCLArray(*map(f, self), noneIter=self._none)._ca
        
    def map(self, f: Callable[[Any], Any],
            size: int|None=None,
            noneIter: Any=None,
            noneSwap: Any|None=None) -> FCLArray:
        """Apply function f over the FCLArray contents. Return a new FCLArray
        with the mapped contents. Size to the data unless size is given. If
        a default value is not given, use the previous FCLArray's default value
        if defined, otherwise leave undefined.
        """
        if (noneIter, noneSwap) == (None, None):
            noneIter = self._none

        if size is None:
            return FCLArray(*map(f, self), noneIter=noneIter, noneSwap=noneSwap)
        else:
            return FCLArray(*map(f, self), size=size, noneIter=noneIter, noneSwap=noneSwap)
            
    def flatMap(self, f: Callable[[Any], FCLArray],
                size: int|None=None,
                noneIter: Any=None,
                noneSwap: Any|None=None) -> FCLArray:
        """Map f across self and flatten result by concatenating the FCLArray
        elements generated by f. If a default value is not given, use the
        default value of the FLArray being flatMapped if it has been set,
        otherwise leave it unset.

        Note: Any default values of the FLArrays created by f need not have
        anything to do with the default value of the FPArray being flat mapped
        over.
        """
        if (noneIter, noneSwap) == (None, None):
            noneIter = self._none

        return FCLArray(
            *chain(
                *self.map(f)
            ),
            size=size, noneIter=noneIter, noneSwap=noneSwap
        )

    def mergeMap(self, f: Callable[[Any], FCLArray],
                 size: int|None=None,
                 noneIter: Any=None,
                 noneSwap: Any|None=None) -> FCLArray:
        """Map f across self and flatten result by merging the FCLArray elements
        generated by f until the first is exhausted. If a default value is not
        given, use the default value of the FLArray being flatMapped if it has
        been set, otherwise leave it unset.
        """
        if (noneIter, noneSwap) == (None, None):
            noneIter = self._none

        return FCLArray(
            *merge(
                *self.map(f)
            ),
            size=size, noneIter=noneIter, noneSwap=noneSwap
        )

    def exhastMap(self, f: Callable[[Any], FCLArray],
                  size: int|None=None,
                  noneIter: Any=None,
                  noneSwap: Any|None=None) -> FCLArray:
        """Map f across self and flatten result by merging the FCLArray elements
        generated by f until all are exhausted. If a default value is not given,
        use the default value of the FLArray being flatMapped if it has been
        set, otherwise leave it unset.
        """
        if (noneIter, noneSwap) == (None, None):
            noneIter = self._none

        return FCLArray(
            *exhaust(
                *self.map(f)
            ),
            size=size, noneIter=noneIter, noneSwap=noneSwap
        )

if __name__ == "__main__":
    pass
