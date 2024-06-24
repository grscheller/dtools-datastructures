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

# TODO: Add type parameter to FP, FP_Base, FP_Map_Mutate, Either, Maybe
# TODO: Update docstrings

"""Functional tools

* class **FP**: default functional implementations for data structure methods
* class **Maybe**: Implements the Maybe Monad
* class **Either**: Implements a left biased Either Monad
"""
from __future__ import annotations

__all__ = [ 'FP', 'FP_Map_Mutate',
            'maybeToEither', 'eitherToMaybe',
            'Either', 'Left', 'Right',
            'Maybe', 'Some', 'Nothing' ]
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023-2024 Geoffrey R. Scheller"
__license__ = "Apache License 2.0"

import operator
from typing import Any, Callable, Iterator, Type
from itertools import accumulate, chain
from .iterlib import exhaust, merge

class FP_Base():
    """Default functional data structure behaviors if not overridden."""
    __slots__ = ()

    def __iter__(self) -> Iterator[Any]:
        raise NotImplementedError

    def foldL(self, f: Callable[[Any, Any], Any], initial: Any=None) -> Any:
        """Fold with an optional initial value. If an initial value is not
        given and the data structure is empty, return `None`.
        """
        if not self:
            return initial

        if initial is None:
            vs = iter(self)
        else:
            vs = chain((initial,), self)

        value = next(vs)
        for v in vs:
            value = f(value, v)
        return value

    def accummulate(self, f: Callable[[Any, Any], Any]|None=None, initial: Any=None) -> FP_Base:
        """Accumulate partial fold results in same type data structure. Works
        best for variable sized containers."""
        # May need to tell mypy I am returning a subtype of FP_Base
        # From: https://stackoverflow.com/questions/55441612/does-mypy-have-a-subclass-acceptable-return-type
        #  See: https://mypy.readthedocs.io/en/stable/kinds_of_types.html#the-type-of-class-objects
        #  For: Either errors below
        if f is None:
            f = operator.add

        if initial is None:
            return type(self)(*accumulate(self, f))
        else:
            return type(self)(*accumulate(chain((initial,), self), f))

    # Default implementations for FIFO data structures,
    # see stacks module for LIFO examples.

    def flatMap(self, f: Callable[[Any], FP_Base]) -> FP_Base:
        """Monadically bind `f` to the data structure sequentially."""
        return type(self)(*chain(*map(iter, map(f, self))))

    def mergeMap(self, f: Callable[[Any], FP_Base]) -> FP_Base:
        """Monadically bind `f` to the data structure, merge until one exhausted."""
        return type(self)(*merge(*map(iter, map(f, self))))

    def exhaustMap(self, f: Callable[[Any], FP_Base]) -> FP_Base:
        """Monadically bind `f` to the data structure, merge until all are exhausted."""
        return type(self)(*exhaust(*map(iter, map(f, self))))

class FP(FP_Base):

    def map(self, f: Callable[[Any], Any]) -> FP:
        """Apply `f` over the elements of the data structure."""
        return type(self)(*map(f, self))

class FP_Map_Mutate(FP_Base):

    def map(self, f: Callable[[Any], Any]) -> None:
        raise NotImplementedError

class Maybe(FP):
    """Class representing a potentially missing value.

    * implements the Option Monad
    * where `Maybe(value)` constructs a `Some(value)`
    * where `Maybe()` & `Maybe(None)` constructs a `Nothing`
    * immutable semantics, `map` & `flatMap` return modified copies
    * where `None` is always treated as a existence value
    * where `None` cannot be stored in an object of type `Maybe`
    * semantically `None` represent non-existence
    * when used `None` is only as an implementation detail
    """
    __slots__ = '_value',

    def __init__(self, value: Any=None):
        self._value = value

    def __iter__(self) -> Iterator[Any]:
        # Yields its value if not a Nothing
        if self:
            yield self._value

    def __repr__(self) -> str:
        if self:
            return 'Some(' + repr(self._value) + ')'
        else:
            return 'Nothing'

    def __bool__(self) -> bool:
        # Return False if `Nothing,` otherwise `True`
        return self._value is not None

    def __len__(self) -> int:
        # Length of a `Maybe` is either `0` or `1`
        if self:
            return 1
        else:
            return 0

    def __eq__(self, other: Any) -> bool:
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

    def get(self, alternate: Any=None) -> Any:
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

    def accummulate(self,
                    f: Callable[[Any, Any], Any]|None=None,
                    initial: Any=None) -> Maybe:
        """Accumulate but, since the data structure can only hold at most one value,
        do not include the initial value if the `Maybe` is not a `Nothing`.
        """
        if f is None:
            f = operator.add

        return Maybe(self.foldL(f, initial))

# Maybe convenience functions/vars

def maybeToEither(m: Maybe, right: Any=None) -> Either:
    """Convert a `Maybe` to an `Either`."""
    return Either(m.get(), right)

def Some(value: Any=None) -> Maybe:
    """Function for creating a `Maybe` from a `value`.
    If `value` is `None` or missing, returns a `Nothing`.
    """
    return Maybe(value)

#: Nothing is not a singleton! Test via equality, or in a Boolean context.
Nothing: Maybe = Maybe()

class Either(FP):
    """Class that either contains a `Left` value or `Right` value, but not both.

    * implements a left biased either monad
    * where `Maybe(value, altValue)` constructs `Left(value)` if value not None
    * where `Maybe(None, altValue)` constructs `Right(altValue)`
    * if `altValue` not given, set it to the empty string
    * immutable semantics where `map` & `flatMap` return modified copies
    * in Boolean context, return `True` if a `Left,` `False` if a `Right`
    """
    __slots__ = '_value', '_isLeft'

    def __init__(self, left: Any=None, right: Any=None):
        if right is None:
            right = ''
        if left == None:
            self._isLeft = False
            self._value = right
        else:
            self._isLeft = True
            self._value = left

    def __iter__(self) -> Iterator[Any]:
        # Yields its value if a Left.
        if self:
            yield self._value

    def __repr__(self) -> str:
        if self:
            return 'Left(' + repr(self._value) + ')'
        else:
            return 'Right(' + repr(self._value) + ')'

    def __bool__(self) -> bool:
        # Return `True` if a `Left,` `False` if a `Right`.
        return self._isLeft

    def __len__(self) -> int:
        # An `Either` always contains just one thing, which is not `None`
        return 1

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, type(self)):
            return False
        # Don't know why I need to do this? Can == return Any?
        if (self and other) or (not self and not other):
            sameValue = self._value == other._value
            if type(sameValue) == bool:
                return sameValue
            else:
                return False
        return False

    def get(self, default: Any=None) -> Any:
        """Get value if a `Left,` otherwise return `default` value."""
        if self:
            return self._value
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

def eitherToMaybe(e: Either) -> Maybe:
    """Convert an `Either` to a `Maybe`."""
    return Maybe(e.get())

def Left(left: Any, right: Any=None) -> Either:
    """Function returns a `Left` `Either` if `left != None`, otherwise it
    returns a `Right` `Either`.
    """
    return Either(left, right)

def Right(right: Any) -> Either:
    """Function to construct a `Right` `Either`."""
    return Either(None, right)

if __name__ == "__main__":
    pass
