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

"""Module grscheller.datastructure.core.queue

Abstract base class for stateful queue type data structures. Using a Python List
based circular array for protected data storage.
"""

from __future__ import annotations

__all__ = ['Queue']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

from typing import Any, Callable
from .carray import CArray

class Queue():
    """Abstract base class for the purposes of DRY inheritance of classes
    implementing queue type data structures with a list based circular array.
    Each queue object "has-a" (contains) a circular array to store its data. The
    circular array used will resize itself as needed. Each Queue subclass must
    ensure that None values do not get pushed onto the circular array.
    """
    def __init__(self, *ds):
        """Construct a queue data structure. Cull None values."""
        self._carray = CArray()
        for d in ds:
            if d is not None:
                self._carray.pushR(d)

    def __iter__(self):
        """Iterator yielding data currently stored in queue. Data yielded in
        natural FIFO order.
        """
        cached = self._carray.copy()
        for pos in range(len(cached)):
            yield cached[pos]

    def __reversed__(self):
        """Reverse iterate over the current state of the queue."""
        cached = self._carray.copy()
        for pos in range(len(cached)-1, -1, -1):
            yield cached[pos]

    def __repr__(self):
        return f'{self.__class__.__name__}(' + ', '.join(map(repr, self)) + ')'

    def __bool__(self):
        """Returns true if queue is not empty."""
        return len(self._carray) > 0

    def __len__(self):
        """Returns current number of values in queue."""
        return len(self._carray)

    def __eq__(self, other):
        """Returns True if all the data stored in both compare as equal.
        Worst case is O(n) behavior for the true case.
        """
        if not isinstance(other, type(self)):
            return False
        return self._carray == other._carray

    def map(self, f: Callable[[Any], Any]) -> None:
        """Apply function over the DQueue's contents. Suppress any None values
        returned by f.
        """
        self._carray = Queue(*map(f, self))._carray

if __name__ == "__main__":
    pass
