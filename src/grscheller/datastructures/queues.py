# Copyright 2023-2024 Geoffrey R. Scheller
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

"""Module grscheller.datastructure.queues - queue based datastructures

Module implementing stateful queue data structures with amortized O(1) pushing and
popping from the queue. Obtaining length (number of elements) of a queue is an O(1)
operation. Implemented with a Python List based circular array, these data structures
will resize themselves as needed. Does not store None as a value.
"""

from __future__ import annotations

__all__ = ['CircularArray', 'DoubleQueue', 'FIFOQueue', 'LIFOQueue']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

from typing import Any, Callable
from .core.fp import FP

class CircularArray:
    """Implements an auto-resizing, indexable, double sided queue data
    structure. O(1) indexing and O(1) pushes and pops either end. Mainly used to
    implement other grscheller.datastructure classes in a has-a relationship
    where its functionality is more likely restricted than augmented. This class
    is not opinionated regarding None as a value. It freely stores and returns
    None values. Can be use in a boolean context to determine if empty.
    """
    __slots__ = '_count', '_capacity', '_front', '_rear', '_list'

    def __init__(self, *data):
        """Construct a double sided queue"""
        size = len(data)
        capacity = size + 2
        self._count = size
        self._capacity = capacity
        self._front = 0
        self._rear = (size - 1) % capacity
        self._list = list(data)
        self._list.append(None)
        self._list.append(None)

    def __iter__(self):
        """Generator yielding the cached contents of the current state of
        the CircularArray.
        """
        if self._count > 0:
            cap = self._capacity
            rear = self._rear
            pos = self._front
            currList = self._list.copy()
            while pos != rear:
                yield currList[pos]
                pos = (pos + 1) % cap
            yield currList[pos]

    def __reversed__(self):
        """Generator yielding the cached contents of the current state of
        the CircularArray in reversed order.
        """
        if self._count > 0:
            cap = self._capacity
            front = self._front
            pos = self._rear
            currList = self._list.copy()
            while pos != front:
                yield currList[pos]
                pos = (pos - 1) % cap
            yield currList[pos]

    def __repr__(self):
        return f'{self.__class__.__name__}(' + ', '.join(map(repr, self)) + ')'

    def __str__(self):
        return "(|" + ", ".join(map(repr, self)) + "|)"

    def __bool__(self):
        """Returns true if circular array is not empty"""
        return self._count > 0

    def __len__(self):
        """Returns current number of values in the circlular array"""
        return self._count

    def __getitem__(self, index: int) -> Any:
        """Get value at a valid index, otherwise raise IndexError"""
        cnt = self._count
        if 0 <= index < cnt:
            return self._list[(self._front + index) % self._capacity]
        elif -cnt <= index < 0:
            return self._list[(self._front + cnt + index) % self._capacity]
        else:
            low = -cnt
            high = cnt - 1
            msg = f'Out of bounds: index = {index} not between {low} and {high}'
            msg += 'while getting value.'
            msg0 = 'Trying to get value from an empty data structure.'
            if cnt > 0:
                raise IndexError(msg)
            else:
                raise IndexError(msg0)

    def __setitem__(self, index: int, value: Any) -> Any:
        """Set value at a valid index, otherwise raise IndexError"""
        cnt = self._count
        if 0 <= index < cnt:
            self._list[(self._front + index) % self._capacity] = value
        elif -cnt <= index < 0:
            self._list[(self._front + cnt + index) % self._capacity] = value
        else:
            low = -cnt
            high = cnt - 1
            msg = f'Out of bounds: index = {index} not between {low} and {high}'
            msg += 'while setting value.'
            msg0 = 'Trying to get value from an empty data structure.'
            if cnt > 0:
                raise IndexError(msg)
            else:
                raise IndexError(msg0)

    def __eq__(self, other):
        """Returns True if all the data stored in both compare as equal.
        Worst case is O(n) behavior for the true case.
        """
        if not isinstance(other, type(self)):
            return False

        if self._count != other._count:
            return False

        left, frontL, capL, cnt = self, self._front, self._capacity, self._count
        right, frontR, capR = other, other._front, other._capacity

        nn = 0
        while nn < cnt:
            if left._list[(frontL+nn)%capL] != right._list[(frontR+nn)%capR]:
                return False
            nn += 1
        return True

    def _double(self) -> None:
        """Double capacity of circular array"""
        if self._front > self._rear:
            data  = self._list[self._front:]
            data += self._list[:self._rear+1]
            data += [None]*(self._capacity)
        else:
            data  = self._list
            data += [None]*(self._capacity)

        self._list, self._capacity,     self._front, self._rear = \
        data,       2 * self._capacity, 0,           self._count - 1

    def compact(self) -> None:
        """Compact the datastructure as much as possible"""
        match self._count:
            case 0:
                self._list, self._capacity, self._front, self._rear = [None]*2, 2, 0, 1
            case 1:
                data = [self._list[self._front], None]
                self._list, self._capacity, self._front, self._rear = data, 2, 0, 0
            case _:
                if self._front > self._rear:
                    data  = self._list[self._front:]
                    data += self._list[:self._rear+1]
                else:
                    data  = self._list[self._front:self._rear+1]
                self._list, self._capacity, self._front, self._rear = data, self._count, 0, self._capacity - 1

    def copy(self) -> CircularArray:
        return CircularArray(*self)

    def reverse(self) -> CircularArray:
        return CircularArray(*reversed(self))

    def pushR(self, d: Any) -> None:
        """Push data on rear of circle"""
        if self._count == self._capacity:
            self._double()
        self._rear = (self._rear + 1) % self._capacity
        self._list[self._rear] = d
        self._count += 1

    def pushL(self, d: Any) -> None:
        """Push data on front of circle"""
        if self._count == self._capacity:
            self._double()
        self._front = (self._front - 1) % self._capacity
        self._list[self._front] = d
        self._count += 1

    def popR(self) -> Any:
        """Pop data off rear of circle array, returns None if empty"""
        if self._count == 0:
            return None
        else:
            d = self._list[self._rear]

            self._count, self._list[self._rear], self._rear = \
                self._count-1, None, (self._rear - 1) % self._capacity

            return d

    def popL(self) -> Any:
        """Pop data off front of circle array, returns None if empty"""
        if self._count == 0:
            return None
        else:
            d = self._list[self._front]

            self._count, self._list[self._front], self._front = \
                self._count-1, None, (self._front+1) % self._capacity

            return d

    def empty(self) -> None:
        """Empty circular array, keep current capacity"""
        self._list, self._front, self._rear = \
            [None]*self._capacity, 0, self._capacity-1

    def capacity(self) -> int:
        """Returns current capacity of circle array"""
        return self._capacity

    def fractionFilled(self) -> float:
        """Returns current capacity of circle array"""
        return self._count/self._capacity

    def resize(self, addCapacity = 0) -> None:
        """Compact circle array and add extra capacity"""
        self.compact()
        if addCapacity > 0:
            self._list = self._list + [None]*addCapacity
            self._capacity += addCapacity
            if self._count == 0:
                self._rear = self._capacity - 1

    def map(self, f: Callable[[Any], Any]) -> CircularArray:
        """Apply function over the circular array's contents and return new
        circular array.
        """
        return CircularArray(*map(f, self))

    def mapSelf(self, f: Callable[[Any], Any]) -> None:
        """Apply function over the circular array's contents mutatng the
        circular array, don't return anything.
        """
        ca  = CircularArray(*map(f, self))
        self._count, self._capacity, self._front, self._rear, self._list = \
            ca._count, ca._capacity, ca._front, ca._rear, ca._list

