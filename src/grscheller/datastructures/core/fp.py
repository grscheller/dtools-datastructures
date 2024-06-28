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

# TODO: Update docstrings
# TODO: FoldR & FoldR1 consistent (short circuit-able) with infite types? 
# TODO: Get rid of FoldL & FoldR? (redundant for monoids)

"""Functional tools

* class **FP**: default functional implementations for data structure methods
* class **Maybe**: Implements the Maybe Monad
* class **Either**: Implements a left biased Either Monad
"""
from __future__ import annotations

__all__ = [ 'FP',
            'maybeToEither', 'eitherToMaybe',
            'Either', 'Left', 'Right',
            'Maybe', 'Some', 'Nothing' ]
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023-2024 Geoffrey R. Scheller"
__license__ = "Apache License 2.0"

import operator
from typing import Any, Callable, Generic, Iterator, Optional, TypeVar
from itertools import accumulate, chain
from .iterlib import exhaust, merge

_T = TypeVar('_T')
_S = TypeVar('_S')

class FP(Generic[_T]):
    """Default functional data structure behaviors if not overridden."""
    __slots__ = ()

    def __iter__(self) -> Iterator[_T]:
        raise NotImplementedError

    def __bool__(self) -> bool:
        """By convention, False when "empty", True otherwise."""
        raise NotImplementedError

    def map(self, f: Callable[[_T], _S]) -> FP[_S]:
        return type(self)(*map(f, self))

    def foldL1(self, f: Callable[[_S, _T], _S], initial: _S) -> _S:
        """Fold left with an initial value.

        * first argument of `f` is for the accumulated value
        * if empty, return the initial value

        """
        if self:
            return initial

        value: _S = initial
        for v in iter(self):
            value = f(value, v)

        return value

    def accummulate(self, f: Callable[[Any, Any], Any], initial: Any) -> FP[Any]:
        """Accumulate partial fold results in same type data structure.

        Works best for variable sized containers.

        """
        # Probably need a subtype of fp[_S]
        return type(self)(*accumulate(chain((initial,), self), f))

    # Default implementations for FIFO data structures,
    # see stacks module for LIFO examples.

    def flatMap(self, f: Callable[[Any], FP[Any]]) -> FP[Any]:
        """Monadically bind `f` to the data structure sequentially."""
        return type(self)(*chain(*map(iter, map(f, self))))

    def mergeMap(self, f: Callable[[Any], FP[Any]]) -> FP[Any]:
        """Monadically bind `f` to the data structure, merge until one exhausted."""
        return type(self)(*merge(*map(iter, map(f, self))))

    def exhaustMap(self, f: Callable[[Any], FP[Any]]) -> FP[Any]:
        """Monadically bind `f` to the data structure, merge until all are exhausted."""
        return type(self)(*exhaust(*map(iter, map(f, self))))

class Maybe(Generic[_T]):
    """Class representing a potentially missing value.

    * implements the Option Monad
    * where `Maybe(value)` constructs a `Some(value)`
    * where `Maybe()` & `Maybe(None)` constructs a `Nothing()`
    * immutable semantics, `map` & `flatMap` return modified copies
    * where `None` is always treated as a existence value
    * where `None` cannot be stored in an object of type `Maybe`
    * semantically `None` represent non-existence
    * where used, `None` is only as an implementation detail
    """
    __slots__ = '_value',

    def __init__(self, value: Optional[_T]=None):
        self._value = value

    def __iter__(self) -> Iterator[Any]:
        # Yields its value if not a Nothing
        if self:
            yield self._value

    def map(self, f: Callable[[_T], _S]) -> Maybe[_S]:
        """Apply `f` over the elements of the data structure."""
        return Maybe[_S](*map(f, self))

    def __repr__(self) -> str:
        if self:
            return 'Some(' + repr(self._value) + ')'
        else:
            return 'Nothing()'

    def __bool__(self) -> bool:
        # Return False if `Nothing,` otherwise `True`
        return self._value is not None

    def __len__(self) -> int:
        # Length of a `Maybe` is either `0` or `1`
        if self:
            return 1
        else:
            return 0

    def __eq__(self, other: object) -> bool:
        # Return `True` if both sides are of type `Nothing` or if both sides
        # are of type `Some` containing values which compare as as equal.
        if not isinstance(other, Maybe):
            return False
        # Don't know why I need to do this? Can == return Any?
        sameValue = self._value == other._value
        if type(sameValue) == bool:
            return sameValue
        else:
            return False

    def get(self, alternate: Optional[_T]=None) -> Any:
        """Get contents if they exist, otherwise return `alternate` value."""
        if self:
            return self._value
        else:
            return alternate

    def foldL(self, f: Callable[[Any, Any], Any], initial: Any=None) -> Any:
        """Left biased foldleft."""
        if self:
            if initial is None:
                return self._value
            else:
                return f(initial, self._value)
        else:
            return None

