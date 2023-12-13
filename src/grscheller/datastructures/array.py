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

Module implementing an mutable fixed length data structure with O(1) data
access. All mutating methods are guaranteed not to change the length of the
data structure.

None values are not allowed in this data structures. An immutable default value                     
is set upon instantiating. If no default value is given, the empty tuple () is
used in lieu of None, but is not set as the default value. Method which return
new CLArray values can set a different default value for the new instance.
"""

from __future__ import annotations

__all__ = ['CLArray']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

from typing import Any, Callable, Iterator, Never, Union
from itertools import chain, cycle
from .core.circular_array import CircularArray
from .core.iterlib import merge, exhaust
from .core.fp import FP

class CLArray(FP):
    """Functional Constant Length Array

    Class implementing a mutable fixed length array data structure whose
    mutaing methods are guaranteed not to change the length of the data
    structure.

    - if size set to None, size to all the data provided (even the Nones)
    - if size > 0, pad data on right with default value or slice off trailing data
    - if size < 0, pad data on left with default value or slice off initial data
    - put any non-None sliced off data on the backlog

    Does not permits storing None as a value. If a default value is not set, the
    empty tuple () is used in lieu of None.
    """
    def __init__(self, *initialData,
                 size: int|None=None,
                 backstore: Iterable|None=None,
                 default: Any|None=None):

        match (backstore, default):
            case (None, None):
                self._default = ()
                self._backstore = cycle(((),))
            case (None, default):
                self._default = default
                self._backstore = cycle((default,))
            case (backstore, None):
                self._default = ()
                self._backstore = chain(backstore, cycle(((),)))
            case (backstore, default):
                self._default = default
                self._backstore = chain(backstore, cycle((default,)))

        data = CircularArray()
        backlog = self._backstore

        ds_size = 0
        for d in initialData:
            if d is not None:
                data.pushR(d)

        ds_size = len(data)

        # If size is None, size to max of initial non-None data or 1.
        if size is None:
            abs_size = size = ds_size
            if size:
                abs_size = size = 1
        else:
            if size:
                abs_size = size = 1
            abs_size = abs(size)

        if abs_size > ds_size:
            if size > 0:
                # pad CLArray on "right" (higher indexes)
                for _ in range(size - ds_size):
                    data.pushR(next(backlog))
            else:
                # pad CLArray 0n "left" (lower indexes)
                for _ in range(-size - ds_size):
                    data.pushL(next(backlog))
        elif abs_size < ds_size:
            # Push extra data onto self._backlog iterator, keep original order.
            extra = CircularArray()
            if size > 0:
                # push final data to end
                for _ in range(ds_size - size):
                    extra.pushL(data.popR())
            else:
                # push inital data at beginning
                for _ in range(ds_size + size):
                    extra.pushR(data.popL())
            self._backstore = chain(extra, backlog)

        self._data = data

    def __iter__(self):
        """Iterate over the current state of the CLArray. Copy is made
        so original source can safely mutate.
        """
        for data in self._data.copy():
            yield data

    def __reversed__(self):
        """Reverse iterate over the current state of the CLArray. Copy is made
        so original source can safely mutate.
        """
        for data in reversed(self._data.copy()):
            yield data

    def __repr__(self):
        """Representation of current state of data, does not reproduce the backstore"""
        repr1 = f'{self.__class__.__name__}('
        repr2 = ', '.join(map(repr, self))
        if repr2 == '':
            repr3 = f'size={len(self), }'
        else:
            repr3 = f', size={len(self), }'
        repr4 = f'default={repr(self._default)})'
        return repr1 + repr2 + repr3 + repr4

    def __str__(self):
        return '[[[' + ', '.join(map(repr, self)) + ']]]'

    def __bool__(self):
        """Return true only if there exists an array value not equal to the
        default value which gets used in lieu of None.
        """
        for value in self:
            if value != self._default:
                return True
        return False

    def default(self) -> Any:
        """Return the default value that eventually gets used in lieu of None"""
        return self._default

    def __len__(self) -> int:
        """Returns the size of the CLArray"""
        return len(self._data)

    def __getitem__(self, index: int) -> Union[Any,Never]:
        return self._data[index]

    def __setitem__(self, index: int, value: Any) -> Union[None,Never]:
        if value is None:
            self._data[index] = next(self._backstore)
        else:
            self._data[index] = value

    def __eq__(self, other: Any):
        """Returns True if all the data stored in both compare as equal. Worst
        case is O(n) behavior for the true case. The default value play no role
        in determining equality.
        """
        if not isinstance(other, type(self)):
            return False
        return self._data == other._data

    def reverse(self) -> None:
        """Swap the circular array with one with its elements reversed."""
        self._data = self._data.reverse()

    def mapSelf(self, f: Callable[[Any], Any]) -> None:
        """Mutate the CLArray by appling function over the CLArray contents."""
        self._data = CLArray(*map(f, self),
                            backstore=self._backstore,
                            default=self._default)._data

    def __str__(self):
        return '[|' + ', '.join(map(repr, self)) + '|]'

    def copy(self,
             size: int|None=None,
             noneIter: Iterator|None=None,
             default: Any|None=None) -> CLArray:
        """Return shallow copy of the CLArray in O(n) complexity."""
        return self.map(lambda x: x, size, noneIter, default)

    def map(self, f: Callable[[Any], Any], size: int|None=None,
            backstore: Iterator|None=None, default: Any|None=None) -> CLArray:
        """Apply function f over the CLArray contents. Return a new CLArray with the
        mapped contents. Size to the data unless size is given. If backstore is not
        given, use default to create one. If default is not given, use the value from
        the CLArray being mapped.
        """
        match (backstore, default):
            case (None, None):
                default = self._default
                backstore = cycle((default,))
            case (None, default):
                backstore = cycle((default,))
            case (backstore, None):
                # Careful: noneIter might be infinite!
                default = self._default

        if size is None:
            return CLArray(*map(f, self), backstore=backstore, default=default)
        else:
            return CLArray(*map(f, self), size=size, backstore=backstore, default=default)

    def flatMap(self, f: Callable[[Any], CLArray],
                size: int|None=None,
                backstore: Iterator|None=None,
                default: Any|None=None) -> CLArray:
        """Map f across self and flatten result by concatenating the CLArray elements
        generated by f. If a default value is not given, use the default value of the
        FLArray being flatMapped if it has been set, otherwise leave it unset.

        Any default values of the FLArrays created by f need not have anything to do
        with the default value of the FPArray being flat mapped over.
        """
        if (backstore, default) == (None, None):
            default = self._default

        return CLArray(
            *chain(*self.map(f)), size=size, backstore=backstore, default=default
        )

    def mergeMap(self, f: Callable[[Any], CLArray],
                 size: int|None=None,
                 noneIter: Iterator|None=None,
                 default: Any|None=None) -> CLArray:
        """Map f across self and flatten result by merging the CLArray elements
        generated by f until the first is exhausted. If a default value is not given,
        use the default value of the FLArray being flatMapped if it has been set,
        otherwise leave it unset.
        """
        if (noneIter, default) == (None, None):
            noneIter = self._backstore

        return CLArray(
            *merge(*self.map(f)), size=size, backstore=noneIter, default=default
        )

    def exhastMap(self, f: Callable[[Any], CLArray],
                  size: int|None=None,
                  noneIter: Iterator|None=None,
                  default: Any|None=None) -> CLArray:
        """Map f across self and flatten result by merging the CLArray elements
        generated by f until all are exhausted. If a default value is not given,
        use the default value of the FLArray being flatMapped if it has been set,
        otherwise leave it unset.
        """
        if (noneIter, default) == (None, None):
            noneIter = self._backstore

        return CLArray(
            *exhaust(*self.map(f)), size=size, backstore=noneIter, default=default
        )

if __name__ == "__main__":
    pass
