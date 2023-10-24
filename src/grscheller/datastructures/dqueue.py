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

"""Module grscheller.datastructure.dqueue - Double sided queue

Double sided queue with amortized O(1) insertions & deletions from either end.
Obtaining length (number of elements) of a Dqueue is also a O(1) operation.

Implemented with a Python List based circular array.
"""

from __future__ import annotations

__all__ = ['Dqueue']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

from typing import Any, Callable, Self, Union
from .carray import CArray
from .iterlib import concatIters, mapIter, mergeIters

class Dqueue():
    """Double sided queue datastructure. Will resize itself as needed.

    Does not throw exceptions. The Dqueue class consistently uses None to
    represent the absence of a value. None will not be pushed to this
    data structure. As an alternative, use Maybe objects of type Nothing,
    or the empty tuple () to represent a non-existent value. 
    """
    def __init__(self, *ds):
        """Construct a double sided queue"""
        self._carray = CArray()
        for d in ds:
            if d is not None:
                self._carray.pushR(d)

    def __bool__(self) -> bool:
        """Returns true if dqueue is not empty"""
        return len(self._carray) != 0

    def __len__(self) -> int:
        """Returns current number of values in dqueue"""
        return len(self._carray)

    def __iter__(self):
        """Iterator yielding data currently stored in dqueue"""
        currCarray = self._carray.copy()
        for pos in range(len(currCarray)):
            yield currCarray[pos]

    def __reversed__(self):
        """Reverse iterate over the current state of the dqueue"""
        for data in reversed(self._carray.copy()):
            yield data

    def __eq__(self, other):
        """Returns True if all the data stored in both compare as equal.
        Worst case is O(n) behavior for the true case.
        """
        if not isinstance(other, type(self)):
            return False
        return self._carray == other._carray

    def __repr__(self):
        """Display data in dqueue"""
        dataListStrs = []
        for data in self._carray:
            dataListStrs.append(repr(data))
        return ">< " + " | ".join(dataListStrs) + " ><"

    def copy(self) -> Dqueue:
        """Return shallow copy of the dqueue in O(n) time & space complexity"""
        new_dqueue = Dqueue()
        new_dqueue._carray = self._carray.copy()
        return new_dqueue

    def pushR(self, *ds: Any) -> Dqueue:
        """Push data on rear of dqueue & return reference to self"""
        for d in ds:
            if d != None:
                self._carray.pushR(d)
        return self

    def pushL(self, *ds: Any) -> Dqueue:
        """Push data on front of dqueue, return reference to self"""
        for d in ds:
            if d != None:
                self._carray.pushL(d)
        return self

    def popR(self) -> Union[Any, None]:
        """Pop data off rear of dqueue"""
        if len(self._carray) > 0:
            return self._carray.popR()
        else:
            return None

    def popL(self) -> Union[Any, None]:
        """Pop data off front of dqueue"""
        if len(self._carray) > 0:
            return self._carray.popL()
        else:
            return None

    def peakR(self) -> Union[Any, None]:
        """Return rear element of dqueue without consuming it"""
        if len(self._carray) > 0:
            return self._carray[-1]
        else:
            return None

    def peakL(self) -> Union[Any, None]:
        """Return front element of dqueue without consuming it"""
        if len(self._carray) > 0:
            return self._carray[0]
        else:
            return None

    def capacity(self) -> int:
        """Returns current capacity of dqueue"""
        return self._carray.capacity()

    def fractionFilled(self) -> float:
        """Returns current capacity of dqueue"""
        return self._carray.fractionFilled()

    def resize(self, addCapacity = 0) -> Self:
        """Compact dqueue and add extra capacity"""
        self._carray.resize(addCapacity)
        return self

    def map(self, f: Callable[[Any], Any]) -> Self:
        """Apply function over dqueue contents"""
        self._carray = Dqueue(*mapIter(iter(self), f))._carray
        return self

    def flatMap(self, f: Callable[[Any], Dqueue]) -> Self:
        """Apply function and flatten result, surpress any None values"""
        self._carray = Dqueue(*concatIters(
            *mapIter(mapIter(iter(self), f), lambda x: iter(x))))._carray
        return self

    def mergeMap(self, f: Callable[[Any], Dqueue]) -> Self:
        """Apply function and flatten result, surpress any None values"""
        self._carray = Dqueue(*mergeIters(
            *mapIter(mapIter(iter(self), f), lambda x: iter(x))))._carray
        return self

if __name__ == "__main__":
    pass
