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
* these data structures will resize themselves larger as needed

##### Queue types:

* **FIFOQueue:** First-In-First-Out Queue
* **LIFOQueue:** Last-In-First-Out Queue
* **DoubleQueue:** Double-Ended Queue

"""

from __future__ import annotations

from typing import Callable, cast, Generic, Iterator, Optional, TypeVar
from grscheller.circular_array.ca import CA
from grscheller.fp.woException import MB

__all__ = [ 'DoubleQueue', 'FIFOQueue', 'LIFOQueue', 'QueueBase' ]

D = TypeVar('D')
S = TypeVar('S')
U = TypeVar('U')
V = TypeVar('V')
L = TypeVar('L')
R = TypeVar('R')

class QueueBase(Generic[D]):
    """#### Base class for circular area based queues.

    * primarily for DRY inheritance
    * implemented with a grscheller.circular-array (has-a)
    * order of initial data retained

    """
    __slots__ = '_ca'

    def __init__(self, *ds: D):
        self._ca = CA(*ds)

    def __repr__(self) -> str:
        if len(self) == 0:
            return type(self).__name__ + '()'
        else:
            return type(self).__name__ + '(' + ', '.join(map(repr, self._ca)) + ')'

    def __bool__(self) -> bool:
        return len(self._ca) > 0

    def __len__(self) -> int:
        return len(self._ca)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return False
        return self._ca == other._ca

class FIFOQueue(QueueBase[D]):
    """#### FIFO Queue

    * stateful First-In-First-Out (FIFO) data structure
    * initial data pushed on in natural FIFO order

    """
    __slots__ = ()

    def __iter__(self) -> Iterator[D]:
        return iter(list(self._ca))

    def copy(self) -> FIFOQueue[D]:
        """Return a shallow copy of the FIFOQueue."""
        return FIFOQueue(*self._ca)

    def __str__(self) -> str:
        return "<< " + " < ".join(map(str, self)) + " <<"

    def push(self, *ds: D) -> None:
        """Push data onto queue in FIFO order.

        * like a Python List, does not return a value

        """
        self._ca.pushR(*ds)

    def pop(self) -> MB[D]:
        """Pop data from queue.

        * pop item off FIFOQueue, return item in a maybe monad
        * returns an empty MB() if queue is empty

        """
        if self._ca:
            return MB(self._ca.popL())
        else:
            return MB()

    def peak_last_in(self) -> MB[D]:
        """Peak last data in.

        Return a maybe monad of the last item pushed to queue if not already
        consumed. Do not consume it.
        """
        if self._ca:
            return MB(self._ca[-1])
        else:
            return MB()

    def peak_next_out(self) -> MB[D]:
        """Peak next data out.

        Return a maybe monad of the next item to be popped from the queue.
        Do not consume it.
        """
        if self._ca:
            return MB(self._ca[0])
        else:
            return MB()

    def fold(self, f: Callable[[L, D], L], initial: Optional[L]=None) -> MB[L]:
        """Fold in FIFO Order.

        Reduce with `f` using an optional initial value.

        * folds in natural FIFO Order (oldest to newest)
        * note that when an initial value is not given then `~L = ~D`
        * if iterable empty & no initial value given, return `MB()`
        * traditional FP type order given for function `f`

        """
        if initial is None:
            if not self:
                return MB()
        return MB(self._ca.foldL(f, initial=initial))

    def map(self, f: Callable[[D], U]) -> FIFOQueue[U]:
        """Map over the queue.

        * map function `f` over the FIFOQueue
          * oldest to newest
          * retain original order
        * returns a new instance

        """
        return FIFOQueue(*map(f, self._ca))

class LIFOQueue(QueueBase[D]):
    """#### LIFO Queue

    * stateful Last-In-First-Out (LIFO) data structure
    * initial data pushed on in natural LIFO order

    """
    __slots__ = ()

    def __iter__(self) -> Iterator[D]:
        return reversed(list(self._ca))

    def copy(self) -> LIFOQueue[D]:
        """Return a shallow copy of the LIFOQueue."""
        return LIFOQueue(*reversed(self._ca))

    def __str__(self) -> str:
        return "|| " + " > ".join(map(str, self)) + " ><"

    def push(self, *ds: D) -> None:
        """Push data onto queue in LIFO order.

        * like a Python List, does not return a value

        """
        self._ca.pushR(*ds)

    def pop(self) -> MB[D]:
        """Pop data from queue.

        * pop item off of LIFOQueue, return item in a maybe monad
        * returns an empty MB() if queue is empty

        """
        if self._ca:
            return MB(self._ca.popR())
        else:
            return MB()

    def peak(self) -> MB[D]:
        """Peak next data out.

        Return a maybe monad of the next item to be popped from the queue.
        Do not consume it.
        """
        if self._ca:
            return MB(self._ca[-1])
        else:
            return MB()

    def fold(self, f: Callable[[D, R], R], initial: Optional[R]=None) -> MB[R]:
        """Fold in LIFO Order.

        Reduce with `f` using an optional initial value.

        * folds in natural LIFO Order (newest to oldest)
        * note that when an initial value is not given then `~R = ~D`
        * if iterable empty & no initial value given, return `MB()`
        * traditional FP type order given for function `f`

        """
        if initial is None:
            if not self:
                return MB()
        return MB(self._ca.foldR(f, initial=initial))

    def map(self, f: Callable[[D], U]) -> LIFOQueue[U]:
        """Map Over the queue.

        * map the function `f` over the LIFOQueue
          * newest to oldest
          * retain original order
        * returns a new instance

        """
        return LIFOQueue(*reversed(CA(*map(f, reversed(self._ca)))))

class DoubleQueue(QueueBase[D]):
    """ #### Double Ended Queue

    * stateful Double-Ended (DEQueue) data structure
    * order of initial data retained

    """
    __slots__ = ()

    def __iter__(self) -> Iterator[D]:
        return iter(list(self._ca))

    def __reversed__(self) -> Iterator[D]:
        return reversed(list(self._ca))

    def __str__(self) -> str:
        return ">< " + " | ".join(map(str, self)) + " ><"

    def copy(self) -> DoubleQueue[D]:
        """Return a shallow copy of the DoubleQueue."""
        return DoubleQueue(*self._ca)

    def pushL(self, *ds: D) -> None:
        """Push data onto left side (front) of queue.

        * like a Python List, does not return a value

        """
        self._ca.pushL(*ds)

    def pushR(self, *ds: D) -> None:
        """Push data onto right side (rear) of queue.

        * like a Python List, does not return a value

        """
        self._ca.pushR(*ds)

    def popL(self) -> MB[D]:
        """Pop Data from left side (front) of queue.

        * return left most value in a maybe monad
        * returns an empty MB() if queue is empty

        """
        if self._ca:
            return MB(self._ca.popL())
        else:
            return MB()

    def popR(self) -> MB[D]:
        """Pop Data from right side (rear) of queue.

        * return right most value in a maybe monad
        * returns an empty MB() if queue is empty

        """
        if self._ca:
            return MB(self._ca.popR())
        else:
            return MB()

    def peakL(self) -> MB[D]:
        """Peak left side of queue.

        * return left most value in a maybe monad
        * returns an empty MB() if queue is empty

        """
        if self._ca:
            return MB(self._ca[0])
        else:
            return MB()

    def peakR(self) -> MB[D]:
        """Peak right side of queue.

        * return right most value in a maybe monad
        * returns an empty MB() if queue is empty

        """
        if self._ca:
            return MB(self._ca[-1])
        else:
            return MB()

    def foldL(self, f: Callable[[L, D], L], initial: Optional[L]=None) -> MB[L]:
        """Fold Left to Right.

        Reduce left with `f` using an optional initial value.

        * note that when an initial value is not given then `~L = ~D`
        * if iterable empty & no initial value given, return `MB()`
        * traditional FP type order given for function `f`

        """
        if self._ca:
            return MB(self._ca.foldL(f, initial=initial))
        else:
            return MB()

    def foldR(self, f: Callable[[D, R], R], initial: Optional[R]=None) -> MB[R]:
        """Fold Right to Left.

        Reduce right with `f` using an optional initial value.

        * note that when an initial value is not given then `~R = ~D`
        * if iterable empty & no initial value given, return `MB()`
        * traditional FP type order given for function `f`

        """
        if self._ca:
            return MB(self._ca.foldR(f, initial=initial))
        else:
            return MB()

    def map(self, f: Callable[[D], U]) -> DoubleQueue[U]:
        """
        **Map Over DoubleQueue**

        * map the function `f` over the DoubleQueue
          * left to right
          * retain original order
        * returns a new instance

        """
        return DoubleQueue(*map(f, self._ca))
