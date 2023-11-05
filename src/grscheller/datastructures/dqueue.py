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
Obtaining length (number of elements) of a DQueue is also a O(1) operation.

Implemented with a Python List based circular array.
"""

from __future__ import annotations

__all__ = ['DQueue']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

from typing import Any, Callable, Self
from itertools import chain
from .core.iterlib import merge, exhaust
from .core.carray import CArray

class DQueue():
    """Double sided queue datastructure. Will resize itself as needed.

    The DQueue class consistently uses None to represent the absence of a value.
    None will not be pushed to this data structure. As an alternative, use Maybe
    objects of type Nothing, or the empty tuple () to represent a non-existent
    value. 
    """
    def __init__(self, *ds):
        """Construct a double sided queue data structure.

        Null values will be culled from the intial data from ds.
        """
        self._carray = CArray()
        for d in ds:
            if d is not None:
                self._carray.pushR(d)

    def __bool__(self) -> bool:
        """Returns true if dqueue is not empty."""
        return len(self._carray) != 0

    def __len__(self) -> int:
        """Returns current number of values in dqueue."""
        return len(self._carray)

    def __iter__(self):
        """Iterator yielding data currently stored in dqueue.

        Data yielded in left-to-right order.
        """
        currCarray = self._carray.copy()
        for pos in range(len(currCarray)):
            yield currCarray[pos]

    def __reversed__(self):
        """Reverse iterate over the current state of the dqueue.
        
        Data yielded in right-to-left order.
        """
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
        """Display data in dqueue."""
        return ">< " + " | ".join(self.map(lambda x: repr(x))) + " ><"

    def copy(self) -> DQueue:
        """Return shallow copy of the dqueue in O(n) time & space complexity."""
        new_dqueue = DQueue()
        new_dqueue._carray = self._carray.copy()
        return new_dqueue

    def pushR(self, *ds: Any) -> None:
        """Push data left to right onto rear of dqueue."""
        for d in ds:
            if d != None:
                self._carray.pushR(d)

    def pushL(self, *ds: Any) -> None:
        """Push data left to right onto front of dqueue."""
        for d in ds:
            if d != None:
                self._carray.pushL(d)

    def popR(self) -> Any|None:
        """Pop data off rear of dqueue"""
        if len(self._carray) > 0:
            return self._carray.popR()
        else:
            return None

    def popL(self) -> Any|None:
        """Pop data off front of dqueue"""
        if len(self._carray) > 0:
            return self._carray.popL()
        else:
            return None

    def peakR(self) -> Any|None:
        """Return right-most element of dqueue if it exists."""
        if len(self._carray) > 0:
            return self._carray[-1]
        else:
            return None

    def peakL(self) -> Any|None:
        """Return left-most element of dqueue if it exists."""
        if len(self._carray) > 0:
            return self._carray[0]
        else:
            return None

    def map(self, f: Callable[[Any], Any], mut: bool=False) -> None|DQueue:
        """Apply function over DQueue contents. If mut=True (the default) mutate
        the DQueue & don't return anything. Othersise, return a new DQueue
        leaving the original unchanged. Suppress any None Values returned by f.
        """
        dqueue  = DQueue(*map(f, iter(self)))
        if mut:
            self._carray = dqueue._carray
            return None
        return dqueue

    def flatMap(self, f: Callable[[Any], DQueue], mut: bool=False) -> None|DQueue:
        """Apply function over the DQueue's contents and flatten result merging
        the DQueues produced sequentially front-to-back. If mut=True (default)
        mutate the DQueue & don't return anything. Othersise, return a new
        DQueue leaving the original unchanged. Suppress any None Values
        contained in any of the DQueues returned by f.
        """
        dqueue = DQueue(*chain(
            *map(lambda x: iter(x), map(f, iter(self)))
        ))
        if mut:
            self._carray = dqueue._carray
            return None
        return dqueue

    def mergeMap(self, f: Callable[[Any], DQueue], mut: bool=False) -> None|DQueue:
        """Apply function over the DQueue's contents and flatten result by round
        robin merging until one of the first DQueues produced by f is exhausted.
        If mut=True (default) mutate the DQueue & don't return anything.
        Othersise, return a new DQueue leaving the original unchanged. Suppress
        any None Values contained in any of the DQueues returned by f.
        """
        dqueue = DQueue(*merge(
            *map(lambda x: iter(x), map(f, iter(self)))
        ))
        if mut:
            self._carray = dqueue._carray
            return None
        return dqueue

    def exhaustMap(self, f: Callable[[Any], DQueue], mut: bool=False) -> None|DQueue:
        """Apply function over the DQueue's contents and flatten result by round
        robin merging until all the DQueues produced by f are exhausted. If
        mut=True (default) mutate the DQueue & don't return anything. Othersise,
        return a new DQueue leaving the original unchanged. Suppress any None
        Values contained in any of the DQueues returned by f.
        """
        dqueue = DQueue(*exhaust(
            *map(lambda x: iter(x), map(f, iter(self)))
        ))
        dqueue = DQueue(*exhaust(*(iter(x) for x in map(f, iter(self)))))
        if mut:
            self._carray = dqueue._carray
            return None
        return dqueue

if __name__ == "__main__":
    pass
