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

"""Module grscheller.datastructure.clarray - constant length array.

Module implementing an mutable fixed length data structure with O(1) data
access. All mutating methods are guaranteed not to change the length of the
data structure.

None values are not allowed in this data structures. An immutable default value                     
is set upon instantiating. If no default value is given, the empty tuple () is
used in lieu of None, but is not set as the default value. Method which return
new CLArray values can set a different default value for the new instance.
"""

from __future__ import annotations

__all__ = ['CLArray']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

from typing import Any, Callable, Iterator, Never, Union
from itertools import chain, cycle
from .core.circular_array import CircularArray
from .core.iterlib import merge, exhaust
from .core.fp import FP

class CLArray(FP):
    """Functional Constant Length Array

    Class implementing a mutable fixed length array data structure whose
    mutaing methods are guaranteed not to change the length of the data
    structure.

    If size set to None, size to data provided.
    If size > 0, pad data on right with default value or slice off trailing data.
    If size < 0, pad data on left with default value or slice off initial data.

    Does not permits storing None as a value. If a default value is not set, the
    empty tuple () is used in lieu of None, but () is not set as the default
    value.
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
        """Mutate the CLArray by appling function over the CLArray contents."""
        self._ca = CLArray(*map(f, self),
                            noneIter=self._none,
                            default=self._default)._ca

    def __str__(self):
        return '[|' + ', '.join(map(repr, self)) + '|]'

    def copy(self,
             size: int|None=None,
             noneIter: Iterator|None=None,
             default: Any|None=None) -> CLArray:
        """Return shallow copy of the CLArray in O(n) complexity."""
        return self.map(lambda x: x, size, noneIter, default)

    def map(self, f: Callable[[Any], Any], size: int|None=None,
            noneIter: Iterator|None=None, default: Any|None=None) -> CLArray:
        """Apply function f over the CLArray contents. Return a new CLArray
        with the mapped contents. Size to the data unless size is given. If
        noneIter is not given, use default to create the none iterator. If
        default is not given, use the value from the CLArray being mapped.
        """
        match (noneIter, default):
            case (None, None):
                default = self._default
                noneIter = cycle((default,))
            case (None, default):
                noneIter = cycle((default,))
            case (noneIter, None):
                # Careful: noneIter might be infinite!
                default = self._default

        if size is None:
            return CLArray(*map(f, self), noneIter=noneIter, default=default)
        else:
            return CLArray(*map(f, self), size=size, noneIter=noneIter, default=default)

    def flatMap(self, f: Callable[[Any], CLArray],
                size: int|None=None,
                noneIter: Iterator|None=None,
                default: Any|None=None) -> CLArray:
        """Map f across self and flatten result by concatenating the CLArray
        elements generated by f. If a default value is not given, use the
        default value of the FLArray being flatMapped if it has been set,
        otherwise leave it unset.

        Note: Any default values of the FLArrays created by f need not have
        anything to do with the default value of the FPArray being flat mapped
        over.
        """
        if (noneIter, default) == (None, None):
            default = self._default

        return CLArray(
            *chain(*self.map(f)), size=size, noneIter=noneIter, default=default
        )

    def mergeMap(self, f: Callable[[Any], CLArray],
                 size: int|None=None,
                 noneIter: Iterator|None=None,
                 default: Any|None=None) -> CLArray:
        """Map f across self and flatten result by merging the CLArray elements
        generated by f until the first is exhausted. If a default value is not
        given, use the default value of the FLArray being flatMapped if it has
        been set, otherwise leave it unset.
        """
        if (noneIter, default) == (None, None):
            noneIter = self._none

        return CLArray(
            *merge(*self.map(f)), size=size, noneIter=noneIter, default=default
        )

    def exhastMap(self, f: Callable[[Any], CLArray],
                  size: int|None=None,
                  noneIter: Iterator|None=None,
                  default: Any|None=None) -> CLArray:
        """Map f across self and flatten result by merging the CLArray elements
        generated by f until all are exhausted. If a default value is not given,
        use the default value of the FLArray being flatMapped if it has been
        set, otherwise leave it unset.
        """
        if (noneIter, default) == (None, None):
            noneIter = self._none

        return CLArray(
            *exhaust(*self.map(f)), size=size, noneIter=noneIter, default=default
        )

if __name__ == "__main__":
    pass
