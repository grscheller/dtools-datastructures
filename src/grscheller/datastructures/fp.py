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

* class **MB**: Implements the Maybe Monad
* class **XOR**: Implements a left biased Either Monad (rigid right type)
"""
from __future__ import annotations

__all__ = [ 'MB', 'XOR', 'mb_to_xor', 'xor_to_mb' ]
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023-2024 Geoffrey R. Scheller"
__license__ = "Apache License 2.0"

from abc import abstractmethod
from typing import Callable, Generic, Iterator, Optional, TypeVar

_T = TypeVar('_T')
_S = TypeVar('_S')
_L = TypeVar('_L')
_R = TypeVar('_R')

class MB(Generic[_T]):
    """Class representing a potentially missing value.

    * implements the Maybe Monad
    * where `MB(value)` contains a value of type _T
    * and `MB()` & `MB(None)` both semantically represent "Nothing"
    * above two imply `None` as a value cannot be stored in a `MB`
    * immutable, a `MB` does not change after being created
    * immutable semantics, `map` & `flatMap` never change `self`
    """
    __slots__ = '_value',

    def __init__(self, value: Optional[_T]=None):
        self._value = value

    def __iter__(self) -> Iterator[_T]:
        """Yields its value if not a "Nothing"."""
        if self._value is not None:
            yield self._value

    def __repr__(self) -> str:
        if self:
            return 'MB(' + repr(self._value) + ')'
        else:
            return 'MB()'

    def __bool__(self) -> bool:
        """Determine if the `MB` contains a value.

        * return `True` if the `MB` contains a value
        * return `False` otherwise
        """
        return self._value is not None

    def __len__(self) -> int:
        if self._value is None:
            return 0
        else:
            return 1

    def __eq__(self, other: object) -> bool:
        """Return `True` only when

        * both sides are "Nothings"
        * both sides contain values which compare as equal
        """
        if not isinstance(other, type(self)):
            return False
        return self._value == other._value

    def get(self, alt: Optional[_T]=None) -> Optional[_T]:
        """Get contents if they exist, otherwise return an alternate value."""
        if self:
            return self._value
        else:
            return alt

    def map(self, f: Callable[[_T], Optional[_S]]) -> MB[_S]:
        """Map `f` over the 0 or 1 elements of the data structure.

        * returns a new `MB` instance only if necessary
        * to help keep reference count low, will re-use self
        """
        if self._value is None:
            return self         # type: ignore # at runtime, just another "Nothing"
        return MB(f(self._value))

    def flatmap(self, f: Callable[[_T], MB[_S]]) -> MB[_S]:
        """Map `f` and flatten.

        * returns a new `MB` instance only if necessary
        * to help keep reference count low, will re-use self
        """
        if self._value is None:
            return self         # type: ignore # at runtime, just another "Nothing"
        return f(self._value)

class XOR(Generic[_L,_R]):
    """Class that either contains a "left" value or "right" value, but not both.

    * implements a left biased Either Monad
    * where `XOR(None, r: _S): XOR[_T,_S]
    * where `XOR(l: _T, None): XOR[_T,_S]
    * above two imply `None` as a value cannot be stored in a "left" `MB`
    * in Boolean context, returns `True` if a "left", `False` if a "right"
    * immutable, does not change after being created
    * immutable, an `XOR` does not change after being created
    * immutable semantics, `map` & `flatMap` never change `self`
    """
    __slots__ = '_value', '_isLeft'

    def __init__(self, left: Optional[_L], right: _R):
        self._value: _L|_R
        if left is None:
            self._isLeft = False
            self._value = right
        else:
            self._isLeft = True
            self._value = left

    def __iter__(self) -> Iterator[_L]:
        """Yields its value if a "left" XOR."""
        if self._isLeft:
            yield self._value       # type: ignore # always will be type _T

    def __repr__(self) -> str:
        if self._isLeft:
            return 'XOR(' + repr(self._value) + ')'
        else:
            return 'XOR(None, ' + repr(self._value) + ')'

    def __bool__(self) -> bool:
        """Determine if an `XOR` contains a "left" or "right" value.

        * `True` if a "left" `XOR`
        * `False` if a "right" `XOR`
        """
        return self._isLeft

    def __len__(self) -> int:
        """An `XOR` always contains just one value."""
        return 1

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return False

        if (self._isLeft and other._isLeft) or (not self._isLeft and not other._isLeft):
            return self._value == other._value
        else:
            return False

    def get(self, alt: Optional[_L]=None) -> Optional[_L]:
        """Get value if a `Left,` otherwise return `default` value."""
        if self:
            return self._value    # type: ignore
        return alt

    def getRight(self, alt: Optional[_S]=None) -> Optional[_S]:
        """Get value if a `Right`, otherwise return `None`."""
        if self:
            return alt
        return self._value    # type: ignore # returns a "right" value 

    def map(self, f: Callable[[_L], Optional[_S]], right: _R) -> XOR[_S, _R]:
        """Map over an `XOR`.

        * returns a new `XOR` instance only if necessary
        * to help keep reference count low, will re-use self
        """
        if self:
            return XOR(f(self._value), right)    # type: ignore
        return self                              # type: ignore

    def mapRight(self, g: Callable[[_R], _R]) -> XOR[_L, _R]:
        """Map over a `Right(value)`."""
        if self:
            return self
        return XOR(None, g(self._value))    # type: ignore # contains a "right" of type _R

    def flatMap(self, f: Callable[[_L], XOR[_S, _R]]) -> XOR[_S, _R]:
        """Map and flatten a `Left` value, propagate `Right` values.

        * raises TypeError if _S does not support __add__ g is `None`
        """
        if self:
            return f(self._value)    # type: ignore # f applied to a _L
        else:
            return self     # type: ignore # contains a "right" of type _R

# Conversion functions

def mb_to_xor(m: MB[_T], right: _R) -> XOR[_T, _R]:
    """Convert a `MB` to an `XOR`."""
    return XOR(m.get(), right)

def xor_to_mb(e: XOR[_T,_S]) -> MB[_T]:
    """Convert an `XOR` to a `MB`."""
    return MB(e.get())

if __name__ == "__main__":
    pass
