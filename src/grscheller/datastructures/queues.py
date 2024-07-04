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

"""Queue based datastructures.

* stateful queue data structures with amortized O(1) pushes and pops
* obtaining length (number of elements) of a queue is an O(1) operation
* implemented with Python List based circular array in a "has-a" relationship
* these data structures will resize themselves as needed

Types of Queues:

* class **FIFOQueue**: First In, First Out Queue
* class **LIFOQueue**: Last In, First Out Queue
* class **DoubleQueue**: Double Ended Queue
"""

from __future__ import annotations

__all__ = ['DoubleQueue', 'FIFOQueue', 'LIFOQueue']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023-2024 Geoffrey R. Scheller"
__license__ = "Apache License 2.0"

from typing import Callable, Generic, Iterator, Optional, TypeVar
from grscheller.circular_array.circular_array import CircularArray

_T = TypeVar('_T')
_S = TypeVar('_S')

class QueueBase(Generic[_T]):
    """Abstract base class for stateful queue-based data structures

    * primarily for DRY implementation inheritance of queue type classes
    * derived classes used will resize themselves as needed
    * each queue object "has-a" (contains) a circular array to store its data
    * care is needed if None is stored as a value on Queue data structures 
    """
    __slots__ = '_ca'

    def __init__(self, *ds: _T):
        """Construct a queue data structure. Cull None values."""
        self._ca: CircularArray[_T] = CircularArray(*ds)

    # TODO: change to yield in the "natural" data retrieval order of the queue
    def __iter__(self) -> Iterator[_T]:
        """Iterator yielding data currently stored in the queue. Data yielded in
        natural FIFO order.
        """
        ca = self._ca.copy()
        for pos in range(len(ca)):
            yield ca[pos]

    def __reversed__(self) -> Iterator[_T]:
        """Reverse iterate over the current state of the queue."""
        ca = self._ca.copy()
        for pos in range(len(ca)-1, -1, -1):
            yield ca[pos]

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(' + ', '.join(map(repr, self)) + ')'

    def __bool__(self) -> bool:
        """Returns `True` if queue is not empty."""
        return len(self._ca) > 0

    def __len__(self) -> int:
        """Returns current number of values in queue."""
        return len(self._ca)

    def __eq__(self, other: object) -> bool:
        """Returns `True` if all the data stored in both compare as equal.
        Worst case is O(n) behavior for the true case.
        """
        if not isinstance(other, type(self)):
            return False
        return self._ca == other._ca

    # TODO: change to fold in the "natural" data retrieval order of the queue

    def foldL(self, f:Callable[[_T, _T], _T]) -> Optional[_T]:
        return self._ca.foldL(f)

    def foldR(self, f:Callable[[_T, _T], _T]) -> Optional[_T]:
        return self._ca.foldR(f)

    def foldL1(self, f:Callable[[_S, _T], _S], init: _S) -> _S:
        return self._ca.foldL1(f, init)

    def foldR1(self, f:Callable[[_T, _S], _S], init: _S) -> _S:
        return self._ca.foldR1(f, init)

class FIFOQueue(QueueBase[_T]):
    """Stateful single sided FIFO data structure. Will resize itself as needed. `None`
    represents the absence of a value and ignored if pushed onto the queue.
    """
    __slots__ = ()

    def __str__(self) -> str:
        return "<< " + " < ".join(map(str, self)) + " <<"

    def copy(self) -> FIFOQueue[_T]:
        """Return shallow copy of the `FIFOQueue` in O(n) time & space complexity."""
        return FIFOQueue(*self)

    def map(self, f: Callable[[_T], Optional[_S]]) -> FIFOQueue[_S]:
        """Apply function over the FIFO queue's contents.

        * suppress any `None` values returned by `f`

        """
        # initializer strips the None values
        return FIFOQueue(*map(f, self))          # type: ignore

    def push(self, *ds: _T) -> None:
        """Push data onto the `FIFOQueue`."""
        self._ca.pushR(*ds)

    def pop(self) -> Optional[_T]:
        """Pop data off front of the `FIFOQueue`."""
        return self._ca.popL()

    def peak_last_in(self) -> Optional[_T]:
        """Return last element pushed to the `FIFOQueue` without consuming it"""
        if self._ca:
            return self._ca[-1]
        else:
            return None

    def peak_next_out(self) -> Optional[_T]:
        """Return next element ready to `pop` from the `FIFOQueue`."""
        if self._ca:
            return self._ca[0]
        else:
            return None

class LIFOQueue(QueueBase[_T]):
    """Stateful single sided LIFO data structure. Will resize itself as needed. `None`
    represents the absence of a value and ignored if pushed onto the queue.
    """
    __slots__ = ()

    def __str__(self) -> str:
        return "|| " + " > ".join(map(str, self)) + " ><"

    def copy(self) -> LIFOQueue[_T]:
        """Return shallow copy of the `FIFOQueue` in O(n) time & space complexity."""
        return LIFOQueue(*self)

    def map(self, f: Callable[[_T], Optional[_S]]) -> LIFOQueue[_S]:
        """Apply function over the LIFO queue's contents.

        * suppress any `None` values returned by `f`

        """
        # initializer strips the None values
        return LIFOQueue(*map(f, self))          # type: ignore

    def push(self, *ds: _T) -> None:
        """Push data onto the `LIFOQueue` & no return value."""
        self._ca.pushR(*ds)

    def pop(self) -> Optional[_T]:
        """Pop data off rear of the `LIFOQueue`."""
        if self._ca:
            return self._ca.popR()
        else:
            return None

    def peak(self) -> Optional[_T]:
        """Return last element pushed to the `LIFOQueue` without consuming it."""
        if self._ca:
            return self._ca[-1]
        else:
            return None

class DoubleQueue(QueueBase[_T]):
    """Stateful double sided queue data structure. Will resize itself as needed.
    `None` represents the absence of a value and ignored if pushed onto the queue.
    """
    __slots__ = ()

    def __str__(self) -> str:
        return ">< " + " | ".join(map(str, self)) + " ><"

    def copy(self) -> DoubleQueue[_T]:
        """Return shallow copy of the `DoubleQueue` in O(n) time & space complexity."""
        dqueue: DoubleQueue[_T] = DoubleQueue()
        dqueue._ca = self._ca.copy()
        return dqueue

    def map(self, f: Callable[[_T], Optional[_S]]) -> DoubleQueue[_S]:
        """Apply function over the LIFO queue's contents.

        * suppress any `None` values returned by `f`

        """
        # initializer strips the None values
        return DoubleQueue(*map(f, self))          # type: ignore

    def pushR(self, *ds: _T) -> None:
        """Push data left to right onto rear of the `DoubleQueue`."""
        self._ca.pushR(*ds)

    def pushL(self, *ds: _T) -> None:
        """Push data left to right onto front of `DoubleQueue`."""
        self._ca.pushL(*ds)

    def popR(self) -> Optional[_T]:
        """Pop data off rear of the `DoubleQueue`."""
        return self._ca.popR()

    def popL(self) -> Optional[_T]:
        """Pop data off front of the `DoubleQueue`."""
        return self._ca.popL()

    def peakR(self) -> Optional[_T]:
        """Return rightmost element of the `DoubleQueue` if it exists."""
        if self._ca:
            return self._ca[-1]
        else:
            return None

    def peakL(self) -> Optional[_T]:
        """Return leftmost element of the `DoubleQueue` if it exists."""
        if self._ca:
            return self._ca[0]
        else:
            return None