class QueueBase():
    """Abstract base class for the purposes of DRY inheritance of classes
    implementing queue type data structures with a list based circular array.
    Each queue object "has-a" (contains) a circular array to store its data. The
    circular array used will resize itself as needed. Each QueueBase subclass
    must ensure that None values do not get pushed onto the circular array.
    """
    __slots__ = '_ca',

    def __init__(self, *ds):
        """Construct a queue data structure. Cull None values."""
        self._ca = CircularArray()
        for d in ds:
            if d is not None:
                self._ca.pushR(d)

    def __iter__(self):
        """Iterator yielding data currently stored in queue. Data yielded in
        natural FIFO order.
        """
        cached = self._ca.copy()
        for pos in range(len(cached)):
            yield cached[pos]

    def __reversed__(self):
        """Reverse iterate over the current state of the queue."""
        cached = self._ca.copy()
        for pos in range(len(cached)-1, -1, -1):
            yield cached[pos]

    def __repr__(self):
        return f'{self.__class__.__name__}(' + ', '.join(map(repr, self)) + ')'

    def __bool__(self):
        """Returns true if queue is not empty."""
        return len(self._ca) > 0

    def __len__(self):
        """Returns current number of values in queue."""
        return len(self._ca)

    def __eq__(self, other):
        """Returns True if all the data stored in both compare as equal.
        Worst case is O(n) behavior for the true case.
        """
        if not isinstance(other, type(self)):
            return False
        return self._ca == other._ca

    def map(self, f: Callable[[Any], Any]) -> None:
        """Apply function over the queue's contents. Suppress any None values
        returned by f.
        """
        self._ca = QueueBase(*map(f, self))._ca

    def reverse(self):
        """Reverse the elements in the Queue"""
        self._ca = self._ca.reverse()

