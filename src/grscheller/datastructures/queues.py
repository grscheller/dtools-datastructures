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

__all__ = [ 'DoubleQueue', 'FIFOQueue', 'LIFOQueue', 'QueueBase' ]
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023-2024 Geoffrey R. Scheller"
__license__ = "Apache License 2.0"

from typing import Callable, Generic, Iterator, Optional, Self, TypeVar
from typing import overload, cast
from grscheller.circular_array.ca import CA
from grscheller.fp.nothing import Nothing, nothing
from grscheller.fp.woException import MB

D = TypeVar('D')
S = TypeVar('S')
U = TypeVar('U')
V = TypeVar('V')
L = TypeVar('L')
R = TypeVar('R')

class QueueBase(Generic[D, S]):
    """Base class for stateful queue-based data structures

    * provided to allow users to define their own queue type classes
    * primarily for DRY implementation inheritance and generics
    * each queue object "has-a" (contains) a circular array to store its data
    * initial data to initializer stored in same order as provided
    * some care is needed if storing None as a value in these data structures

    """
    __slots__ = '_ca', '_s'

    def __init__(self, *ds: D, s: S):
        """Construct a queue data structure.

        * data always internally stored in the same order as ds
        """
        self._ca = CA(*ds)
        self._s = s

    def __repr__(self) -> str:
        if len(self) == 0:
            return type(self).__name__ + '(s=' + repr(self._s)+ ')'
        else:
            return type(self).__name__ + '(' + ', '.join(map(repr, self._ca)) + ', s=' + repr(self._s)+ ')'

    def copy(self) -> Self:
        """Return shallow copy of a QueueBase[_T] subtype."""
        return type(self)(*self._ca, s=self._s)

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

class FIFOQueue(QueueBase[D, S]):
    """Stateful First In First Out (FIFO) data structure.

    * will resize itself larger as needed
    * initial data pushed on in natural FIFO order
    """
    __slots__ = ()

    def __iter__(self) -> Iterator[D]:
        """Iterator yielding data currently stored in the queue.

        * data yielded in natural FIFO order
        * copies the current state of the data to iterate over
        """
        return iter(list(self._ca))

    def __str__(self) -> str:
        return "<< " + " < ".join(map(str, self)) + " <<"

    def push(self, *ds: D) -> None:
        """Push data onto the FIFOQueue."""
        self._ca.pushR(*ds)

    def pop(self) -> D|S:
        """Pop data off the FIFOQueue."""
        if self._ca:
            return self._ca.popL()
        else:
            return self._s

    def peak_last_in(self) -> D|S:
        """Return last element pushed to the FIFOQueue without consuming it"""
        if self._ca:
            return self._ca[-1]
        else:
            return self._s

    def peak_next_out(self) -> D|S:
        """Return next element ready to pop from the FIFOQueue."""
        if self._ca:
            return self._ca[0]
        else:
            return self._s

    @overload
    def fold(self, f: Callable[[L, D], L], initial: Optional[L]) -> L|S:
        ...
    @overload
    def fold(self, f: Callable[[D, D], D]) -> D|S:
        ...
    @overload
    def fold(self, f: Callable[[L, D], L], initial: L) -> L:
        ...
    @overload
    def fold(self, f: Callable[[D, D], D], initial: D) -> D:
        ...

    def fold(self, f: Callable[[L, D], L], initial: Optional[L]=None) -> L|S:
        """Reduce with f using an optional initial value.

        * note that ~S can be the same type as ~L
        * note that when an initial value is not given then ~L = ~D
        * if iterable empty & no initial value given, return a sentinel value of type ~S
        * traditional FP type order given for function f
        * folds in natural FIFO Order
        * raises `ValueError` when called on an empty `FIFOQueue` and `initial` not given

        """
        if initial is None:
            if not self:
                return self._s
        return self._ca.foldL(f, initial=initial)

    def map(self, f: Callable[[D], U]) -> FIFOQueue[U, S]:
        """Apply function over the contents of the FIFOQueue."""
        return FIFOQueue(*map(f, self._ca), s=self._s)

