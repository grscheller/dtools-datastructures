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

"""
### Queue based datastructures.

* stateful queue data structures with amortized O(1) pushes and pops each end
* obtaining length (number of elements) of a queue is an O(1) operation
* implemented in a "has-a" relationship with a Python list based circular array
* these data structures will resize themselves as needed

"""

from __future__ import annotations

from typing import Callable, Generic, Iterator, Optional, Self, TypeVar
from typing import overload, cast
from grscheller.circular_array.ca import CA
from grscheller.fp.woException import MB

__all__ = [ 'DoubleQueue', 'FIFOQueue', 'LIFOQueue', 'QueueBase' ]

D = TypeVar('D')
S = TypeVar('S')
U = TypeVar('U')
V = TypeVar('V')
L = TypeVar('L')
R = TypeVar('R')

class QueueBase(Generic[D, S]):
    """
    #### Base class for queues

    * primarily for DRY implementation inheritance
    * each queue object "has-a" (contains) a circular array to store its data
    * len() returns the current number of elements in the queue
    * in a boolean context, returns true if not empty

    """
    __slots__ = '_ca', '_sentinel'

    def __init__(self, *ds: D, s: S):
        self._ca = CA(*ds)
        self._sentinel = s

    def __repr__(self) -> str:
        if len(self) == 0:
            return type(self).__name__ + '(s=' + repr(self._sentinel)+ ')'
        else:
            return type(self).__name__ + '(' + ', '.join(map(repr, self._ca)) + ', s=' + repr(self._sentinel)+ ')'

    def __bool__(self) -> bool:
        return len(self._ca) > 0

    def __len__(self) -> int:
        return len(self._ca)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return False
        return self._ca == other._ca

class FIFOQueue(QueueBase[D, S]):
    """
    #### FIFO Queue

    * stateful First In First Out (FIFO) data structure.
    * will resize itself larger as needed
    * initial data pushed on in natural FIFO order
    """
    __slots__ = ()

    def __iter__(self) -> Iterator[D]:
        return iter(list(self._ca))

    def copy(self) -> FIFOQueue[D, S]:
        """
        ##### FIFOQueue Copy

        Return shallow copy of the FIFOQueue.

        """
        return FIFOQueue(*self._ca, s=self._sentinel)

    def __str__(self) -> str:
        return "<< " + " < ".join(map(str, self)) + " <<"

    def push(self, *ds: D) -> None:
        """
        ##### Push Data

        Push data onto FIFOQueue. Like Python list, does not return
        a reference to itself.
        """
        self._ca.pushR(*ds)

    def pop(self) -> D|S:
        """
        ##### Pop Data

        Pop data off of FIFOQueue. Return sentinel value if queue is empty.
        """
        if self._ca:
            return self._ca.popL()
        else:
            return self._sentinel

    def peak_last_in(self) -> D|S:
        """
        ### Peak Last In

        Without consuming it, if it is still in the queue, return last element
        pushed. If queue empty, return sentinel value.
        """
        if self._ca:
            return self._ca[-1]
        else:
            return self._sentinel

    def peak_next_out(self) -> D|S:
        """
        ### Peak Next Out

        Without consuming it, if the queue is not empty, return the next item
        ready to be popped. Otherwise, return sentinel value.
        """
        if self._ca:
            return self._ca[0]
        else:
            return self._sentinel

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
        """
        ##### Fold in FIFO Order

        * reduce with `f` using an optional initial value
        * folds in natural FIFO Order (oldest to newest)
        * note that ~S can be the same type as either ~L or ~D
        * note that when an initial value is not given then ~L = ~D
        * if iterable empty & no initial value given, return a sentinel value of type ~S
        * traditional FP type order given for function f

        """
        if initial is None:
            if not self:
                return self._sentinel
        return self._ca.foldL(f, initial=initial)

    def map(self, f: Callable[[D], U]) -> FIFOQueue[U, S]:
        """
        ##### Map FIFOQueue

        Map the function `f` over the FIFOQueue, oldest to newest. Retain
        original order.

        """
        return FIFOQueue(*map(f, self._ca), s=self._sentinel)

