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

"""Module grscheller.datastructure.ftuple - functional tuples

Module implementing an immutable tuple like object with
a funtional interface. Right now just a minimally viable product.
"""

from __future__ import annotations

__all__ = ['FTuple']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

from typing import Any, Callable
from itertools import chain
from .core.iterlib import exhaust, merge

class FTuple():
    """Class implementing tuple-like data structure with FP behaviors."""
    def __init__(self, *ds):
        """Wrap a tuple and filter out None values"""
        self._ds = tuple(filter(lambda x: x != None, ds))

    def __bool__(self):
        """Returns true if not empty"""
        return self._ds != ()

    def __len__(self) -> int:
        """Returns the number of elements in the ftuple"""
        return len(self._ds)

    def __getitem__(self, index: int) -> Any:
        # TODO: Does not like being given a slice ... research
        msg = ''
        if (cnt := len(self)) == 0:
            msg = 'Indexing an empty FTuple'
        elif not -cnt <= index < cnt:
            l = -cnt
            h = cnt - 1
            msg = f'FTuple index = {index} not between {l} and {h}'
            msg += ' while getting value'
        
        if msg:
            raise IndexError(msg)

        return self._ds[index]

    def __iter__(self):
        """Iterate over the immutable state of the FTuple"""
        for d in self._ds:
            yield d

    def __reversed__(self):
        """Reverse iterate over the immutable state of the FTuple"""
        for d in reversed(self._ds):
            yield d

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return self._ds == other._ds

    def __repr__(self):
        """Display data in the FTuple"""
        return "((" + ", ".join(map(repr, self)) + "))"

    def __add__(self, other: FTuple) -> FTuple:
        """Concatenate two FTuples"""
        ftuple = FTuple()
        ftuple._ds = self._ds + other._ds
        return ftuple

    def copy(self) -> FTuple:
        """Return shallow copy of the FTuple in O(1) time & space complexity"""
        ftuple = FTuple()
        ftuple._ds = self._ds
        return ftuple

    def reverse(self) -> FTuple:
        """Return a reversed FTuple, new instance."""
        return(FTuple(*reversed(self)))

    def map(self, f: Callable[[Any], Any]) -> FTuple:
        """Apply function over the FTuple's contents. Filter out None values."""
        return FTuple(*map(f, self))

    def flatMap(self, f: Callable[[Any], FTuple]) -> FTuple:
        """Apply function and flatten result by concatenating the results."""
        return FTuple(*chain(*map(iter, map(f, self))))

    def mergeMap(self, f: Callable[[Any], FTuple]) -> FTuple:
        """Apply function and flatten result by round robin
        merging the results until first FTuple is exhauted.
        """
        return FTuple(*merge(*map(iter, map(f, self))))

    def exhaustMap(self, f: Callable[[Any], FTuple]) -> FTuple:
        """Apply function and flatten result by round robin
        merging the results until all FTuples are exhauted.
        """
        return FTuple(*exhaust(*map(iter, map(f, self))))

if __name__ == "__main__":
    pass
