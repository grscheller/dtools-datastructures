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

__all__ = ['DoubleQueue', 'FIFOQueue', 'LIFOQueue', 'QueueBase']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023-2024 Geoffrey R. Scheller"
__license__ = "Apache License 2.0"

from typing import Callable, Generic, Iterator, Optional, TypeVar
from grscheller.circular_array.ca import CircularArray

_T = TypeVar('_T')
_S = TypeVar('_S')

class QueueBase(Generic[_T]):
    """Base class for stateful queue-based data structures

    * provided to allow users to define their own queue type classes
    * primarily for DRY implementation inheritance and generics
    * each queue object "has-a" (contains) a circular array to store its data
    * initial data to initializer stored in same order as provided
    * some care is needed if storing `None` as a value in these data structures
    """
    __slots__ = '_ca'

    def __init__(self, *ds: _T):
        """Construct a queue data structure.

        * data always internally stored in the same order as `ds`
        """
        self._ca: CircularArray[_T] = CircularArray(*ds)

    def __bool__(self) -> bool:
        """Returns `True` if queue is not empty."""
        return len(self._ca) > 0

    def __len__(self) -> int:
        """Returns current number of values in queue."""
        return len(self._ca)

    def __eq__(self, other: object) -> bool:
        """Returns `True` if all the data stored in both compare as equal.

        * worst case is O(n) behavior for the true case.
        """
        if not isinstance(other, type(self)):
            return False
        return self._ca == other._ca

class FIFOQueue(QueueBase[_T]):
    """Stateful First In First Out (FIFO) data structure.

    * will resize itself larger as needed
    * initial data pushed on in natural FIFO order
    """
    __slots__ = ()

    def __iter__(self) -> Iterator[_T]:
        """Iterator yielding data currently stored in the queue.

        * data yielded in natural FIFO order.
        """
        ca = self._ca.copy()
        for pos in range(len(ca)):
            yield ca[pos]

    def __repr__(self) -> str:
        return 'FIFOQueue(' + ', '.join(map(repr, self._ca)) + ')'

    def __str__(self) -> str:
        return "<< " + " < ".join(map(str, self)) + " <<"

    def copy(self) -> FIFOQueue[_T]:
        """Return shallow copy of the `FIFOQueue` in O(n) time & space complexity."""
        return FIFOQueue(*self._ca)

    def map(self, f: Callable[[_T], _S]) -> FIFOQueue[_S]:
        """Apply function over the FIFO queue's contents."""
        return FIFOQueue(*map(f, self._ca))

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

    def fold(self, f:Callable[[_T, _T], _T]) -> Optional[_T]:
        """Reduce with f.

        * returns a value of the of type _T if self is not empty
        * returns None if self is empty
        * folds in natural FIFO Order
        """
        return self._ca.foldL(f)

    def fold1(self, f:Callable[[_S, _T], _S], init: _S) -> _S:
        """Reduce with f.

        * returns a value of the of type _S
        * type _S can be same type as _T
        * folds in natural FIFO Order
        """
        return self._ca.foldL1(f, init)

class LIFOQueue(QueueBase[_T]):
    """Stateful Last In First Out (LIFO) data structure.

    * will resize itself larger as needed
    * initial data pushed on in natural LIFO order
    """
    __slots__ = ()

    def __iter__(self) -> Iterator[_T]:
        """Iterator yielding data currently stored in the queue.

        * data yielded in natural LIFO order.
        """
        ca = self._ca.copy()
        for pos in range(len(ca)-1, -1, -1):
            yield ca[pos]

    def __repr__(self) -> str:
        return 'LIFOQueue(' + ', '.join(map(repr, self._ca)) + ')'

    def __str__(self) -> str:
        return "|| " + " > ".join(map(str, self)) + " ><"

    def copy(self) -> LIFOQueue[_T]:
        """Return shallow copy of the `FIFOQueue` in O(n) time & space complexity."""
        return LIFOQueue(*self._ca)

    def map(self, f: Callable[[_T], _S]) -> LIFOQueue[_S]:
        """Apply function over the LIFO queue's contents."""
        return LIFOQueue(*map(f, self._ca))

    def push(self, *ds: _T) -> None:
        """Push data onto the `LIFOQueue` & no return value."""
        self._ca.pushR(*ds)

    def pop(self) -> Optional[_T]:
        """Pop data off rear of the `LIFOQueue`."""
        return self._ca.popR()

    def peak(self) -> Optional[_T]:
        """Return last element pushed to the `LIFOQueue` without consuming it."""
        if self._ca:
            return self._ca[-1]
        else:
            return None

    def fold(self, f:Callable[[_T, _T], _T]) -> Optional[_T]:
        """Reduce with f.

        * returns a value of the of type _T if self is not empty
        * returns None if self is empty
        * folds in natural LIFO Order
        """
        return self._ca.foldR(f)

    def fold1(self, f:Callable[[_S, _T], _S], init: _S) -> _S:
        """Reduce with f.

        * always returns a value of type _S
        * type _S can be the same type as _T
        * folds in natural LIFO Order
        """
        return self._ca.foldR1(lambda s, t: f(t, s), init)

class DoubleQueue(QueueBase[_T]):
    """Stateful Double Sided Queue data structure.

    * will resize itself larger as needed
    * initial data pushed on in FIFO order
    """
    __slots__ = ()

    def __iter__(self) -> Iterator[_T]:
        """Iterator yielding data currently stored in the queue.

        * data yielded in FIFO (left to right) order.
        """
        ca = self._ca.copy()
        for pos in range(len(ca)):
            yield ca[pos]

    def __repr__(self) -> str:
        return 'DoubleQueue(' + ', '.join(map(repr, self)) + ')'

    def __str__(self) -> str:
        return ">< " + " | ".join(map(str, self)) + " ><"

    def copy(self) -> DoubleQueue[_T]:
        """Return shallow copy of the `DoubleQueue` in O(n) time & space complexity."""
        dqueue: DoubleQueue[_T] = DoubleQueue()
        dqueue._ca = self._ca.copy()
        return dqueue

    def map(self, f: Callable[[_T], Optional[_S]]) -> DoubleQueue[_S]:
        """Apply function over the Double queue's contents."""
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

    def foldL(self, f:Callable[[_T, _T], _T]) -> Optional[_T]:
        """Reduce Left with f.

        * returns a value of the of type _T if self is not empty
        * returns None if self is empty
        * folds in FIFO Order
        """
        return self._ca.foldL(f)

    def foldR(self, f:Callable[[_T, _T], _T]) -> Optional[_T]:
        """Reduce right with f.

        * returns a value of the of type _T if self is not empty
        * returns None if self is empty
        * folds in LIFO Order
        """
        return self._ca.foldR(f)

    def foldL1(self, f:Callable[[_S, _T], _S], init: _S) -> _S:
        """Reduce Left with f starting with an initial value.

        * returns a value of the of type _S
        * type _S can be same type as _T
        * folds in FIFO Order
        """
        return self._ca.foldL1(f, init)

    def foldR1(self, f:Callable[[_S, _T], _S], init: _S) -> _S:
        """Reduce Right with f starting with an initial value.

        * returns a value of the of type _S
        * type _S can be same type as _T
        * folds in LIFO Order
        """
        return self._ca.foldR1(lambda t, s: f(s, t), init)
