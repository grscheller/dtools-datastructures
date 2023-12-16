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

from typing import Any, Callable, Iterable, Iterator, Never, Union
from itertools import chain, cycle, repeat
from .queue import DoubleQueue
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
    __slots__ = ['_ca', '_backQueue' '_default']

    def __init__(self, *data, size: int|None=None, default: Any|None=None):

        ca = CircularArray()
        if default is None:
            default = ()

        backQueue = DoubleQueue(*data)
        data_size = len(backQueue)

        if size is None:
            abs_size = size = data_size
        else:
            abs_size = abs(size)

        if size >= 0:
            if data_size < abs_size:
                # pad CLArray on right with default value
                while backQueue:
                    ca.pushR(backQueue.popL())
                ca.pushR(*(repeat(default, abs_size - data_size)))
            else:
                # slice initial data on right
                for _ in range(abs_size):
                    ca.pushR(backQueue.popL())
        else:
            if data_size < abs_size:
                # pad CLArray on left with default value
                while backQueue:
                    ca.pushL(backQueue.popR())
                ca.pushL(*(repeat(default, abs_size - data_size)))
            else:
                # slice initial data on left
                for _ in range(abs_size):
                    ca.pushL(backQueue.popR())

        self._ca = ca
        self._backQueue = backQueue
        self._default = default

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
        """Representation of current state of data, does not reproduce the backstore"""
        repr1 = f'{self.__class__.__name__}('
        repr2 = ', '.join(map(repr, self))
        if repr2 == '':
            repr3 = f'size={len(self)}, '
        else:
            repr3 = f', size={len(self)}, '
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

    def backstore(self) -> Iterator:
        """Return the backstore iterator"""
        return self._backstore

    def __len__(self) -> int:
        """Returns the size of the CLArray"""
        return len(self._ca)

    def __getitem__(self, index: int) -> Union[Any,Never]:
        return self._ca[index]

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
        return self._ca == other._ca

    def reverse(self) -> None:
        """Swap the circular array with one with its elements reversed."""
        self._ca = self._ca.reverse()

    def mapSelf(self, f: Callable[[Any], Any]) -> None:
        """Mutate the CLArray by appling function over the CLArray contents."""
        self._ca = CLArray(*map(f, self),
                            backData=self._backstore,
                            default=self._default)._data

    def __str__(self):
        return '[|' + ', '.join(map(repr, self)) + '|]'

    def copy(self,
             size: int|None=None,
             backstore: Iterable|None=None,
             default: Any|None=None) -> CLArray:
        """Return shallow copy of the CLArray in O(n) complexity."""
        return self.map(lambda x: x, size, backstore, default)

    def map(self, f: Callable[[Any], Any], size: int|None=None,
            backstore: Iterale|None=None, default: Any|None=None) -> CLArray:
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
                default = self._default

        if size is None:
            return CLArray(*map(f, self), backData=backstore, default=default)
        else:
            return CLArray(*map(f, self), size=size, backData=backstore, default=default)

    def flatMap(self, f: Callable[[Any], CLArray],
                size: int|None=None,
                backstore: Iterator|None=None,
                default: Any|None=None) -> CLArray:
        """Map f across self and flatten result by concatenating the CLArray elements
        generated by f. If a default value is not given, use the default value of the
        FLArray being flatMapped.

        Any default values of the FLArrays created by f need not have anything to do
        with the default value of the FPArray being flatmapped over.
        """
        if (default, backstore) == (None, None):
            default = self._default

        return CLArray(*chain(*self.map(f)), size, backstore, default)

    def mergeMap(self, f: Callable[[Any], CLArray],
                 size: int|None=None,
                 backstore: Iterale|None=None,
                 default: Any|None=None) -> CLArray:
        """Map f across self and flatten result by merging the CLArray elements
        generated by f until the first is exhausted. If a default value is not given,
        use the default value of the FLArray being flatmapped.
        """
        if (default, backstore) == (None, None):
            default = self._default

        return CLArray(*merge(*self.map(f)), size, backstore, default)

    def exhastMap(self, f: Callable[[Any], CLArray],
                  size: int|None=None,
                  backstore: Iterable|None=None,
                  default: Any|None=None) -> CLArray:
        """Map f across self and flatten result by merging the CLArray elements
        generated by f until all are exhausted. If a default value is not given,
        use the default value of the FLArray being flatmapped.
        """
        if (default, backstore) == (None, None):
            default = self._default

        return CLArray(*exhaust(*self.map(f)), size, backstore, default)

if __name__ == "__main__":
    pass
