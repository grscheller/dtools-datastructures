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

"""Module grscheller.datastructures.core.functional

Class Maybe: Implements the Maybe Monad, also called Option or Optional Monad.
Class Either: Implements a left biased Either Monad.
"""

from __future__ import annotations

__all__ = [
            'FP', 'FP_rev',
            'Either', 'Left', 'Right',
            'Maybe', 'Some', 'Nothing',
            'maybeToEither', 'eitherToMaybe'
          ]
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

from typing import Any, Callable
from itertools import chain
from .iterlib import exhaust, merge

class FP():
    def __init__(self):
        pass

    # For FIFO type data structures.
    def map(self, f: Callable[[Any], Any]) -> type[FP]:
        return type(self)(*map(f, self))

    def flatMap(self, f: Callable[[Any], FP]) -> type[FP]:
        return type(self)(*chain(*map(iter, map(f, self))))

    def mergeMap(self, f: Callable[[Any], FP]) -> type[FP]:
        return type(self)(*merge(*map(iter, map(f, self))))

    def exhaustMap(self, f: Callable[[Any], FP]) -> type[FP]:
        return type(self)(*exhaust(*map(iter, map(f, self))))

class FP_rev(FP):
    def __reversed__(self):
        raise NotImplementedError

    # FP modified for FILO type data structures.
    def map(self, f: Callable[[Any], Any]) -> type[FP_rev]:
        # return type(self)(*map(f, reversed(self)))
        return type(self)(*map(f, reversed(self)))

    def flatMap(self, f: Callable[[Any], type[FP_rev]]) -> type[FP_rev]:
        return type(self)(*chain(*map(reversed, map(f, reversed(self)))))

    def mergeMap(self, f: Callable[[Any], type[FP_rev]]) -> type[FP_rev]:
        return type(self)(*merge(*map(reversed, map(f, reversed(self)))))

    def exhaustMap(self, f: Callable[[Any], type[FP]]) -> type[FP_rev]:
        return type(self)(*exhaust(*map(reversed, map(f, reversed(self)))))

class Maybe(FP):
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
    def __init__(self, value: Any=None):
        self._value = value

    def __iter__(self):
        """Yields its value if not a Nothing"""
        if self:
            yield self._value

    def __repr__(self):
        if self:
            return 'Some(' + repr(self._value) + ')'
        else:
            return 'Nothing'

    def __bool__(self) -> bool:
        """Return false if a Nothing, otherwise true."""
        return self._value is not None

    def __len__(self) -> int:
        """A Maybe either contains something or not.

        Return 1 if a Some
        Return 0 if a Nothing
        """
        if self:
            return 1
        else:
            return 0

    def __eq__(self, other: Maybe) -> bool:
        """Returns true if both sides are Nothings, or if both sides are Somes
        contining values which compare as equal.
        """
        if not isinstance(other, type(self)):
            return False
        return self._value == other._value

    def get(self, default: Any=None) -> Any:
        """Get contents if they exist, otherwise return None. Caller is
        responsible with dealing with a None return value.
        """
        if self:
            return self._value
        else:
            return default

# Maybe convenience functions/objects.

def maybeToEither(m: Maybe, right: Any=None) -> Either:
    """Convert a Maybe to an Either"""
    return Either(m.get(), right)

def Some(value=None):
    """Function for creating a Maybe from a value. If value is None or missing,
    returns a Nothing.
    """
    return Maybe(value)

#: Maybe object representing a missing value,
#: Nothing is not a singleton. Test via equality not identity.
Nothing = Some()


class Either(FP):
    """Class that either contains a Left value or Right value, but not both. If
    right not given, set it to the empty str. This version is biased to the
    Left, which is intended as the "happy path."
    """
    def __init__(self, left: Any=None, right: Any=None):
        if right is None:
            right = ''
        if left == None:
            self._isLeft = False
            self._value = right
        else:
            self._isLeft = True
            self._value = left

    def __iter__(self):
        """Yields its value if a Left"""
        if self:
            yield self._value

    def __repr__(self):
        if self:
            return 'Left(' + repr(self._value) + ')'
        else:
            return 'Right(' + repr(self._value) + ')'

    def __bool__(self) -> bool:
        """Return true if a Left, false if a Right"""
        return self._isLeft

    def __len__(self) -> int:
        """An Either always contains just one thing, which is not None"""
        return 1

    def __eq__(self, other: Either) -> bool:
        """True if both sides are same "type" and values compare as equal"""
        if not isinstance(other, type(self)):
            return False
        if (self and other) or (not self and not other):
            return self._value == other._value
        return False

    def get(self, default: Any=None) -> Any:
        """get value if a Left, otherwise return default value."""
        if self:
            return self._value
        return default

    def map(self, f: Callable[[Any], Any], right=None) -> Either:
        if self:
            return Either(f(self._value), right)
        return self

    def mapRight(self, g: Callable[[Any], Any]) -> Either:
        """Map over if a Right."""
        if self:
            return self
        return Right(g(self._value))

    def flatMap(self, f: Callable[[Any], Either], right=None) -> Either:
        """flatMap with a Right default. Replace Right with right"""
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

    def mergeMap(self, f: Callable[[Any], Either], right=None) -> Either:
        """flatMap with a Right default. Merge right into Right via +"""
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

# Either convenience functions, act like subtype constructors.

def eitherToMaybe(e: Either) -> Maybe:
    """Convert an Either to a Maybe"""
    return Maybe(e.get())

def Left(left: Any, right: Any=None) -> Either:
    """Function returns Left Either if left != None, otherwise Right Either."""
    return Either(left, right)

def Right(right: Any) -> Either:
    """Function to construct a Right Either."""
    return Either(None, right)

if __name__ == "__main__":
    pass
