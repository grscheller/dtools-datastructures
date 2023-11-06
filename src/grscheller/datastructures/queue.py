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
  grscheller.datastructure.queue  - Single sided FIFO queue
  grscheller.datastructure.dqueue - Double sided FIFO/LIFO queue
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
    circular array used will resize itself as needed. Each Queue subclass most
    ensure that None values do not get pushed onto the circular array.
    """
    def __init__(self, *ds):
        """Construct a queue data structure.

        Null values will be culled from the intial data from ds.
        """
        self._carray = CArray()
        for d in ds:
            if d is not None:
                self._carray.pushR(d)

    def __bool__(self) -> bool:
        """Returns true if queue is not empty."""
        return len(self._carray) > 0

    def __len__(self) -> int:
        """Returns current number of values in queue."""
        return len(self._carray)

    def __iter__(self):
        """Iterator yielding data currently stored in queue. Data yielded in
        natural FIFO order.
        """
        currCarray = self._carray.copy()
        for pos in range(len(currCarray)):
            yield currCarray[pos]

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

    def copy(self) -> Any:
        """Return shallow copy of the queue in O(n) time & space complexity."""
        # Since types are objects, why can't Python match on Types???
        match repr(type(self)):
            case "<class 'grscheller.datastructures.queue.SQueue'>":
                queue = SQueue()
            case "<class 'grscheller.datastructures.queue.DQueue'>":
                queue = DQueue()
            case _:
                msg = f'{repr(type(self))} is not a supported class '
                msg += 'derived from the Stack base class.'
                raise NotImplementedError(msg)
        queue._carray = self._carray.copy()
        return queue


class SQueue(Queue):
    """Single sided queue datastructure.

    Will resize itself as needed.

    None represents the absence of a value and are ignored if pushed on the
    queue. Use another object, like an empty tuple (), as a sentinal values.
    """
    def __init__(self, *ds):
        """Construct a FIFO queue data structure."""
        super().__init__(*ds)

    def __repr__(self):
        """Display data in queue."""
        return "<< " + " < ".join(map(lambda x: repr(x), iter(self))) + " <<"

    def copy(self):
        squeue = SQueue()
        squeue._carray = self._carray.copy()
        return squeue

    def push(self, *ds: Any) -> None:
        """Push data on rear of queue & no return value."""
        for d in ds:
            if d != None:
                self._carray.pushR(d)

    def pop(self) -> Any|None:
        """Pop data off front of queue."""
        if len(self._carray) > 0:
            return self._carray.popL()
        else:
            return None

    def peakLastIn(self) -> Any|None:
        """Return last element pushed to queue without consuming it."""
        if len(self._carray) > 0:
            return self._carray[-1]
        else:
            return None

    def peakNextOut(self) -> Any|None:
        """Return next element ready to pop from queue without consuming it."""
        if len(self._carray) > 0:
            return self._carray[0]
        else:
            return None

    def map(self, f: Callable[[Any], Any], mut: bool=True) -> SQueue|None:
        """Apply function over Queue contents. If mut=True (the default) mutate
        the Queue & don't return anything. Othersise, return a new Queue leaving
        the original unchanged. Suppress any None Values returned by f.
        """
        queue  = SQueue(*map(f, iter(self)))
        if mut:
            self._carray = queue._carray
            return None
        return queue

    def flatMap(self, f: Callable[[Any], SQueue], mut: bool=True) -> SQueue|None:
        """Apply function over the queue's contents and flatten result merging
        the queues produced sequentially front-to-back. If mut=True (default)
        mutate the Queue & don't return anything. Othersise, return a new Queue
        leaving the original unchanged. Suppress any None Values contained in
        any of the Queues returned by f.
        """
        queue = SQueue(*chain(
            *map(lambda x: iter(x), map(f, iter(self)))
        ))
        if mut:
            self._carray = queue._carray
            return None
        return queue

    def mergeMap(self, f: Callable[[Any], SQueue], mut: bool=True) -> SQueue|None:
        """Apply function over the Queue's contents and flatten result by round
        robin merging until one of the first Queues produced by f is exhausted.
        If mut=True (default) mutate the Queue & don't return anything.
        Othersise, return a new Queue leaving the original unchanged. Suppress
        any None Values contained in any of the Queues returned by f.
        """
        queue = SQueue(*merge(
            *map(lambda x: iter(x), map(f, iter(self)))
        ))
        if mut:
            self._carray = queue._carray
            return None
        return queue

    def exhaustMap(self, f: Callable[[Any], SQueue], mut: bool=True) -> SQueue|None:
        """Apply function over the Queue's contents and flatten result by round
        robin merging until all the Queues produced by f are exhausted. If
        mut=True (default) mutate the Queue & don't return anything. Othersise,
        return a new Queue leaving the original unchanged. Suppress any None
        Values contained in any of the Queues returned by f.
        """
        queue = SQueue(*exhaust(
            *map(lambda x: iter(x), map(f, iter(self)))
        ))
        if mut:
            self._carray = queue._carray
            return None
        return queue


class DQueue(Queue):
    """Double sided queue datastructure.

    Will resize itself as needed.

    None represents the absence of a value and are ignored if pushed on the
    queue. Use another object, like an empty tuple (), as a sentinal values.
    """
    def __init__(self, *ds):
        """Construct a FIFO queue data structure."""
        super().__init__(*ds)

    def __repr__(self):
        """Display data in dqueue."""
        return ">< " + " | ".join(map(lambda x: repr(x), iter(self))) + " ><"

    def copy(self):
        dqueue = DQueue()
        dqueue._carray = self._carray.copy()
        return dqueue

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

    def map(self, f: Callable[[Any], Any], mut: bool=False) -> DQueue|None:
        """Apply function over DQueue contents. If mut=True (the default) mutate
        the DQueue & don't return anything. Othersise, return a new DQueue
        leaving the original unchanged. Suppress any None Values returned by f.
        """
        dqueue  = DQueue(*map(f, iter(self)))
        if mut:
            self._carray = dqueue._carray
            return None
        return dqueue

    def flatMap(self, f: Callable[[Any], DQueue], mut: bool=False) -> DQueue|None:
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

    def mergeMap(self, f: Callable[[Any], DQueue], mut: bool=False) -> DQueue|None:
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

    def exhaustMap(self, f: Callable[[Any], DQueue], mut: bool=False) -> DQueue|None:
        """Apply function over the DQueue's contents and flatten result by round
        robin merging until all the DQueues produced by f are exhausted. If
        mut=True (default) mutate the DQueue & don't return anything. Othersise,
        return a new DQueue leaving the original unchanged. Suppress any None
        Values contained in any of the DQueues returned by f.
        """
        dqueue = DQueue(*exhaust(
            *map(lambda x: iter(x), map(f, iter(self)))
        ))
        if mut:
            self._carray = dqueue._carray
            return None
        return dqueue

if __name__ == "__main__":
    pass
