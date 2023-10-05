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

from typing import Any, Callable
from .carray import Carray
from .functional.maybe import Maybe, Nothing, Some
from .core import concatIters, mapIter

class Dqueue:
    """Double sided queue datastructure. Will resize itself as needed.

    Does not throw exceptions. The Dqueue class consistently uses None to
    represent the absence of a value. Therefore some care needs to be taken
    when Python None is pushed onto Dqueue objects.
    """
    def __init__(self, *data):
        """Construct a double sided queue"""
        self._carray = Carray()
        for datum in data:
            if datum != None:
                self._carray.pushR(datum)

    def __bool__(self) -> bool:
        """Returns true if dqueue is not empty"""
        return len(self._carray) != 0

    def __len__(self) -> int:
        """Returns current number of values in dqueue"""
        return len(self._carray)

    def __getitem__(self, ii: int) -> Any:
        return self._carray[ii]

    def __iter__(self):
        """Iterator yielding data stored in dequeue, does not consume data"""
        if self._carray:
            for pos in range(len(self._carray)):
                yield self._carray[pos]

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
        return Dqueue(*self)

    def pushR(self, *data: Any) -> Dqueue:
        """Push data on rear of dqueue & return reference to self"""
        for datum in data:
            if datum != None:
                self._carray.pushR(datum)
        return self

    def pushL(self, *data: Any) -> Dqueue:
        """Push data on front of dqueue, return the dqueue pushed to"""
        for datum in data:
            if datum != None:
                self._carray.pushL(datum)
        return self

    def popR(self) -> Maybe:
        """Pop data off rear of dqueue"""
        if len(self._carray) > 0:
            return Some(self._carray.popR())
        else:
            return Nothing

    def popL(self) -> Maybe:
        """Pop data off front of dqueue"""
        if len(self._carray) > 0:
            return Some(self._carray.popL())
        else:
            return Nothing

    def headR(self) -> Maybe:
        """Return rear element of dqueue without consuming it"""
        if len(self._carray) > 0:
            return Some(self._carray[-1])
        else:
            return Nothing

    def headL(self) -> Maybe:
        """Return front element of dqueue without consuming it"""
        if len(self._carray) > 0:
            return Some(self._carray[0])
        else:
            return Nothing

    def capacity(self) -> int:
        """Returns current capacity of dqueue"""
        return self._carray.capacity()

    def fractionFilled(self) -> float:
        """Returns current capacity of dqueue"""
        return self._carray.fractionFilled()

    def resize(self, addCapacity = 0):
        """Compact dqueue and add extra capacity"""
        return self._carray.resize(addCapacity)

    def map(self, f: Callable[[Any], Any]) -> Dqueue:
        """Apply function over dqueue contents, returns new instance"""
        return Dqueue(*mapIter(iter(self), f))

    def flatMap(self, f: Callable[[Any], Dqueue]) -> Dqueue:
        """Apply function and flatten result, returns new instance"""
        return Dqueue(
            *concatIters(
                *mapIter(mapIter(iter(self), f), lambda x: iter(x))
            )
        )

if __name__ == "__main__":
    pass
