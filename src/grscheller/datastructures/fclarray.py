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

Note: None values are not allowed in this data structures. Due to the
      fixed length size guarantees provided by the FCLArray class, a "default"
      value is needed if a None is attemped to be stored. If no default value
      is given, the empty tuple () is used. Once set, the default value is
      immutable. A copy method is provided to create a new FCLArray with
      a different default value.
"""

from __future__ import annotations

__all__ = ['FCLArray']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

from typing import Any, Callable, Never, Union
from .core.fp import FP

class FCLArray(FP):
    """Functional Constant Length Array

    Class implementing an mutable fixed length array data structure whose
    mutaing methods are guaranteed not to change the length of the data
    structure.

    If size set to None, size to data provided.
    If size > 0, pad data on right with default value or slice off trailing data.
    If size < 0, pad data on left with default value or slice off initial data.

    Does not permits storing None as a value. If a default value is not given,
    the empty tuple () is used. A better choice would be to generate an
    "unhappy path" monadic "subtype" with Nothing or Right().
    """
    def __init__(self, *ds, size: int|None=None, default: Any=None):
        """Construct a fixed length array, None values not allowed."""
        if default is None:
            self._default = ()
        else:
            self._default = default

        dlist = []
        for d in ds:
            if d is not None:
                dlist.append(d)
            else:
                dlist.append(self._default)
        dsize = len(dlist)

        if size is None:
            abs_size = size = dsize
        else:
            abs_size = abs(size)

        if abs_size == dsize:
            # no size inconsistencies
            self._size = dsize
            self._list = dlist
        elif abs_size > dsize:
            if size > 0:
                # pad higher indexes (on "right")
                self._size = size
                self._list = dlist + [self._default]*(size - dsize)
            else:
                # pad lower indexes (on "left")
                dlist.reverse()
                dlist += [self._default]*(-size - dsize)
                dlist.reverse()
                self._size = -size
                self._list = dlist + [self._default]*(size - dsize)
        else:
            if size > 0:
                # take left slice, ignore extra data at end
                self._size = size
                self._list = dlist[0:size]
            else:
                # take right slice, ignore extra data at beginning
                self._size = -size
                self._list = dlist[dsize+size:]

    def __iter__(self):
        """Iterate over the current state of the FCLArray. Copy is made
        so original source can safely mutate.
        """
        for data in self._list.copy():
            yield data

    def __reversed__(self):
        """Reverse iterate over the current state of the FCLArray. Copy is made
        so original source can safely mutate.
        """
        for data in reversed(self._list.copy()):
            yield data

    def __repr__(self):
        repr1 = f'{self.__class__.__name__}('
        repr2 = ', '.join(map(repr, self))
        if repr2 == '':
            repr3 = f'default={self._default})'
        else:
            repr3 = f', default={self._default})'
        return repr1 + repr2 + repr3

    def __str__(self):
        return '[|' + ', '.join(map(repr, self)) + '|]'

    def __bool__(self):
        """Return true only only if there existsan array
        value ot equal to the default value.
        """
        default = self._default
        for value in self:
            if value != default:
                return True
        return False

    def __len__(self) -> int:
        """Returns the size of the FCLArray"""
        return self._size

    def __getitem__(self, index: int) -> Union[Any,Never]:
        size = self._size
        if size == 0:
            msg = 'Attempt to index an empty FCLArray'
            raise IndexError(msg)

        if not -size <= index < size:
            l = -size
            h = size - 1
            msg = f'FCLArray index = {index} not between {l} and {h}'
            msg += ' while getting value'
            raise IndexError(msg)

        return self._list[index]

    def __setitem__(self, index: int, value: Any) -> Union[None,Never]:
        size = self._size
        if size == 0:
            msg = 'Attempt to index an empty FCLArray'
            raise IndexError(msg)

        if not -size <= index < size:
            l = -size
            h = size - 1
            msg = f'FCLArray index = {index} not between {l} and {h}'
            msg += ' while setting value'
            raise IndexError(msg)
        
        if value is not None:
            self._list[index] = value
        else:
            self._list[index] = self._default

    def __eq__(self, other: Any):
        """Returns True if all the data stored in both compare as equal. Worst
        case is O(n) behavior for the true case. The default value play no role
        in determining equality.
        """
        if not isinstance(other, type(self)):
            return False
        return self._list == other._list

    def __add__(self, other: Any) -> FCLArray:
        """Concatenate components and return new FCLArray with default value set
        to that of the LHS FCLArray"""
        if not isinstance(other, type(self)):
            msg = 'Type mismatch: FCLArrays concatenate only with other FCLArrays'
            raise ValueError(msg)
        return FCLArray(*self, *other, default=self._default)

    def copy(self, size: int|None=None, default: Any=None) -> FCLArray:
        """Return shallow copy of the FCLArray in O(n) time & space complexity.
        Optionally change the FCLArray's default value. Does not affect any
        contained values of the previous default value.
        """
        return self.map(lambda x: x, size=size, default=default)

    def default(self) -> Any:
        """Return the default value used to swap with None."""
        return self._default

    def reverse(self) -> None:
        """Reverse the elements of the FCLArray. Mutates the FCLArray."""
        self._list.reverse()

    def map(self, f: Callable[[Any], Any], size: int|None=None, default: Any=None) -> FCLArray:
        """Apply function f over the FCLArray contents. Return a new FCLArray
        with the mapped contents. Size to the data unless size is given. Use
        self._default if f returns None and a default is not given.
        """
        if default is None:
            default = self._default
        return FCLArray(*map(f, self), size=size, default=default)

    def mapSelf(self, f: Callable[[Any], Any]) -> None:
        """Mutate the CLArray by appling function over the CLArray contents."""
        self._list = FCLArray(*map(f, self), default=self._default)._list

if __name__ == "__main__":
    pass
