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

"""Functional tools

* class **Maybe**: Implements the Maybe Monad
* class **Either**: Implements a left biased Either Monad
"""
from __future__ import annotations

__all__ = [ 'Either', 'Left', 'Right',
            'Maybe', 'Some', 'Nothing',
            'maybe_to_either', 'either_to_maybe' ]
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023-2024 Geoffrey R. Scheller"
__license__ = "Apache License 2.0"

import operator
from typing import Any, Callable, Generic, Iterator, Optional, Protocol, TypeVar
from itertools import accumulate, chain
from .iterlib import exhaust, merge

_T = TypeVar('_T')
_S = TypeVar('_S')
_R = TypeVar('_R')
_P = TypeVar('_P')

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

    def get(self, alternate: Optional[_T]=None) -> Optional[_T]:
        """Get contents if they exist, otherwise return `alternate` value."""
        if self:
            return self._value
        else:
            return alternate

class Either(Generic[_T,_S]):
    """Class that either contains a `Left` value or `Right` value, but not both.

    * implements a left biased either monad
    * immutable semantics where `map` & `flatMap` return modified copies
    * in Boolean context, return `True` if a `Left,` `False` if a `Right
    * will not store a `None` as a `left` value
    """
    __slots__ = '_value', '_isLeft'

    def __init__(self, left: Optional[_T], right: Optional[_S|str]=None):
        if right is None:
            right = ''
        self._value: _T|_S|str
        if left is None:
            self._isLeft = False
            self._value = right
        else:
            self._isLeft = True
            self._value = left

    def __iter__(self) -> Iterator[_T]:
        # Yields its value if a Left of type _T.
        if self:
            yield self._value       # type: ignore # always will be an _T

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

    def get(self, default: Optional[_T]=None) -> Optional[_T]:
        """Get value if a `Left,` otherwise return `default` value."""
        if self:
            return self._value    # type: ignore
        return default

    def getRight(self) -> Optional[_S]:
        """Get value if a `Right`, otherwise return `None`."""
        if self:
            return None
        return self._value    # type: ignore

    def map(self, f: Callable[[_T], Optional[_R]], right: _P) -> Either[_R, _P]:
        """Map over a `Left(value)`."""
        if self:
            return Either(f(self._value), right)    # type: ignore
        return Either(None, right)

    def mapRight(self, g: Callable[[_S], _S]) -> Either[_T, _S]:
        """Map over a `Right(value)`."""
        if self:
            return self
        return Either(None, g(self._value))    # type: ignore

    def flatMap(self,
                f: Callable[[_T], Either[_R, _S]],
                g: Optional[Callable[[_S], _S]]=None,
                right: Optional[_S]=None) -> Either[_R, _S]:
        """flatmap a `Left` value, propagate `Right` values."""
        if g is None:
            gg = lambda x: x + right
        else:
            gg = g

        if right is None:
            if self:
                return f(self._value)                 # type: ignore
            else:
                return self                           # type: ignore
        else:
            if self:
                return f(self._value).mapRight(gg)    # type: ignore
            else:
                return self.mapRight(gg)              # type: ignore

# Convenience functions - useful as subtype constructors

def Some(value: Optional[_T]=None) -> Maybe[_T]:
    """Function for creating a `Maybe` from a `value`.
    
    * if `value` is `None` or missing, returns a `Nothing`.
    """
    return Maybe(value)

#: Nothing does not a singleton! Test via equality, or in a Boolean context.
def Nothing() -> Maybe[_T]:
    return Some(None)

def Left(left: Optional[_T], right: _S) -> Either[_T,_S]:
    """Function returns a `Left` `Either` if `left != None`, otherwise it
    returns a `Right` `Either`.
    """
    return Either(left, right)

def Right(right: _S) -> Either[_T,_S]:
    """Function to construct a `Right` `Either`."""
    return Either(None, right)

# Conversion functions

def maybe_to_either(m: Maybe[_T], right: _S) -> Either[_T,_S]:
    """Convert a `Maybe` to an `Either`."""
    return Either(m.get(), right)

def either_to_maybe(e: Either[_T,_S]) -> Maybe[_T]:
    """Convert an `Either` to a `Maybe`."""
    return Maybe(e.get())

if __name__ == "__main__":
    pass
