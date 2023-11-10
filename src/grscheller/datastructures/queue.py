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

"""Module grscheller.datastructure.queue - queue based datastructures

Module implementing stateful FIFO data structures with amortized O(1) pushing
& popping from the queue. Obtaining length (number of elements) of a queue is
also a O(1) operation. Implemented with a Python List based circular array.
Does not store None as a value.

Classes:
  grscheller.datastructure.SQueue - Single sided FIFO queue
  grscheller.datastructure.DQueue - Double sided FIFO/LIFO queue
"""

from __future__ import annotations

__all__ = ['SQueue', 'DQueue']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

from typing import Any, Callable
from itertools import chain
from .core.iterlib import merge, exhaust
from .core.carray import CArray

class Queue():
    """Abstract base class for the purposes of DRY inheritance of classes
    implementing queue type data structures with a list based circular array.
    Each queue object "has-a" (contains) a circular array to store its data. The
    circular array used will resize itself as needed. Each Queue subclass must
    ensure that None values do not get pushed onto the circular array.
    """
    def __init__(self, *ds):
        """Construct a queue data structure. Cull None values."""
        self._carray = CArray()
        for d in ds:
            if d is not None:
                self._carray.pushR(d)

    def __bool__(self):
        """Returns true if queue is not empty."""
        return len(self._carray) > 0

    def __len__(self):
        """Returns current number of values in queue."""
        return len(self._carray)

    def __iter__(self):
        """Iterator yielding data currently stored in queue. Data yielded in
        natural FIFO order.
        """
        cached = self._carray.copy()
        for pos in range(len(cached)):
            yield cached[pos]

    def __reversed__(self):
        """Reverse iterate over the current state of the queue."""
        for data in reversed(self._carray.copy()):
            yield data

    def __eq__(self, other):
        """Returns True if all the data stored in both compare as equal.
        Worst case is O(n) behavior for the true case.
        """
        if not isinstance(other, type(self)):
            return False
        return self._carray == other._carray

    def copy(self) -> Queue:
        raise NotImplementedError


class SQueue(Queue):
    """Single sided queue datastructure. Will resize itself as needed.
    None represents the absence of a value and ignored if pushed onto an SQueue.
    """
    def __init__(self, *ds):
        """Construct a FIFO SQueue data structure."""
        super().__init__(*ds)

    def __repr__(self):
        """Display the SQueue showing the contained data."""
        return "<< " + " < ".join(map(repr, self)) + " <<"

    def push(self, *ds: Any) -> None:
        """Push data on rear of the SQueue & no return value."""
        for d in ds:
            if d != None:
                self._carray.pushR(d)

    def copy(self) -> SQueue:
        """Return shallow copy of the SQueue in O(n) time & space complexity."""
        squeue = SQueue()
        squeue._carray = self._carray.copy()
        return squeue

    def pop(self) -> Any:
        """Pop data off front of the SQueue."""
        if len(self._carray) > 0:
            return self._carray.popL()
        else:
            return None

    def peakLastIn(self) -> Any:
        """Return last element pushed to the SQueue without consuming it"""
        if len(self._carray) > 0:
            return self._carray[-1]
        else:
            return None

    def peakNextOut(self) -> Any:
        """Return next element ready to pop from the SQueue."""
        if len(self._carray) > 0:
            return self._carray[0]
        else:
            return None

    def map(self, f: Callable[[Any], Any]) -> None:
        """Apply function over the SQueue's contents. Suppress any None values
        returned by f.
        """
        self._carray = SQueue(*map(f, self))._carray

    def flatMap(self, f: Callable[[Any], SQueue]) -> None:
        """Apply function over the SQueue's contents and flatten result merging
        the SQueues produced sequentially front-to-back.
        """
        self._carray = SQueue(*chain(*map(iter, map(f, self))))._carray

    def mergeMap(self, f: Callable[[Any], SQueue]) -> None:
        """Apply function over the SQueue's contents and flatten result by round
        robin merging until one of the first SQueues produced by f is exhausted.
        """
        self._carray = SQueue(*merge(*map(iter, map(f, self))))._carray

    def exhaustMap(self, f: Callable[[Any], SQueue]) -> None:
        """Apply function over the SQueue's contents and flatten result by round
        robin merging until all the SQueues produced by f are exhausted.
        """
        self._carray = SQueue(*exhaust(*map(iter, map(f, self))))._carray


class DQueue(Queue):
    """Double sided queue datastructure. Will resize itself as needed.
    None represents the absence of a value and ignored if pushed onto a DQueue.
    """
    def __init__(self, *ds):
        """Construct a FIFO/LIFO double sided queue data structure."""
        super().__init__(*ds)

    def __repr__(self):
        """Display the DQueue showing the data contained."""
        return ">< " + " | ".join(map(repr, self)) + " ><"

    def copy(self) -> DQueue:
        """Return shallow copy of the DQueue in O(n) time & space complexity."""
        dqueue = DQueue()
        dqueue._carray = self._carray.copy()
        return dqueue

    def pushR(self, *ds: Any) -> None:
        """Push data left to right onto rear of the DQueue."""
        for d in ds:
            if d != None:
                self._carray.pushR(d)

    def pushL(self, *ds: Any) -> None:
        """Push data left to right onto front of DQueue."""
        for d in ds:
            if d != None:
                self._carray.pushL(d)

    def popR(self) -> Any:
        """Pop data off rear of the DQueue"""
        if len(self._carray) > 0:
            return self._carray.popR()
        else:
            return None

    def popL(self) -> Any:
        """Pop data off front of the DQueue"""
        if len(self._carray) > 0:
            return self._carray.popL()
        else:
            return None

    def peakR(self) -> Any:
        """Return right-most element of the DQueue if it exists."""
        if len(self._carray) > 0:
            return self._carray[-1]
        else:
            return None

    def peakL(self) -> Any:
        """Return left-most element of the DQueue if it exists."""
        if len(self._carray) > 0:
            return self._carray[0]
        else:
            return None

    def map(self, f: Callable[[Any], Any]) -> None:
        """Apply function over the DQueue's contents. Suppress any None values
        returned by f.
        """
        self._carray = DQueue(*map(f, self))._carray

    def flatMap(self, f: Callable[[Any], DQueue]) -> None:
        """Apply function over the DQueue's contents and flatten result merging
        the DQueues produced sequentially front-to-back.
        """
        self._carray = DQueue(*chain(*map(iter, map(f, self))))._carray

    def mergeMap(self, f: Callable[[Any], DQueue]) -> None:
        """Apply function over the DQueue's contents and flatten result by round
        robin merging until one of the first DQueues produced by f is exhausted.
        """
        self._carray = DQueue(*merge(*map(iter, map(f, self))))._carray

    def exhaustMap(self, f: Callable[[Any], DQueue]) -> None:
        """Apply function over the DQueue's contents and flatten result by round
        robin merging until all the DQueues produced by f are exhausted.
        """
        self._carray = DQueue(*exhaust(*map(iter, map(f, self))))._carray


if __name__ == "__main__":
    pass
