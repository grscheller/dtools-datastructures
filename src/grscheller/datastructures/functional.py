# Copyright 2023 Geoffrey R. Scheller
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

"""Functional Programming Library

Datastructures supporting a functional style of programming in Python.
"""
from __future__ import annotations

__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

__all__ = [
    'Maybe', 'Nothing', 'Some',
    'Either', 'Left', 'Right'
]

from typing import TypeVar, Any, Callable

T = TypeVar('T')
U = TypeVar('U')
V = TypeVar('V')

class Maybe():
    """Class representing a potentially missing value.

    - Implements the Option Monad
    - Maybe(value) constructs "Some(value)" 
    - Both Maybe() or Maybe(None) constructs a "Nothing"
    - immutable semantics - map & flatMap return modified copies
    - None is always treated as a non-existance value
      - cannot be stored in an object of type Maybe
      - semantically None does not exist
      - None only has any real existance as an implementration detail
    """
    def __init__(self, value=None):
        self._value = value

    def __bool__(self) -> bool:
        """Return false if a Nothing, otherwise true."""
        return self._value != None

    def __len__(self) -> int:
        if self:
            return 1
        return 0

    def __iter__(self):
        if self:
            yield self._value

    def __repr__(self) -> str:
        if self:
            return 'Some(' + repr(self._value) + ')'
        else:
            return 'Nothing'

    def __eq__(self, other: Maybe) -> bool:
        """Returns true if both sides are Nothings, or if both sides are Somes
        contining values which compare as equal.
        """
        if not isinstance(other, type(self)):
            return False
        return self._value == other._value

    def map(self, f: Callable[[Any], Any]) -> Maybe:
        if self:
            return Maybe(f(self._value))
        else:
            return Maybe()

    def flatMap(self, f: Callable[..., Maybe]) -> Maybe:
        if self:
            return f(self._value)
        else:
            return Maybe()

    def get(self) -> Any | None:
        """Get constents if they exist, otherwise return None. Caller is
        responsible with dealing with a None return value.
        """
        return self._value

    def getOrElse(self, default) -> Any:
        """Get constents if they exist, otherwise return provided default value,
        which is guarnteed never to be None. If the caller sets it to None,
        swap it for the empty tuple (). () was choosen since it is iterable and
        "does the right thing" in an iterable context.
        """
        if default is None:
            default = ()
        if self:
            return self._value
        else:
            return default

# Maybe convenience features. Like "unit", "Nil" or "()" in FP-languages.
# These are not necessary to ues Maybe, but gives Maybe the flavor of a Union
# type without using either inheritance or unnecessary internal state.

def Some(value=None):
    """Convenience function for creating a Maybe containing a value (unit)."""
    return Maybe(value)

"""Maybe with no value. Not a singleton. Test via equality, not identity."""
Nothing = Some()

class Either():
    """Class that either contains a Left value or Right value, but not both.

    This version is biased to the Left, which is intended as the "happy path."
    """
    def __init__(self, left, right=Nothing):
        if left == Nothing or left is None:
            self._isLeft = False
            self._value = right
        else:
            self._isLeft = True
            self._value = left

    def __bool__(self) -> bool:
        """Return true if a Left, false if a Right."""
        return self._isLeft

    def __repr__(self) -> str:
        if self:
            return 'Left(' + repr(self._value) + ')'
        else:
            return 'Right(' + repr(self._value) + ')'

    def __eq__(self, other: Either) -> bool:
        """True if both sides are same "type" and values compare as equal."""
        if not isinstance(other, type(self)):
            return False

        if (self and other) or (not self and not other):
            return self._value == other._value
        return False

    def copy(self) -> Either:
        if self:
            return Either(self._value)
        return Either(None, self._value)

    def map(self, f: Callable[[Any], Any], right=Nothing) -> Either:
        if self:
            return Either(f(self._value), right)
        return self.copy()

    def mapRight(self, g: Callable[[Any], Any]) -> Either:
        if self:
            return self.copy()
        return Either(Nothing, g(self._value))

    def flatMap(self, f: Callable[[Any], Either]) -> Either:
        if self:
            return f(self._value)
        return self.copy()

    def toMaybe(self) -> Maybe:
        if self:
            return Maybe(self._value)
        return Nothing

# Either convenience functions. Not necessary
# to use Either, but more intuitive,

def Left(left, right=Nothing) -> Either:
    return Either(left, right)

def Right(right) -> Either:
    return Either(Nothing, right)

if __name__ == "__main__":
    pass
