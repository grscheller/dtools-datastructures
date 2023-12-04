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

"""Module grscheller.datastructure.clarray_base - constant length array.

Module implementing a base class for fixed length O(1) array data structures.
    
None values are not allowed in this data structures. A default iterator is used
to swap out None values .ssigned or mapped to these data structures.
"""

from __future__ import annotations

__all__ = ['CLArrayBase']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

from typing import Any, Callable,Iterator, Never, Union
from itertools import chain, cycle
from .circular_array import CircularArray

class CLArrayBase():
    """Constant Length Array

    Base class for fixed length array data structure. None values are not
    permitted to be stored to these data structure. A default iterator can be
    defined to swap out None values if stored to the CLArray. If no such
    iterator is defined, or is exhausted, the data structure defaults back to an
    infinite iterator which supplies an infinite stream of default values, the
    "default" default value is the empty tuples ().

    These data structures are guaranteed to remain a fixed length.

    So that data is not lost when imposing a fixed size upon these
    datastructures, cleaved data is pushed onto the front of the default
    iterator.

    TODO: Describe constructor values here, or figure out how to get pdoc
          to generate documentation from a constructor docstring.
    """
    def __init__(self, *ds,
                 size: int|None=None,
                 noneIter: Iterator|None=None,
                 default: Any|None=None):

        match (noneIter, default):
            case (None, None):
                self._default = ()
                self._none = cycle(((),))
            case (None, default):
                self._default = default
                self._none = cycle((default,))
            case (noneIter, None):
                self._default = ()
                self._none = chain(noneIter, cycle(((),)))
            case (noneIter, default):
                self._default = default
                self._none = chain(noneIter, cycle((default,)))

        ca = CircularArray()
        none = self._none

        for d in ds:
            if d is not None:
                ca.pushR(d)
            else:
                ca.pushR(self._default)

        ds_size = len(ca)

        # If size is None, size to the initial non-None data.
        if size is None:
            abs_size = size = ds_size
        else:
            abs_size = abs(size)

        if abs_size > ds_size:
            if size > 0:
                # pad higher indexes by iterating in default values
                for _ in range(size - ds_size):
                    ca.pushR(next(none))
            else:
                # pad lower indexes (on "left")
                for _ in range(-size - ds_size):
                    ca.pushL(next(none))
        elif abs_size < ds_size:
            # push extra data onto self._none iterator
            extra = CircularArray()
            if size > 0:
                # push final data at end
                for _ in range(ds_size - size):
                    extra.pushR(ca.popR())
            else:
                # push inital data at beginning
                for _ in range(ds_size + size):
                    extra.pushR(ca.popL())
            self._none = chain(iter(extra), none)

        self._ca = ca

    def __iter__(self):
        """Iterate over the current state of the CLArray. Copy is made
        so original source can safely mutate.
        """
        for data in self._ca.copy():
            yield data

    def __reversed__(self):
        """Reverse iterate over the current state of the CLArray. Copy is made
        so original source can safely mutate.
        """
        for data in reversed(self._ca.copy()):
            yield data

    def __repr__(self):
        # TODO: rethink this one?
        repr1 = f'{self.__class__.__name__}('
        repr2 = ', '.join(map(repr, self))
        if repr2 == '':
            repr3 = f'noneIter={self._none})'
        else:
            repr3 = f', noneIter={self._none})'
        return repr1 + repr2 + repr3

    def __str__(self):
        return '[[[' + ', '.join(map(repr, self)) + ']]]'

    def __bool__(self):
        """Return true only if there exists an array value not equal to the
        default value which eventually gets used in lieu of None. Empty arrays
        always return false. The "default" default value is the empty tuple ().
        """
        for value in self:
            if value != self._default:
                return True
        return False

    def default(self):
        """Return the default value that eventually gets used in lieu of None.
        The "default" default value is the empty tuple ().
        """
        return self._default

    def __len__(self) -> int:
        """Returns the size of the CLArray"""
        return len(self._ca)

    def __getitem__(self, index: int) -> Union[Any,Never]:
        return self._ca[index]

    def __setitem__(self, index: int, value: Any) -> Union[None,Never]:
        if value is None:
            self._ca[index] = next(self._none)
        else:
            self._ca[index] = value

    def __eq__(self, other: Any):
        """Returns True if all the data stored in both compare as equal. Worst
        case is O(n) behavior for the true case. The default value play no role
        in determining equality.
        """
        if not isinstance(other, type(self)):
            return False
        return self._ca == other._ca

    def reverse(self) -> None:
        """Swap the circular array with one with its elements reversed."""
        self._ca = self._ca.reverse()

    def mapSelf(self, f: Callable[[Any], Any]) -> None:
        """Mutate the FCLArray by appling function over the FCLArray contents."""
        self._ca = type(self)(*map(f, self),
                            noneIter=self._none,
                            default=self._default)._ca

if __name__ == "__main__":
    pass
