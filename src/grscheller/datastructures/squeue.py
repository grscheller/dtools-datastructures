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

__all__ = ['SQueue']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

from typing import Any, Callable
from .core.queue import Queue

class SQueue(Queue):
    """Single sided queue datastructure. Will resize itself as needed.
    None represents the absence of a value and ignored if pushed onto an SQueue.
    """
    def __init__(self, *ds):
        """Construct a FIFO SQueue data structure."""
        super().__init__(*ds)

    def __repr__(self):
        """Display the SQueue showing the contained data."""
        return "<< " + " < ".join(map(repr, self)) + " <<"

    def push(self, *ds: Any) -> None:
        """Push data on rear of the SQueue & no return value."""
        for d in ds:
            if d != None:
                self._carray.pushR(d)

    def copy(self) -> SQueue:
        """Return shallow copy of the SQueue in O(n) time & space complexity."""
        squeue = SQueue()
        squeue._carray = self._carray.copy()
        return squeue

    def pop(self) -> Any:
        """Pop data off front of the SQueue."""
        if len(self._carray) > 0:
            return self._carray.popL()
        else:
            return None

    def peakLastIn(self) -> Any:
        """Return last element pushed to the SQueue without consuming it"""
        if len(self._carray) > 0:
            return self._carray[-1]
        else:
            return None

    def peakNextOut(self) -> Any:
        """Return next element ready to pop from the SQueue."""
        if len(self._carray) > 0:
            return self._carray[0]
        else:
            return None

    def map(self, f: Callable[[Any], Any]) -> None:
        """Apply function over the SQueue's contents. Suppress any None values
        returned by f.
        """
        self._carray = SQueue(*map(f, self))._carray


if __name__ == "__main__":
    pass
