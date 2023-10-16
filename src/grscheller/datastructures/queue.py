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

"""Module grscheller.datastructure.queue - LIFO queue

LIFO queue with amortized O(1) pushing & popping from the queue.
Obtaining length (number of elements) of a Queue is also a O(1) operation.

Implemented with a Python List based circular array.
"""

from __future__ import annotations

__all__ = ['Queue']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

from typing import Any, Callable
from .circle import Circle
from .functional.maybe import Maybe, Nothing, Some
from .iterlib import concatIters, mapIter

class Queue():
    """FIFO queue datastructure. Will resize itself as needed.

    The Queue class consistently uses None to represent the absence of a value.
    None will not be pushed to this datastructure. As an alternative, use Maybe
    objects of type Nothing, or the empty tuple () to represent a non-existent
    value. 
    """
    def __init__(self, *ds):
        """Construct a FIFO queue datastructure"""
        self._circle = Circle()
        for d in ds:
            self._circle.pushR(d)

    def __bool__(self) -> bool:
        """Returns true if queue is not empty"""
        return len(self._circle) != 0

    def __len__(self) -> int:
        """Returns current number of values in queue"""
        return len(self._circle)

    def __iter__(self):
        """Iterator yielding data currently stored in queue"""
        currCircle = self._circle.copy()
        for pos in range(len(currCircle)):
            yield currCircle[pos]

    def __reversed__(self):
        """Reverse iterate over the current state of the queue"""
        for data in reversed(self._circle.copy()):
            yield data

    def __eq__(self, other):
        """Returns True if all the data stored in both compare as equal.
        Worst case is O(n) behavior for the true case.
        """
        if not isinstance(other, type(self)):
            return False
        return self._circle == other._circle

    def __repr__(self):
        """Display data in queue"""
        dataListStrs = []
        for data in self._circle:
            dataListStrs.append(repr(data))
        return "<< " + " | ".join(dataListStrs) + " <<"

    def copy(self) -> Queue:
        """Return shallow copy of the queue in O(n) time & space complexity"""
        new_queue = Queue()
        new_queue._circle = self._circle.copy()
        return new_queue

    def push(self, *ds: Any) -> Queue:
        """Push data on rear of queue & return reference to self"""
        for d in ds:
            if d != None:
                self._circle.pushR(d)
        return self

    def pop(self) -> Maybe:
        """Pop data off front of queue"""
        if len(self._circle) > 0:
            return Some(self._circle.popL())
        else:
            return Nothing

    def peakLastIn(self) -> Maybe:
        """Return last element pushed to queue without consuming it"""
        if len(self._circle) > 0:
            return Some(self._circle[-1])
        else:
            return Nothing

    def peakNextOut(self) -> Maybe:
        """Return next element ready to pop from queue without consuming it"""
        if len(self._circle) > 0:
            return Some(self._circle[0])
        else:
            return Nothing

    def capacity(self) -> int:
        """Returns current capacity of queue"""
        return self._circle.capacity()

    def fractionFilled(self) -> float:
        """Returns current capacity of queue"""
        return self._circle.fractionFilled()

    def resize(self, addCapacity = 0):
        """Compact queue and add extra capacity"""
        return self._circle.resize(addCapacity)

    def map(self, f: Callable[[Any], Any]) -> Queue:
        """Apply function over queue contents, returns new instance"""
        return Queue(*mapIter(iter(self), f))

    def mapSelf(self, f: Callable[[Any], Any]) -> Queue:
        """Apply function over queue contents"""
        copy = Queue(*mapIter(iter(self), f))
        self._circle = copy._circle
        return self

    def flatMap(self, f: Callable[[Any], Queue]) -> Queue:
        """Apply function and flatten result, returns new instance"""
        return Queue(
            *concatIters(
                *mapIter(mapIter(iter(self), f), lambda x: iter(x))
            )
        )

if __name__ == "__main__":
    pass
