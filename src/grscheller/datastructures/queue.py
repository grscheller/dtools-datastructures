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

"""Module grscheller.datastructure.queue - FIFO queue

FIFO queue with amortized O(1) pushing & popping from the queue.
Obtaining length (number of elements) of a Queue is also a O(1) operation.

Implemented with a Python List based circular array. Does not store None as
a value.
"""

from __future__ import annotations

__all__ = ['Queue']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

from typing import Any, Callable, Self
from itertools import chain
from .core.iterlib import merge, exhaust
from .core.carray import CArray

class Queue():
    """Module grscheller.datastructure.queue - FIFO queue

    The Queue class consistently uses None to represent the absence of a value.
    None will not be pushed to this datastructure. Other alternatives, use Maybe
    objects of type Nothing, or just the empty tuple (), as sentital values. One
    advantage os () over None is that () is iterable and thus making type
    checkers more happy.

    A Queue instance will resize itself as needed.
    """
    def __init__(self, *ds):
        """Construct a FIFO queue data structure.

        Null values will be culled from the intial data from ds.
        """
        self._carray = CArray()
        for d in ds:
            if d is not None:
                self._carray.pushR(d)

    def __bool__(self) -> bool:
        """Returns true if queue is not empty."""
        return len(self._carray) != 0

    def __len__(self) -> int:
        """Returns current number of values in queue."""
        return len(self._carray)

    def __iter__(self):
        """Iterator yielding data currently stored in queue.

        Data yielded in natural FIFO order.
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

    def __repr__(self):
        """Display data in queue."""
        return "<< " + " < ".join(map(lambda x: repr(x), iter(self))) + " <<"

    def copy(self) -> Queue:
        """Return shallow copy of the queue in O(n) time & space complexity."""
        new_queue = Queue()
        new_queue._carray = self._carray.copy()
        return new_queue

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

    def map(self, f: Callable[[Any], Any], mut: bool=True) -> Queue|None:
        """Apply function over Queue contents. If mut=True (the default) mutate
        the Queue & don't return anything. Othersise, return a new Queue leaving
        the original unchanged. Suppress any None Values returned by f.
        """
        queue  = Queue(*map(f, iter(self)))
        if mut:
            self._carray = queue._carray
            return None
        return queue

    def flatMap(self, f: Callable[[Any], Queue], mut: bool=True) -> None|Queue:
        """Apply function over the queue's contents and flatten result merging
        the queues produced sequentially front-to-back. If mut=True (default)
        mutate the Queue & don't return anything. Othersise, return a new Queue
        leaving the original unchanged. Suppress any None Values contained in
        any of the Queues returned by f.
        """
        queue = Queue(*chain(
            *(iter(x) for x in map(f, iter(self)))
        ))
        if mut:
            self._carray = queue._carray
            return None
        return queue

    def mergeMap(self, f: Callable[[Any], Queue], mut: bool=True) -> None|Queue:
        """Apply function over the Queue's contents and flatten result by round
        robin merging until one of the first Queues produced by f is exhausted.
        If mut=True (default) mutate the Queue & don't return anything.
        Othersise, return a new Queue leaving the original unchanged. Suppress
        any None Values contained in any of the Queues returned by f.
        """
        queue = Queue(*merge(
            *map(lambda x: iter(x), map(f, iter(self)))
        ))
        if mut:
            self._carray = queue._carray
            return None
        return queue

    def exhaustMap(self, f: Callable[[Any], Queue], mut: bool=True) -> None|Queue:
        """Apply function over the Queue's contents and flatten result by round
        robin merging until all the Queues produced by f are exhausted. If
        mut=True (default) mutate the Queue & don't return anything. Othersise,
        return a new Queue leaving the original unchanged. Suppress any None
        Values contained in any of the Queues returned by f.
        """
        queue = Queue(*exhaust(
            *map(lambda x: iter(x), map(f, iter(self)))
        ))
        if mut:
            self._carray = queue._carray
            return None
        return queue

if __name__ == "__main__":
    pass
