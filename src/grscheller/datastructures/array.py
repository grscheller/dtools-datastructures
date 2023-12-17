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

from typing import Any, Callable, Iterable, Iterator, Union
from itertools import chain, cycle, repeat
from .circular_array import CircularArray
from .queue import DoubleQueue
from .core.iterlib import merge, exhaust
from .core.fp import FP, Some

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
    def __init__(self, *data, size: int|None=None, default: Any|None=None):

        if default is None:
            default = ()

        arrayQueue = DoubleQueue()
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
                    arrayQueue.pushR(backQueue.popL())
                arrayQueue.pushR(*(repeat(default, abs_size - data_size)))
            else:
                # slice initial data on right
                for _ in range(abs_size):
                    arrayQueue.pushR(backQueue.popL())
        else:
            if data_size < abs_size:
                # pad CLArray on left with default value
                while backQueue:
                    arrayQueue.pushL(backQueue.popR())
                arrayQueue.pushL(*(repeat(default, abs_size - data_size)))
            else:
                # slice initial data on left
                for _ in range(abs_size):
                    arrayQueue.pushL(backQueue.popR())
                backQueue = DoubleQueue(*reversed(backQueue))

        self._arrayQueue = arrayQueue
        self._backQueue = backQueue
        self._default = default

    def __iter__(self):
        """Iterate over the current state of the CLArray. Copy is made
        so original source can safely mutate.
        """
        for data in self._arrayQueue.copy():
            yield data

    def __reversed__(self):
        """Reverse iterate over the current state of the CLArray. Copy is made
        so original source can safely mutate.
        """
        for data in reversed(self._arrayQueue.copy()):
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
        return '[|' + ', '.join(map(repr, self)) + '|]'

    def __bool__(self):
        """Return true only if there exists an array value not equal to the
        default value which gets used in lieu of None.
        """
        for value in self:
            if value != self._default:
                return True
        return False

    def default(self) -> Any:
        """Return a reference to the default value that gets used in lieu of None"""
        return self._default

    def backQueue(self) -> DoubleQueue:
        """Return a copy of the backQueue"""
        return self._backQueue.copy()

    def __len__(self) -> int:
        """Returns the size of the CLArray"""
        return len(self._arrayQueue)

    def __getitem__(self, index: int) -> Any:
        return self._arrayQueue[index]

    def __setitem__(self, index: int, value: Any) -> Any:
        if value is None:
            self._arrayQueue[index] = Some(self._backQueue.popL()).get(self._default)
        else:
            self._arrayQueue[index] = value

    def __eq__(self, other: Any):
        """Returns True if all the data stored in both compare as equal. Worst case is
        O(n) behavior for the true case. The default value and the backQueue plays no
        role in determining equality.
        """
        if not isinstance(other, type(self)):
            return False
        return self._arrayQueue == other._arrayQueue

    def copy(self, size: int|None=None, default: Any|None=None) -> CLArray:
        """Return shallow copy of the CLArray in O(n) complexity."""
        return self.map(lambda x: x, size, default)

    def map(self, f: Callable[[Any], Any],
            size: int|None=None,
            default: Any|None=None) -> CLArray:
        """Apply function f over the CLArray contents. Return a new CLArray with the
        mapped contents. Size to the data unless size is given. If default is not given,
        use the value from the CLArray being mapped.

        Recommendation: default should be of the same type that f produces
        """
        if default is None:
            default = self._default

        def F(ff: Callable([Any], Any)) -> Callable([Any], Any):
            def FF(x: Any) -> Any:
                value = ff(x)
                if value is None:
                    return default
                else:
                    return value
            return FF

        if size is None:
            return CLArray(*map(F(f), self), default=default)
        else:
            return CLArray(*map(F(f), self), size=size, default=default)

    def flatMap(self,
                f: Callable[[Any], CLArray],
                size: int|None=None,
                default: Any|None=None,
                mapDefault: bool=False) -> CLArray:
        """Map f across self and flatten result by concatenating the CLArray elements
        generated by f. If a default value is not given, use the default value of the
        FLArray being flatMapped.

        Any default values of the FLArrays created by f need not have anything to do
        with the default value of the FPArray being flatmapped over.
        """
        if default is None:
            default = self.default()
        if mapDefault:
            default = f(default).default()

        return CLArray(*chain(*self.map(f)), size=size, default=default)

    def mergeMap(self, f: Callable[[Any], CLArray],
                 size: int|None=None,
                 default: Any|None=None,
                 mapDefault: bool=False) -> CLArray:
        """Map f across self and flatten result by merging the CLArray elements
        generated by f until the first is exhausted. If a default value is not given,
        use the default value of the FLArray being flatmapped.
        """
        if default is None:
            default = self._default
        if mapDefault:
            default = f(default).default()

        return CLArray(*merge(*self.map(f)), size=size, default=default)

    def exhastMap(self, f: Callable[[Any], CLArray],
                  size: int|None=None,
                  default: Any|None=None,
                  mapDefault: bool=False) -> CLArray:
        """Map f across self and flatten result by merging the CLArray elements
        generated by f until all are exhausted. If a default value is not given,
        use the default value of the FLArray being flatmapped.
        """
        if default is None:
            default = self._default
        if mapDefault:
            default = f(default).default()

        return CLArray(*exhaust(*self.map(f)), size=size, default=default)

    def reverse(self) -> None:
        """Swap the arrayQueue with one with its elements reversed."""
        self._arrayQueue = DoubleQueue(*reversed(self))

if __name__ == "__main__":
    pass
