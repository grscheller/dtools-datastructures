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

"""Immutable Tuple-like data structure with a functional interfaces.

Types of Tuples:

* class **FTuple**: extend builtin tuple with functional interface
"""

from __future__ import annotations

__all__ = ['FTuple']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023-2024 Geoffrey R. Scheller"
__license__ = "Apache License 2.0"

from typing import Any, Callable, Iterator, Generic, Optional, TypeVar
from itertools import accumulate
from grscheller.fp.iterators import concat, exhaust, merge

_T = TypeVar('_T')
_S = TypeVar('_S')

class FTuple(Generic[_T]):
    """Class implementing a Tuple-like object with FP behaviors."""
    __slots__ = '_tuple'

    def __init__(self, *ds: _T):
        self._tuple = tuple(ds)

    def __iter__(self) -> Iterator[_T]:
        return iter(self._tuple)

    def __reversed__(self) -> Iterator[_T]:
        return reversed(self._tuple)

    def __bool__(self) -> bool:
        return bool(len(self._tuple))

    def __len__(self) -> int:
        return len(self._tuple)

    def __repr__(self) -> str:
        return 'FTuple(' + ', '.join(map(repr, self)) + ')'

    def __str__(self) -> str:
        return "((" + ", ".join(map(repr, self)) + "))"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return False
        return self._tuple == other._tuple

    def __getitem__(self, sl: slice|int) -> FTuple[_T]|Optional[_T]:
        """Supports both indexing and slicing."""
        if isinstance(sl, slice):
            tup = self._tuple[sl]
            return FTuple(*tup)
        try:
            item = self._tuple[sl]
        except IndexError:
            item = None
        return item

    def foldL(self, f: Callable[[_T, _T], _T]) -> Optional[_T]:
        """Fold (reduce) left.

        * first argument of `f` is for the accumulated value
        * if FTuple is empty, return `None`

        """
        if len(self._tuple) == 0:
            return None

        iter_self = iter(self)
        acc = next(iter_self)

        for v in iter_self:
            acc = f(acc, v)

        return acc

    def foldR(self, f: Callable[[_T, _T], _T]) -> Optional[_T]:
        """Fold (reduce) right.

        * second argument of `f` is for the accumulated value
        * if FTuple is empty, return `None`

        """
        if len(self._tuple) == 0:
            return None

        rev_self = reversed(self)
        acc = next(rev_self)
        for v in rev_self:
            acc = f(v, acc)

        return acc

    def foldL1(self, f: Callable[[_S, _T], _S], s: _S) -> _S:
        """Fold left with an initial value.

        * first argument of `f` is for the accumulated value
        * if empty, return the initial value s

        """
        acc = s
        for v in self:
            acc = f(acc, v)
        return acc

    def foldR1(self, f: Callable[[_T, _S], _S], s: _S) -> _S:
        """Fold right with an initial value.

        * second argument of f is for the accumulated value
        * if empty, return the initial value s

        """
        acc = s
        for v in reversed(self):
            acc = f(v, acc)
        return acc

    def copy(self) -> FTuple[_T]:
        """Return shallow copy of the FTuple in O(1) time & space complexity."""
        return FTuple(*self)

    def map(self, f: Callable[[_T], _S]) -> FTuple[_S]:
        return FTuple(*map(f, self))

    def __add__(self, other: FTuple[_T]) -> FTuple[_T]:
        """Concatenate two FTuples."""
        return FTuple(*concat(iter(self), other))

    def __mul__(self, num: int) -> FTuple[_T]:
        """Return an `FTuple` which repeats another `FTuple` `num` times."""
        return FTuple(*self._tuple.__mul__(num if num > 0 else 0))

    def accummulate(self, f: Callable[[_T, _T], _T]) -> FTuple[_T]:
        """Accumulate partial fold results in an FTuple."""
        return FTuple(*accumulate(self, f))

    # def accummulate1(self, f: Callable[[_S, _T], _S], s: _S) -> FTuple[_S]:
    #     """Accumulate partial fold results in an FTuple with an initial value."""
    #     return FTuple(*accumulate(chain((s,), self), f))

    def flatMap(self, f: Callable[[_T], FTuple[_S]]) -> FTuple[_S]:
        """Monadically bind `f` to the data structure sequentially."""
        return FTuple(*concat(*map(lambda x: iter(x), map(f, self))))

    def mergeMap(self, f: Callable[[_T], FTuple[_S]]) -> FTuple[_S]:
        """Monadically bind `f` to the data structure, merge until one exhausted."""
        return FTuple(*merge(*map(lambda x: iter(x), map(f, self))))

    def exhaustMap(self, f: Callable[[_T], FTuple[_S]]) -> FTuple[_S]:
        """Monadically bind `f` to the data structure, merge until all are exhausted."""
        return FTuple(*exhaust(*map(lambda x: iter(x), map(f, self))))
