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

"""Module grscheller.datastructure.queue - queue based datastructures

Module implementing stateful FIFO data structures with amortized O(1) pushing
& popping from the queue. Obtaining length (number of elements) of a queue is
also a O(1) operation. Implemented with a Python List based circular array.
Does not store None as a value.
"""

from __future__ import annotations

__all__ = ['DQueue']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

from typing import Any, Callable
from .core.queue import Queue

class DQueue(Queue):
    """Double sided queue datastructure. Will resize itself as needed.
    None represents the absence of a value and ignored if pushed onto a DQueue.
    """
    def __init__(self, *ds):
        """Construct a FIFO/LIFO double sided queue data structure."""
        super().__init__(*ds)

    def __str__(self):
        return ">< " + " | ".join(map(str, self)) + " ><"

    def copy(self) -> DQueue:
        """Return shallow copy of the DQueue in O(n) time & space complexity."""
        dqueue = DQueue()
        dqueue._carray = self._carray.copy()
        return dqueue

    def pushR(self, *ds: Any) -> None:
        """Push data left to right onto rear of the DQueue."""
        for d in ds:
            if d != None:
                self._carray.pushR(d)

    def pushL(self, *ds: Any) -> None:
        """Push data left to right onto front of DQueue."""
        for d in ds:
            if d != None:
                self._carray.pushL(d)

    def popR(self) -> Any:
        """Pop data off rear of the DQueue"""
        if len(self._carray) > 0:
            return self._carray.popR()
        else:
            return None

    def popL(self) -> Any:
        """Pop data off front of the DQueue"""
        if len(self._carray) > 0:
            return self._carray.popL()
        else:
            return None

    def peakR(self) -> Any:
        """Return right-most element of the DQueue if it exists."""
        if len(self._carray) > 0:
            return self._carray[-1]
        else:
            return None

    def peakL(self) -> Any:
        """Return left-most element of the DQueue if it exists."""
        if len(self._carray) > 0:
            return self._carray[0]
        else:
            return None

if __name__ == "__main__":
    pass
