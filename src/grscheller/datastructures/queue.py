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
from .core.iterlib import mergeIters, exhaustIters
from .core.carray import Carray

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
        self._carray = Carray()
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
        dataListStrs = []
        for data in self._carray:
            dataListStrs.append(repr(data))
        return "<< " + " | ".join(dataListStrs) + " <<"

    def copy(self) -> Queue:
        """Return shallow copy of the queue in O(n) time & space complexity."""
        new_queue = Queue()
        new_queue._carray = self._carray.copy()
        return new_queue

    def push(self, *ds: Any) -> Queue:
        """Push data on rear of queue & return reference to self."""
        for d in ds:
            if d != None:
                self._carray.pushR(d)
        return self

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

    def capacity(self) -> int:
        """Returns current capacity of queue."""
        return self._carray.capacity()

    def fractionFilled(self) -> float:
        """Returns current capacity of queue."""
        return self._carray.fractionFilled()

    def resize(self, addCapacity = 0) -> Self:
        """Compact queue and add extra capacity."""
        self._carray.resize(addCapacity)
        return self

    def map(self, f: Callable[[Any], Any], mut: bool=False) -> Self|Queue:
        """Apply function over queue contents.

        Return new Queue if mut=False (the default)
        otherwise mutate the data structure and return self.
        """
        newQueue  = Queue(*map(f, iter(self)))
        if mut:
            self._carray = newQueue._carray
            return self
        return newQueue

    def flatMap(self, f: Callable[[Any], Queue], mut: bool=False) -> Self|Queue:
        """Apply function and flatten result, surpress any None values.

        Merge the queues produced sequentially front-to-back.

        Return new Queue if mut=False (the default)
        otherwise mutate the data structure and return self.
        """
        newQueue = Queue(*chain(*(iter(x) for x in map(f, iter(self)))))
        if mut:
            self._carray = newQueue._carray
            return self
        return newQueue

    def mergeMap(self, f: Callable[[Any], Queue], mut: bool=False) -> Self|Queue:
        """Apply function and flatten result, surpress any None values.

        Round Robin Merge the queues produced until first cached queue is
        exhausted.

        Return new Queue if mut=False (the default)
        otherwise mutate the data structure and return self.
        """
        newQueue = Queue(*mergeIters(*(iter(x) for x in map(f, iter(self)))))
        if mut:
            self._carray = newQueue._carray
            return self
        return newQueue

    def exhaustMap(self, f: Callable[[Any], Queue], mut: bool=False) -> Self|Queue:
        """Apply function and flatten result, surpress any None values.

        Return new Queue if mut=False (the default)
        otherwise mutate the data structure and return self.
        """
        newQueue = Queue(*exhaustIters(*(iter(x) for x in map(f, iter(self)))))
        if mut:
            self._carray = newQueue._carray
            return self
        return newQueue

if __name__ == "__main__":
    pass
