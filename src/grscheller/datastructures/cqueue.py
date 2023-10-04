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

"""Module grscheller.datastructure.carray - Double sided queue

Double sided circular array with amortized O(1) insertions & deletions from
either end and O(1) length determination. Implemented with a Python List.

Mainy used as an implementation detail for other grscheller.datastructure
classes, but not marked private since it could be useful to use in itself. This
class is not opinionated regarding None as a value. It freely stores None values
and will return None to indicate the absence of a value. Therfore don't rely on
using None as a sentital value to determine if a carray is empty or not, use it
in a boolean context instead. Returns false if empty, otherwise true.
"""

from __future__ import annotations

__all__ = ['Cqueue']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

from typing import Any, Callable
from .core import concatIters, mergeIters, mapIter

class Cqueue:
    """Double sided queue datastructure. Will resize itself as needed. Does not
    throw exceptions.
    """
    def __init__(self, *data):
        """Construct a double sided queue"""
        size = len(data)
        capacity = size + 2
        self._capacity = capacity
        self._count = size
        self._front = 0
        self._rear = (size - 1) % capacity
        self._queue = list(data)
        self._queue.append(None)
        self._queue.append(None)

    def _isFull(self) -> bool:
        """Returns true if cArray is full"""
        return self._count == self._capacity

    def _double(self):
        """Double capacity of carray"""
        if self._front > self._rear:
            frontPart = self._queue[self._front:]
            rearPart = self._queue[:self._rear+1]
        else:
            frontPart = self._queue
            rearPart = []
        self._queue = frontPart + rearPart + [None]*(self._capacity)
        self._capacity *= 2
        self._front = 0
        self._rear = self._count - 1

    def _compact(self):
        """Compact the datastructure as much as possible"""
        match self._count:
            case 0:
                self._queue = [None]*2
                self._capacity = 2
                self._front = 0
                self._rear = 1
            case 1:
                self._queue = [self._queue[self._front], None]
                self._capacity = 2
                self._front = 0
                self._rear = 0
            case _:
                if self._front > self._rear:
                    frontPart = self._queue[self._front:]
                    rearPart = self._queue[:self._rear+1]
                else:
                    frontPart = self._queue[self._front:self._rear+1]
                    rearPart = []
                self._queue = frontPart + rearPart
                self._capacity = self._count
                self._front = 0
                self._rear = self._capacity - 1

    def __bool__(self):
        """Returns true if carray is not empty"""
        return self._count > 0

    def __len__(self) -> int:
        """Returns current number of values in carray"""
        return self._count

    def __getitem__(self, idx: int) -> Any | None:
        """Get value at a valid index, otherwise return None.

        Together with __len__ method, allows the reversed() function to return
        a reverse iterator.
        """
        cnt = self._count
        if 0 <= idx < cnt:
            return self._queue[(self._front + idx) % self._capacity]
        elif -cnt <= idx < 0:
            return self._queue[(self._front + cnt + idx) % self._capacity]
        else:
            return None

    def __setitem__(self, idx: int, value) -> bool:
        """Set value at a valid index and return true, otherwise return false.

        TODO: is silently doing nothing the right thing, or do I throw some sort
        of index out of bound exception? It is a "exceptional" event.
        """
        cnt = self._count
        if 0 <= idx < cnt:
            self._queue[(self._front + idx) % self._capacity] = value
        elif -cnt <= idx < 0:
            self._queue[(self._front + cnt + idx) % self._capacity] = value
        else:
            return False
        return True

    def __iter__(self):
        """Iterator yielding data stored in dequeue, does not consume data.

        To export contents of the carray to a list: myList = list(myCarray)
        """
        if self._count > 0:
            cap = self._capacity
            rear = self._rear
            pos = self._front
            while pos != rear:
                yield self._queue[pos]
                pos = (pos + 1) % cap
            yield self._queue[pos]

    def __eq__(self, other):
        """Returns True if all the data stored in both compare as equal.
        Worst case is O(n) behavior for the true case.
        """
        if not isinstance(other, type(self)):
            return False

        if self._count != other._count:
            return False

        cnt = self._count
        left = self
        frontL = self._front
        capL = self._capacity
        right = other
        frontR = other._front
        capR = other._capacity
        nn = 0
        while nn < cnt:
            if left._queue[(frontL+nn)%capL] != right._queue[(frontR+nn)%capR]:
                return False
            nn += 1
        return True

    def __repr__(self):
        """Display data in the carray"""
        dataListStrs = []
        for data in self:
            dataListStrs.append(repr(data))
        return "[[ " + " | ".join(dataListStrs) + " ]]"

    def copy(self) -> Cqueue:
        """Return shallow copy of the carray in O(n) time & space complexity"""
        return Cqueue(*self)

    def pushR(self, data: Any) -> Cqueue:
        """Push data on rear of carray, return the carray pushed to"""
        if self._isFull():
            self._double()
        self._rear = (self._rear + 1) % self._capacity
        self._queue[self._rear] = data
        self._count += 1
        return self

    def pushL(self, data: Any) -> Cqueue:
        """Push data on front of carray, return the carray pushed to"""
        if self._isFull():
            self._double()
        self._front = (self._front - 1) % self._capacity
        self._queue[self._front] = data
        self._count += 1
        return self

    def popR(self) -> Any|None:
        """Pop data off rear of carray"""
        if self._count == 0:
            return None
        else:
            data = self._queue[self._rear]
            self._queue[self._rear] = None
            self._rear = (self._rear - 1) % self._capacity
            self._count -= 1
            return data

    def popL(self) -> Any|None:
        """Pop data off front of carray"""
        if self._count == 0:
            return None
        else:
            data = self._queue[self._front]
            self._queue[self._front] = None
            self._front = (self._front + 1) % self._capacity
            self._count -= 1
            return data

    def capacity(self) -> int:
        """Returns current capacity of carray"""
        return self._capacity

    def fractionFilled(self) -> float:
        """Returns current capacity of carray"""
        return self._count/self._capacity

    def resize(self, addCapacity = 0):
        """Compact carray and add extra capacity"""
        self._compact()
        if addCapacity > 0:
            self._queue = self._queue + [None]*addCapacity
            self._capacity += addCapacity
            if self._count == 0:
                self._rear = self._capacity - 1

    def map(self, f: Callable[[Any], Any]) -> Cqueue:
        """Apply function over carray contents, returns new instance"""
        return Cqueue(*mapIter(iter(self), f))

    def flatMap(self, f: Callable[[Any], Cqueue]) -> Cqueue:
        """Apply function and flatten result, returns new instance"""
        return Cqueue(
            *concatIters(
                *mapIter(mapIter(iter(self), f), lambda x: iter(x))
            )
        )

    def mergeMap(self, f: Callable[[Any], Cqueue]) -> Cqueue:
        """Apply function and flatten result, returns new instance"""
        return Cqueue(
            *mergeIters(
                *mapIter(mapIter(iter(self), f), lambda x: iter(x))
            )
        )

if __name__ == "__main__":
    pass
