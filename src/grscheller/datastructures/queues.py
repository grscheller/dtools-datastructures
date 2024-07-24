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

"""

from __future__ import annotations

__all__ = [ 'DoubleQueue', 'FIFOQueue','LIFOQueue', 'QueueBase' ]
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023-2024 Geoffrey R. Scheller"
__license__ = "Apache License 2.0"

from typing import Callable, Generic, Iterator, Optional, Self, TypeVar
from grscheller.circular_array.ca import CA
from grscheller.fp.woException import MB
from grscheller.fp.nothing import Nothing, nothing

_D = TypeVar('_D')
_S = TypeVar('_S')
_U = TypeVar('_U')
_V = TypeVar('_V')
_L = TypeVar('_L')
_R = TypeVar('_R')

class QueueBase(Generic[_D, _S]):
    """Base class for stateful queue-based data structures

    * provided to allow users to define their own queue type classes
    * primarily for DRY implementation inheritance and generics
    * each queue object "has-a" (contains) a circular array to store its data
    * initial data to initializer stored in same order as provided
    * some care is needed if storing None as a value in these data structures

    """
    __slots__ = '_ca'

    def __init__(self, *ds: _D, sentinel: _S|Nothing=nothing):
        """Construct a queue data structure.

        * data always internally stored in the same order as ds

        """
        if sentinel is nothing:
            sent1: _S = sentinel             # type: ignore # _S is Nothing
            self._ca = CA(*ds, sentinel=sent1)
        else:
            sent2: _S = sentinel             # type: ignore # is _S, not Nothing
            self._ca = CA(*ds, sentinel=sent2)



    def __repr__(self) -> str:
        if len(self) == 0:
            return type(self).__name__ + '(sentinel=' + repr(self._ca._s)+ ')'
        else:
            return type(self).__name__ + '(' + ', '.join(map(repr, self._ca)) + ', sentinel=' + repr(self._ca._s)+ ')'

    def copy(self) -> Self:
        """Return shallow copy of a QueueBase[_T] subtype."""
        return type(self)(*self._ca, sentinel=self._ca._s)

    def __bool__(self) -> bool:
        """Returns True if queue is not empty."""
        return len(self._ca) > 0

    def __len__(self) -> int:
        """Returns current number of values in queue."""
        return len(self._ca)

    def __eq__(self, other: object) -> bool:
        """Returns True if all the data stored in both compare as equal.

        * worst case is O(n) behavior for the true case.

        """
        if not isinstance(other, type(self)):
            return False
        return self._ca == other._ca

class FIFOQueue(QueueBase[_D, _S]):
    """Stateful First In First Out (FIFO) data structure.

    * will resize itself larger as needed
    * initial data pushed on in natural FIFO order

    """
    __slots__ = ()

    def __iter__(self) -> Iterator[_D]:
        """Iterator yielding data currently stored in the queue.

        * data yielded in natural FIFO order.

        """
        ca = self._ca.copy()
        for pos in range(len(ca)):
            yield ca[pos]

    def __str__(self) -> str:
        return "<< " + " < ".join(map(str, self)) + " <<"

    def map(self, f: Callable[[_D], _U]) -> FIFOQueue[_U, _S]:
        """Apply function over the contents of the FIFOQueue subtype."""
        return FIFOQueue(*map(f, self._ca), sentinel=self._ca._s)

    def push(self, *ds: _D) -> None:
        """Push data onto the FIFOQueue."""
        self._ca.pushR(*ds)

    def pop(self) -> _D|_S:
        """Pop data off front of the FIFOQueue."""
        return self._ca.popL()

    def peak_last_in(self) -> _D|_S:
        """Return last element pushed to the FIFOQueue without consuming it"""
        if self._ca:
            return self._ca[-1]
        else:
            return self._ca._s

    def peak_next_out(self) -> _D|_S:
        """Return next element ready to pop from the FIFOQueue."""
        if self._ca:
            return self._ca[0]
        else:
            return self._ca._s

    def fold(self, f:Callable[[_D, _D], _D]) -> _D|_S:
        """Reduce with f.

        * returns a value of the of type _D if self is not empty
        * otherwise returns the sentinel value of type _S
        * folds in natural FIFO Order

        """
        return self._ca.foldL(f)

    def fold1(self, f:Callable[[_L, _D], _L], start: _L) -> _L:
        """Reduce with f using a starting value.

        * returns the reduced value with an initial value
        * folds in natural FIFO Order

        """
        return self._ca.foldL1(f, init=start)

class LIFOQueue(QueueBase[_D, _S]):
    """Stateful Last In First Out (LIFO) data structure.

    * will resize itself larger as needed
    * initial data pushed on in natural LIFO order

    """
    __slots__ = ()

    def __iter__(self) -> Iterator[_D]:
        """Iterator yielding data currently stored in the queue.

        * data yielded in natural LIFO order.

        """
        ca = self._ca.copy()
        for pos in range(len(ca)-1, -1, -1):
            yield ca[pos]

    def __str__(self) -> str:
        return "|| " + " > ".join(map(str, self)) + " ><"

    def map(self, f: Callable[[_D], _U]) -> LIFOQueue[_U, _S]:
        """Apply function over the contents of the LIFOQueue."""
        return LIFOQueue(*map(f, self._ca), sentinel=self._ca._s)

    def push(self, *ds: _D) -> None:
        """Push data onto the LIFOQueue & no return value."""
        self._ca.pushR(*ds)

    def pop(self) -> _D|_S:
        """Pop data off rear of the LIFOQueue."""
        return self._ca.popR()

    def peak(self) -> _D|_S:
        """Return last element pushed to the LIFOQueue without consuming it."""
        if self._ca:
            return self._ca[-1]
        else:
            return self._ca._s

    def fold(self, f:Callable[[_D, _D], _D]) -> _D|_S:
        """Reduce with f.

        * returns a value of the of type _T if self is not empty
        * returns None if self is empty
        * folds in natural LIFO Order

        """
        return self._ca.foldR(f)

    def fold1(self, f:Callable[[_U, _D], _U], s: _U) -> _U:
        """Reduce with f.

        * always returns a value of type _S
        * type _S can be the same type as _T
        * folds in natural LIFO Order

        """
        return self._ca.foldR1(lambda s, t: f(t, s), s)

class DoubleQueue(QueueBase[_D, _S]):
    """Stateful Double Sided Queue data structure.

    * will resize itself larger as needed
    * initial data pushed on in FIFO order

    """
    __slots__ = ()

    def __iter__(self) -> Iterator[_D]:
        """Iterator yielding data currently stored in the queue.

        * data yielded in FIFO (left to right) order.

        """
        ca = self._ca.copy()
        for pos in range(len(ca)):
            yield ca[pos]

    def __str__(self) -> str:
        return ">< " + " | ".join(map(str, self)) + " ><"

    def map(self, f: Callable[[_D], _U]) -> DoubleQueue[_U]:
        """Apply function over the contents of the FIFOQueue subtype."""
        return DoubleQueue(*map(f, self._ca), sentinel=self._ca._s)

    def pushR(self, *ds: _D) -> None:
        """Push data left to right onto rear of the DoubleQueue."""
        self._ca.pushR(*ds)

    def pushL(self, *ds: _D) -> None:
        """Push data left to right onto front of DoubleQueue."""
        self._ca.pushL(*ds)

    def popR(self) -> _D|_S:
        """Pop data off rear of the DoubleQueue."""
        return self._ca.popR()

    def popL(self) -> _D|_S:
        """Pop data off front of the DoubleQueue."""
        return self._ca.popL()

    def peakR(self) -> _D|_S:
        """Return rightmost element of the DoubleQueue if it exists."""
        if self._ca:
            return self._ca[-1]
        else:
            return self._ca._s

    def peakL(self) -> Optional[_D]:
        """Return leftmost element of the DoubleQueue if it exists."""
        if self._ca:
            return self._ca[0]
        else:
            return None

    def foldL(self, f:Callable[[_D, _D], _D]) -> _D|_S:
        """Reduce Left with f.

        * returns a value of the of type _T if self is not empty
        * returns None if self is empty
        * folds in FIFO Order

        """
        return self._ca.foldL(f)

    def foldR(self, f:Callable[[_D, _D], _D]) -> _D|_S:
        """Reduce right with f.

        * returns a value of the of type _T if self is not empty
        * returns None if self is empty
        * folds in LIFO Order

        """
        return self._ca.foldR(f)

    def foldL1(self, f:Callable[[_U, _D], _U], s: _U) -> _U:
        """Reduce Left with f starting with an initial value.

        * returns a value of the of type _S
        * type _S can be same type as _T
        * folds in FIFO Order

        """
        return self._ca.foldL1(f, s)

    def foldR1(self, f:Callable[[_U, _D], _U], s: _U) -> _U:
        """Reduce Right with f starting with an initial value.

        * returns a value of the of type _S
        * type _S can be same type as _T
        * folds in LIFO Order

        """
        return self._ca.foldR1(lambda t, s: f(s, t), s)