class LIFOQueue(QueueBase[D, S]):
    """Stateful Last In First Out (LIFO) data structure.

    * will resize itself larger as needed
    * initial data pushed on in natural LIFO order
    """
    __slots__ = ()

    def __iter__(self) -> Iterator[D]:
        """Iterator yielding data currently stored in the queue.

        * data yielded in natural LIFO order
        * copies the current state of the data to iterate over
        """
        return reversed(list(self._ca))

    def __str__(self) -> str:
        return "|| " + " > ".join(map(str, self)) + " ><"

    def push(self, *ds: D) -> None:
        """Push data onto the LIFOQueue & no return value."""
        self._ca.pushR(*ds)

    def pop(self) -> D|S:
        """Pop data off the LIFOQueue."""
        if self._ca:
            return self._ca.popR()
        else:
            return self._s

    def peak(self) -> D|S:
        """Return last element pushed to the LIFOQueue without consuming it."""
        if self._ca:
            return self._ca[-1]
        else:
            return self._s

    @overload
    def fold(self, f: Callable[[D, R], R], initial: Optional[R]) -> R|S:
        ...
    @overload
    def fold(self, f: Callable[[D, D], D]) -> D|S:
        ...
    @overload
    def fold(self, f: Callable[[D, R], R], initial: R) -> R:
        ...
    @overload
    def fold(self, f: Callable[[D, D], D], initial: D) -> D:
        ...

    def fold(self, f: Callable[[D, R], R], initial: Optional[R]=None) -> R|S:
        """Reduce with f using an optional initial value.

        * note that ~S can be the same type as ~L
        * note that when an initial value is not given then ~L = ~D
        * if iterable empty & no initial value given, return a sentinel value of type ~S
        * traditional FP type order given for function f
        * folds in natural FIFO Order
        * raises `ValueError` when called on an empty `LIFOQueue` and `initial` not given
        """
        if initial is None:
            if not self:
                return self._s
        return self._ca.foldR(f, initial=initial)

    def map(self, f: Callable[[D], U]) -> LIFOQueue[U, S]:
        """Apply function over the contents of the FIFOQueue."""
        return LIFOQueue(*map(f, self._ca), s=self._s)

class DoubleQueue(QueueBase[D, S]):
    """Stateful Double Sided Queue data structure.

    * will resize itself larger as needed
    * initial data pushed on in FIFO order
    """
    __slots__ = ()

    def __iter__(self) -> Iterator[D]:
        """Iterator yielding data currently stored in the queue.

        * data yielded in left to right order.
        """
        return iter(list(self._ca))

    def __reversed__(self) -> Iterator[D]:
        """Reversed iterator yielding data currently stored in the queue.

        * data yielded in right-to-left) order.
        """
        return reversed(list(self._ca))

    def __str__(self) -> str:
        return ">< " + " | ".join(map(str, self)) + " ><"

    def pushL(self, *ds: D) -> None:
        """Push data onto left side of DoubleQueue."""
        self._ca.pushL(*ds)

    def pushR(self, *ds: D) -> None:
        """Push data onto right side of the DoubleQueue."""
        self._ca.pushR(*ds)

    def popL(self) -> D|S:
        """Pop data off left side of DoubleQueue."""
        if self._ca:
            return self._ca.popL()
        else:
            return self._s

    def popR(self) -> D|S:
        """Pop data off right side of DoubleQueue."""
        if self._ca:
            return self._ca.popR()
        else:
            return self._s

    def peakL(self) -> D|S:
        """Return leftmost element of the DoubleQueue if it exists."""
        if self._ca:
            return self._ca[0]
        else:
            return self._s

    def peakR(self) -> D|S:
        """Return rightmost element of the DoubleQueue if it exists."""
        if self._ca:
            return self._ca[-1]
        else:
            return self._s

    @overload
    def foldL(self, f: Callable[[L, D], L], initial: Optional[L]) -> L|S:
        ...
    @overload
    def foldL(self, f: Callable[[D, D], D]) -> D|S:
        ...
    @overload
    def foldL(self, f: Callable[[L, D], L], initial: L) -> L:
        ...
    @overload
    def foldL(self, f: Callable[[D, D], D], initial: D) -> D:
        ...

    def foldL(self, f: Callable[[L, D], L], initial: Optional[L]=None) -> L|S:
        """Reduce with f using an optional initial value.

        * note that ~S can be the same type as ~L
        * note that when an initial value is not given then ~L = ~D
        * if iterable empty & no initial value given, return a sentinel value of type ~S
        * traditional FP type order given for function f
        * folds in natural FIFO Order
        * raises `ValueError` when called on an empty `DoubleQueue` and `initial` not given
        """
        return self._ca.foldL(f, initial=initial)

    @overload
    def foldR(self, f: Callable[[D, R], R], initial: Optional[R]) -> R|S:
        ...
    @overload
    def foldR(self, f: Callable[[D, D], D]) -> D|S:
        ...
    @overload
    def foldR(self, f: Callable[[D, R], R], initial: R) -> R:
        ...
    @overload
    def foldR(self, f: Callable[[D, D], D], initial: D) -> D:
        ...

    def foldR(self, f: Callable[[D, R], R], initial: Optional[R]=None) -> R|S:
        """Reduce with f using an optional initial value.

        * note that ~S can be the same type as ~L
        * note that when an initial value is not given then ~L = ~D
        * if iterable empty & no initial value given, return a sentinel value of type ~S
        * traditional FP type order given for function f
        * folds in natural FIFO Order
        * raises `ValueError` when called on an empty `DoubleQueue` and `initial` not given
        """
        return self._ca.foldR(f, initial=initial)

    def map(self, f: Callable[[D], U]) -> DoubleQueue[U, S]:
        """Apply function over the contents of the FIFOQueue."""
        return DoubleQueue(*map(f, self._ca), s=self._s)