class FIFOQueue(QueueBase, FP):
    """Stateful single sided FIFO data structure. Will resize itself as needed.
    None represents the absence of a value and ignored if pushed onto an FIFOQueue.
    """
    __slots__ = ()

    def __str__(self):
        return "<< " + " < ".join(map(str, self)) + " <<"

    def copy(self) -> FIFOQueue:
        """Return shallow copy of the FIFOQueue in O(n) time & space complexity."""
        fifoqueue = FIFOQueue()
        fifoqueue._ca = self._ca.copy()
        return fifoqueue

    def push(self, *ds: Any) -> None:
        """Push data on rear of the FIFOQueue & no return value."""
        for d in ds:
            if d != None:
                self._ca.pushR(d)

    def pop(self) -> Any:
        """Pop data off front of the FIFOQueue."""
        return self._ca.popL()

    def peakLastIn(self) -> Any:
        """Return last element pushed to the FIFOQueue without consuming it"""
        if self._ca:
            return self._ca[-1]
        else:
            return None

    def peakNextOut(self) -> Any:
        """Return next element ready to pop from the FIFOQueue."""
        if self._ca:
            return self._ca[0]
        else:
            return None

class LIFOQueue(QueueBase, FP):
    """Stateful single sided LIFO data structure. Will resize itself as needed.
    None represents the absence of a value and ignored if pushed onto an FIFOQueue.
    """
    __slots__ = ()

    def __str__(self):
        return "|| " + " > ".join(map(str, self)) + " ><"

    def copy(self) -> LIFOQueue:
        """Return shallow copy of the FIFOQueue in O(n) time & space complexity."""
        lifoqueue = LIFOQueue()
        lifoqueue._ca = self._ca.copy()
        return lifoqueue

    def push(self, *ds: Any) -> None:
        """Push data on rear of the LIFOQueue & no return value."""
        for d in ds:
            if d != None:
                self._ca.pushR(d)

    def pop(self) -> Any:
        """Pop data off rear of the LIFOQueue."""
        return self._ca.popR()

    def peak(self) -> Any:
        """Return last element pushed to the LIFOQueue without consuming it"""
        if self._ca:
            return self._ca[-1]
        else:
            return None

class DoubleQueue(QueueBase, FP):
    """Stateful double sided queue datastructure. Will resize itself as needed.
    None represents the absence of a value and ignored if pushed onto a DoubleQueue.
    """
    __slots__ = ()

    def __str__(self):
        return ">< " + " | ".join(map(str, self)) + " ><"

    def copy(self) -> DoubleQueue:
        """Return shallow copy of the DoubleQueue in O(n) time & space complexity."""
        dqueue = DoubleQueue()
        dqueue._ca = self._ca.copy()
        return dqueue

    def pushR(self, *ds: Any) -> None:
        """Push data left to right onto rear of the DoubleQueue."""
        for d in ds:
            if d != None:
                self._ca.pushR(d)

    def pushL(self, *ds: Any) -> None:
        """Push data left to right onto front of DoubleQueue."""
        for d in ds:
            if d != None:
                self._ca.pushL(d)

    def popR(self) -> Any:
        """Pop data off rear of the DoubleQueue"""
        return self._ca.popR()

    def popL(self) -> Any:
        """Pop data off front of the DoubleQueue"""
        return self._ca.popL()

    def peakR(self) -> Any:
        """Return right-most element of the DoubleQueue if it exists."""
        if self._ca:
            return self._ca[-1]
        else:
            return None

    def peakL(self) -> Any:
        """Return left-most element of the DoubleQueue if it exists."""
        if self._ca:
            return self._ca[0]
        else:
            return None

    def __getitem__(self, index: int) -> Any:
        return self._ca[index]

    def __setitem__(self, index: int, value):
        self._ca[index] = value

if __name__ == "__main__":
    pass
