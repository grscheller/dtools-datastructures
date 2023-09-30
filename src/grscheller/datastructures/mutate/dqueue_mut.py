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

"""Module grscheller.datastructure.mutate.dqueue_mut - Double sided queue

Double sided queue with amortized O(1) insertions & deletions from either end.
Obtaining length (number of elements) of a Dqueue_mut is also a O(1) operation.
Mutable version of grscheller.datastructures.dqueue.

Implemented with a Python List based circular array.
"""
from __future__ import annotations

__all__ = ['Dqueue_mut']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

from typing import Any, Callable

class Dqueue_mut:
    """Double sided queue datastructure. Will resize itself as needed.

    Does not throw exceptions. The Dqueue_mut class consistently uses None to
    represent the absence of a value. Therefore some care needs to be taken
    when Python None is pushed onto Dqueue_mut objects.
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
        """Returns true if dqueue_mut is full"""
        return self._count == self._capacity

    def _double(self):
        """Double capacity of dqueue_mut"""
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

    def pushR(self, data: Any) -> Dqueue_mut:
        """Push data on rear of dqueue_mut, return the dqueue_mut pushed to"""
        if self._isFull():
            self._double()
        self._rear = (self._rear + 1) % self._capacity
        self._queue[self._rear] = data
        self._count += 1
        return self

    def pushL(self, data: Any) -> Dqueue_mut:
        """Push data on front of dqueue_mut, return the dqueue_mut pushed to"""
        if self._isFull():
            self._double()
        self._front = (self._front - 1) % self._capacity
        self._queue[self._front] = data
        self._count += 1
        return self

    def popR(self) -> Any | None:
        """Pop data off rear of dqueue_mut"""
        if self._count == 0:
            return None
        else:
            data = self._queue[self._rear]
            self._queue[self._rear] = None
            self._rear = (self._rear - 1) % self._capacity
            self._count -= 1
            return data

    def popL(self) -> Any | None:
        """Pop data off front of dqueue_mut"""
        if self._count == 0:
            return None
        else:
            data = self._queue[self._front]
            self._queue[self._front] = None
            self._front = (self._front + 1) % self._capacity
            self._count -= 1
            return data

    def headR(self) -> Any | None:
        """Return rear element of dqueue_mut without consuming it"""
        if self._count == 0:
            return None
        return self._queue[self._rear]

    def headL(self) -> Any | None:
        """Return front element of dqueue_mut without consuming it"""
        if self._count == 0:
            return None
        return self._queue[self._front]

    def __iter__(self):
        """Iterator yielding data stored in dequeue, does not consume data.

        To export contents of the dqueue_mut to a list, do
            myList = list(myDqueue-mut)

        """
        if self._count > 0:
            pos = self._front
            while pos != self._rear:
                yield self._queue[pos]
                pos = (pos + 1) % self._capacity
            yield self._queue[pos]

    def __eq__(self, other):
        """Returns True if all the data stored on both are the same.
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
        """Display data in dqueue_mut"""
        dataListStrs = []
        for data in self:
            dataListStrs.append(repr(data))
        return ">< " + " | ".join(dataListStrs) + " ><"

    def __len__(self) -> int:
        """Returns current number of values in dqueue_mut"""
        return self._count

    def __bool__(self):
        """Returns true if dqueue_mut is not empty"""
        return self._count > 0

    def __getitem__(self, ii: int) -> Any | None:
        """Together with __len__ method, allows reversed() function to return
        a reverse iterator. Otherwise, indexing Dqueue objects should be
        considered private to the class.
        """
        if 0 <= ii < self._count:
            return self._queue[(self._front + ii) % self._capacity]
        else:
            return None

    def copy(self) -> Dqueue_mut:
        """Return shallow copy of the dqueue_mut in O(n) time & space complexity"""
        return Dqueue_mut(*self)

    def capacity(self) -> int:
        """Returns current capacity of dqueue_mut"""
        return self._capacity

    def fractionFilled(self) -> float:
        """Returns current capacity of dqueue_mut"""
        return self._count/self._capacity

    def resize(self, addCapacity = 0):
        """Compact dqueue_mut and add extra capacity"""
        self._compact()
        if addCapacity > 0:
            self._queue = self._queue + [None]*addCapacity
            self._capacity += addCapacity
            if self._count == 0:
                self._rear = self._capacity - 1

    def map(self, f: Callable[[Any], Any]) -> Dqueue_mut:
        """Map function over dqueue_mut contents, return same instance"""
        for _ in range(self._count):
            self.pushR(f(self.popL()))
        return self

if __name__ == "__main__":
    pass
