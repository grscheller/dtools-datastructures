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
### Functional Tuple

##### FTuple

Immutable Tuple-like data structure with a functional interfaces.

---

"""

from __future__ import annotations

from enum import auto, Enum
from typing import Callable, Iterator, Generic, Optional, TypeVar
from grscheller.fp.iterables import FM, accumulate, concat, exhaust, merge

__all__ = ['FTuple']

T = TypeVar('T')
S = TypeVar('S')

class FTuple(Generic[T]):
    """
    #### Class FTuple

    Implements a Tuple-like object with FP behaviors.

    """
    __slots__ = '_ds'

    def __init__(self, *ds: T):
        self._ds = ds

    def __iter__(self) -> Iterator[T]:
        return iter(self._ds)

    def __reversed__(self) -> Iterator[T]:
        return reversed(self._ds)

    def __bool__(self) -> bool:
        return bool(len(self._ds))

    def __len__(self) -> int:
        return len(self._ds)

    def __repr__(self) -> str:
        return 'FTuple(' + ', '.join(map(repr, self)) + ')'

    def __str__(self) -> str:
        return "((" + ", ".join(map(repr, self)) + "))"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return False
        return self._ds == other._ds

    def __getitem__(self, sl: slice|int) -> FTuple[T]|Optional[T]:
        """Supports both indexing and slicing."""
        if isinstance(sl, slice):
            return FTuple(*self._ds[sl])
        try:
            item = self._ds[sl]
        except IndexError:
            item = None
        return item

    def foldL(self, f: Callable[[S, T], S], start: Optional[S]=None, default: Optional[S]=None) -> S:
        """
        ##### Fold Left

        * fold left with an optional starting value
        * first argument of function f is for the accumulated value
        * if empty, return `start` if given, otherwise raise ValueError

        """
        it = iter(self._ds)
        if start is not None:
            acc = start
        elif not self:
            if default is None:
                msg = 'Both start and default cannot be None for an empty FTuple'
                raise ValueError('FTuple.foldL - ' + msg)
            acc = default
        else:
            acc = next(it)                # type: ignore # in this case _S == _T
        for v in it:
            acc = f(acc, v)
        return acc

    def foldR(self, f: Callable[[T, S], S], start: Optional[S]=None, default: Optional[S]=None) -> S:
        """
        ##### Fold Right

        * fold right with an optional starting value
        * second argument of function f is for the accumulated value
        * if empty, return `start` if given, otherwise raise ValueError

        """
        it = reversed(self._ds)
        if start is not None:
            acc = start
        elif not self:
            if default is None:
                msg = 'Both start and default cannot be None for an empty FTuple'
                raise ValueError('FTuple.foldR - ' + msg)
            acc = default
        else:
            acc = next(it)                # type: ignore # in this case _S == _T
        for v in it:
            acc = f(v, acc)
        return acc

    def copy(self) -> FTuple[T]:
        """
        ##### Shallow Copy

        Return shallow copy of the FTuple in O(1) time & space complexity.

        """
        return FTuple(*self)

    def map(self, f: Callable[[T], S]) -> FTuple[S]:
        return FTuple(*map(f, self))

    def __add__(self, other: FTuple[T]) -> FTuple[T]:
        """
        ##### Concatenate two FTuples

        """
        return FTuple(*concat(iter(self), other))

    def __mul__(self, num: int) -> FTuple[T]:
        """
        ##### Mult by int

        Return an FTuple which repeats another FTuple num times.

        """
        return FTuple(*self._ds.__mul__(num if num > 0 else 0))

    def accummulate(self, f: Callable[[S, T], S], s: Optional[S]=None) -> FTuple[S]:
        """
        ##### Accumulate

        Accumulate partial fold results in an FTuple with an optional starting value.

        """
        if s is None:
            return FTuple(*accumulate(self, f))
        else:
            return FTuple(*accumulate(self, f, s))

    def flatMap(self, f: Callable[[T], FTuple[S]], type: FM=FM.CONCAT) -> FTuple[S]:
        """
        ##### Bind function to FTuple

        Bind function `f` to the FTuple.

        * type = CONCAT: sequentially concatenate iterables one after the other
        * type = MERGE: merge iterables together until one is exhausted
        * type = Exhaust: merge iterables together until all are exhausted

        """
        match type:
            case FM.CONCAT:
                return FTuple(*concat(*map(lambda x: iter(x), map(f, self))))
            case FM.MERGE:
                return FTuple(*merge(*map(lambda x: iter(x), map(f, self))))
            case FM.EXHAUST:
                return FTuple(*exhaust(*map(lambda x: iter(x), map(f, self))))
            case '*':
                raise ValueError('Unknown FM type')