# Maybe convenience functions/vars

def maybe_to_either(m: Maybe[_T], right: _S) -> Either[_T,_S]:
    """Convert a `Maybe` to an `Either`."""
    return Either(m.get(), right)

def Some(value: Optional[_T]=None) -> Maybe[_T]:
    """Function for creating a `Maybe` from a `value`.
    
    * if `value` is `None` or missing, returns a `Nothing`.
    """
    return Maybe(value)

#: Nothing is not a singleton! Test via equality, or in a Boolean context.
def Nothing() -> Maybe[_T]:
    return Some(None)

class Either(Generic[_T,_S]):
    """Class that either contains a `Left` value or `Right` value, but not both.

    * implements a left biased either monad
    * immutable semantics where `map` & `flatMap` return modified copies
    * in Boolean context, return `True` if a `Left,` `False` if a `Right
    * will not store a `None` as a `left` value
    """
    __slots__ = '_value', '_isLeft'

    def __init__(self, left: Optional[_T], right: _S):
        self._value: _T|_S|None     # the |None should not be necessary``
        if left == None:
            self._isLeft = False
            self._value = right
        else:
            self._isLeft = True
            self._value = left

    def __iter__(self) -> Iterator[_T]:
        # Yields its value if a Left of type _T.
        if self:
            yield self._value       # type: ignore

    def __repr__(self) -> str:
        if self:
            return 'Left(' + repr(self._value) + ')'
        else:
            return 'Right(' + repr(self._value) + ')'

    def __bool__(self) -> bool:
        # Return `True` if a `Left` and `False` if a `Right`.
        return self._isLeft

    def __len__(self) -> int:
        # An `Either` always contains just one thing, which is not `None`
        return 1

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, type(self)):
            return False

        if (self and other) or (not self and not other):
            return self._value == other._value
        else:
            return False

    def get(self, default: Optional[_T]) -> Optional[_T]:
        """Get value if a `Left,` otherwise return `default` value."""
        if self:
            return self._value       # type: ignore
        return default

    def getRight(self) -> Any:
        """Get value if a `Right`, otherwise return `None`."""
        if self:
            return None
        return self._value

    def map(self, f: Callable[[Any], Any], right: Any=None) -> Either:
        """Map over a `Left(value)`."""
        if self:
            return Either(f(self._value), right)
        return self

    def mapRight(self, g: Callable[[Any], Any]) -> Either:
        """Map over a `Right(value)`."""
        if self:
            return self
        return Right(g(self._value))

    def flatMap(self, f: Callable[[Any], Either], right: Any=None) -> Either:
        """flatmap a `Left` value, but replace/override a `Right` value."""
        if self:
            if right is None:
                return f(self._value)
            else:
                return f(self._value).mapRight(lambda _: right)
        else:
            if right is None:
                return self
            else:
                return self.mapRight(lambda _: right)

    def mergeMap(self, f: Callable[[Any], Either], right: Any=None) -> Either:
        """flatMap a `Left` value, but concatenate with a `Right` value."""
        if self:
            if right is None:
                return f(self._value)
            else:
                return f(self._value).mapRight(lambda x: x + right)
        else:
            if right is None:
                return self
            else:
                return self.mapRight(lambda x: x + right)

    def foldL(self, f: Callable[[Any, Any], Any], initial: Any=None) -> Any:
        """Left biased left fold."""
        if self:
            if initial is None:
                return self._value
            else:
                return f(initial, self._value)
        else:
            return None

    def accummulate(self,
                    f: Callable[[Any, Any], Any]|None=None,
                    g: Callable[[Any, Any], Any]|None=None,
                    initial: Any=None,
                    right: Any=None) -> Either:
        """The `Either` data structure always holds one value, so what gets
        "accumulated" depends on whether the `Either` is a `Left` or a `Right`.

        * by default, a `Left` contains numeric data, a `Right` a `str`.
        """
        if f is None:
            f = operator.add
        if g is None:
            g = operator.add
        if initial is None:
            initial = 0
        if right is None:
            right = ''

        if self:
            return Left(f(initial, self._value), right)
        else:
            return Right(g(self._value, right))

# Either convenience functions. They act like subtype constructors.

def either_to_maybe(e: Either[_T,_S]) -> Maybe[_T]:
    """Convert an `Either` to a `Maybe`."""
    return Maybe(e.get())

def Left[_T,_S](left: Optional[_T], right: _S=None) -> Either[_T,_S]:
    """Function returns a `Left` `Either` if `left != None`, otherwise it
    returns a `Right` `Either`.
    """
    return Either(left, right)

def Right[_S](right: _S) -> Either[_T,_S]:
    """Function to construct a `Right` `Either`."""
    return Either(None, right)

if __name__ == "__main__":
    pass
