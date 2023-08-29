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

"""Double sided queue

Module implementing a Queue with amortized O(1) insertions & deletions from
either end. Obtaining length (number of elements) of a Dqueue is also a O(1)
operation.

Implemented with a Python List based circular array.
"""
__all__ = ['Dqueue']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

class Dqueue:
    """
    Double sided queue datastructure. Will resize itself as needed.

    Exceptions
    ----------
    Does not throw exceptions. The Dqueue class consistently uses None to
    represent the absence of a value. Therefore care needs to be taken when
    None "values" are stored in Dqueue objects.
    """
    def __init__(self, *data):
        """
        Parameters
        ----------
            *data : 'any'
                Any type data, except 'None', to prepopulate the stack.
                The data is pushed onto the stack left to right.
        """
        size = len(data)
        capacity = size + 2
        self._capacity = capacity
        self._count = size
        self._front = 0
        self._rear = (size - 1) % capacity
        self._queue = list(data)
        self._queue.append(None)
        self._queue.append(None)

    def _isFull(self):
        """Returns true if dqueue is full."""
        return self._count == self._capacity

    def _double(self):
        """Double capacity of dqueue."""
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
        """Compact the datastructure as much as possible."""
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

    def pushR(self, data):
        """Push data on rear of dqueue. Return the value being pushed."""
        if self._isFull():
            self._double()
        self._rear = (self._rear + 1) % self._capacity
        self._queue[self._rear] = data
        self._count += 1
        return self

    def pushL(self, data):
        """Push data on front of dqueue. Return the value being pushed."""
        if self._isFull():
            self._double()
        self._front = (self._front - 1) % self._capacity
        self._queue[self._front] = data
        self._count += 1
        return self

    def popR(self):
        """Pop data off rear of dqueue."""
        if self._count == 0:
            return None
        else:
            data = self._queue[self._rear]
            self._queue[self._rear] = None
            self._rear = (self._rear - 1) % self._capacity
            self._count -= 1
            return data

    def popL(self):
        """Pop data off front of dqueue."""
        if self._count == 0:
            return None
        else:
            data = self._queue[self._front]
            self._queue[self._front] = None
            self._front = (self._front + 1) % self._capacity
            self._count -= 1
            return data

    def __iter__(self):
        """Iterator yielding data stored in dequeue, does not consume data.

        To export contents of the Dqueue to a list, do
            myList = list(myDqueue)

        """
        if self._count > 0:
            pos = self._front
            while pos != self._rear:
                yield self._queue[pos]
                pos = (pos + 1) % self._capacity
            yield self._queue[pos]

    def __repr__(self):
        """Display data in dqueue."""
        dataListStrs = []
        for data in self:
            dataListStrs.append(repr(data))
        return ">< " + " | ".join(dataListStrs) + " ><"

    def __len__(self):
        """Returns current number of values in dequeue."""
        return self._count

    def __getitem__(self, ii):
        """Together with __len__ method, allows reversed() function to return
        a reverse iterator. Also allows for fetching values via indexing
        Dqueue objects, but not assigning to them. Valid indexes are from
        0 <= ii < self._count. Returns 'None' for an invalid index. Indexed
        values run left (front) to right (rear). If None "values" are pushed
        to the dqueue, care should be taken if when checking for index errors
        via a None being returned. Does not throw IndexError Exceptions.

        Returns
        -------
        data : 'any' | None
        """
        if 0 <= ii < self._count:
            return self._queue[(self._front + ii) % self._capacity]
        else:
            return None

    def isEmpty(self):
        """Returns true if the dqueue is empty."""
        return self._count == 0

    def capacity(self):
        """Returns current capacity of dqueue."""
        return self._capacity

    def fractionFilled(self):
        """Returns current capacity of dqueue."""
        return self._count/self._capacity

    def resize(self, addCapacity = 0):
        """Compact dqueue and add extra capacity"""
        self._compact()
        if addCapacity > 0:
            self._queue = self._queue + [None]*addCapacity
            self._capacity += addCapacity
            if self._count == 0:
                self._rear = self._capacity - 1

if __name__ == "__main__":
    pass