class LIFOQueue(QueueBase[D, S]):
    """
    #### LIFO Queue

    * Last In First Out (LIFO) stateful queue data structure.
    * will resize itself larger as needed
    * initial data pushed on in natural LIFO order

    """
    __slots__ = ()

    def __iter__(self) -> Iterator[D]:
        return reversed(list(self._ca))

    def copy(self) -> LIFOQueue[D, S]:
        """
        ##### LIFOQueue Copy

        Return shallow copy of the LIFOQueue.
        """
        return LIFOQueue(*reversed(self._ca), s=self._sentinel)

    def __str__(self) -> str:
        return "|| " + " > ".join(map(str, self)) + " ><"

    def push(self, *ds: D) -> None:
        """
        ##### Push Data

        Push data on LIFOQueue. Like Python list, does not return
        a reference to itself.
        """
        self._ca.pushR(*ds)

    def pop(self) -> D|S:
        """
        ##### Pop LIFO Queue

        Pop data off of LIFOQueue. Return sentinel value if queue is empty.
        """
        if self._ca:
            return self._ca.popR()
        else:
            return self._sentinel

    def peak(self) -> D|S:
        """
        ##### Peak Next Out

        Without consuming it, if the queue is not empty, return the next item
        ready to be popped. Otherwise, return sentinel value.

        """
        if self._ca:
            return self._ca[-1]
        else:
            return self._sentinel

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
        """
        ##### Fold in LIFO Order

        * reduce with `f` using an optional initial value
        * folds in natural LIFO Order (newest to oldest)
        * note that ~S can be the same type as either ~L or ~D
        * note that when an initial value is not given then ~L = ~D
        * if iterable empty & no initial value given, return a sentinel value of type ~S
        * traditional FP type order given for function f

        """
        if initial is None:
            if not self:
                return self._sentinel
        return self._ca.foldR(f, initial=initial)

    def map(self, f: Callable[[D], U]) -> LIFOQueue[U, S]:
        """
        ##### Map LIFOQueue

        Map the function `f` over the LIFOQueue, newest to oldest. Retain
        original order.

        """
        return LIFOQueue(*reversed(CA(*map(f, reversed(self._ca)))), s=self._sentinel)

class DoubleQueue(QueueBase[D, S]):
    """
    #### Double Ended Queue

    * double ended (DQueue) stateful queue data structure.
    * will resize itself larger as needed
    * initial data pushed on in natural LIFO order

    """
    __slots__ = ()

    def __iter__(self) -> Iterator[D]:
        return iter(list(self._ca))

    def __reversed__(self) -> Iterator[D]:
        return reversed(list(self._ca))

    def __str__(self) -> str:
        return ">< " + " | ".join(map(str, self)) + " ><"

    def copy(self) -> DoubleQueue[D, S]:
        """
        ##### DoubleQueue Copy

        Return shallow copy of the DoubleQueue.

        """
        return DoubleQueue(*self._ca, s=self._sentinel)

    def pushL(self, *ds: D) -> None:
        """
        ##### Push Left

        Push data onto front (left side) of queue. Like Python list, does not
        return a reference to itself.

        """
        self._ca.pushL(*ds)

    def pushR(self, *ds: D) -> None:
        """
        ##### Push Right

        Push data onto rear (right side) of queue. Like Python list, does not
        return a reference to itself.

        """
        self._ca.pushR(*ds)

    def popL(self) -> D|S:
        """
        ##### Pop Left

        Pop data off front (left side) of DoubleQueue. Return sentinel value if
        queue is empty.

        """
        if self._ca:
            return self._ca.popL()
        else:
            return self._sentinel

    def popR(self) -> D|S:
        """
        ##### Pop Right

        Pop data off rear (right side) of DoubleQueue. Return sentinel value if
        queue is empty.

        """
        if self._ca:
            return self._ca.popR()
        else:
            return self._sentinel

    def peakL(self) -> D|S:
        """
        ##### Peak Left

        Return leftmost element of the DoubleQueue if it exists, otherwise
        return the sentinel value.

        """
        if self._ca:
            return self._ca[0]
        else:
            return self._sentinel

    def peakR(self) -> D|S:
        """
        ##### Peak Right

        Return rightmost element of the DoubleQueue if it exists, otherwise
        return the sentinel value.

        """
        if self._ca:
            return self._ca[-1]
        else:
            return self._sentinel

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
        """
        ##### Fold Left

        * reduce left with `f` using an optional initial value
        * note that ~S can be the same type as either ~L or ~D
        * note that when an initial value is not given then ~L = ~D
        * if iterable empty & no initial value given, return a sentinel value of type ~S
        * traditional FP type order given for function f
        * folds in natural FIFO Order

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
        """
        ##### Fold Right

        * reduce right with `f` using an optional initial value
        * note that ~S can be the same type as either ~R or ~D
        * note that when an initial value is not given then ~R = ~D
        * if iterable empty & no initial value given, return a sentinel value of type ~S
        * traditional FP type order given for function f
        * folds in natural FIFO Order

        """
        return self._ca.foldR(f, initial=initial)

    def map(self, f: Callable[[D], U]) -> DoubleQueue[U, S]:
        """
        ##### Map DoubleQueue

        Map the function `f` over the DoubleQueue, oldest to newest. Retain
        original order.

        """
        return DoubleQueue(*map(f, self._ca), s=self._sentinel)
