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

Module implementing stateful queue data structures with amortized O(1) pushing and
popping from the queue. Obtaining length (number of elements) of a queue is an O(1)
operation. Implemented with a Python List based circular array, these data structures
will resize themselves as needed. Does not store None as a value.
"""

from __future__ import annotations

__all__ = ['FIFOQueue', 'LIFOQueue', 'DoubleQueue']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

from typing import Any
from .core.queue_base import QueueBase

class FIFOQueue(QueueBase):
    """Stateful single sided FIFO data structure. Will resize itself as needed.
    None represents the absence of a value and ignored if pushed onto an SQueue.
    """
    def __str__(self):
        return "<< " + " < ".join(map(str, self)) + " <<"

    def copy(self) -> FIFOQueue:
        """Return shallow copy of the SQueue in O(n) time & space complexity."""
        fifoqueue = FIFOQueue()
        fifoqueue._ca = self._ca.copy()
        return fifoqueue

    def push(self, *ds: Any) -> None:
        """Push data on rear of the SQueue & no return value."""
        for d in ds:
            if d != None:
                self._ca.pushR(d)

    def pop(self) -> Any:
        """Pop data off front of the SQueue."""
        return self._ca.popL()

    def peakLastIn(self) -> Any:
        """Return last element pushed to the SQueue without consuming it"""
        if self._ca:
            return self._ca[-1]
        else:
            return None

    def peakNextOut(self) -> Any:
        """Return next element ready to pop from the SQueue."""
        if self._ca:
            return self._ca[0]
        else:
            return None

class LIFOQueue(QueueBase):
    """Stateful single sided LIFO data structure. Will resize itself as needed.
    None represents the absence of a value and ignored if pushed onto an SQueue.
    """
    def __str__(self):
        return "|| " + " > ".join(map(str, self)) + " ><"

    def copy(self) -> LIFOQueue:
        """Return shallow copy of the SQueue in O(n) time & space complexity."""
        squeue = LIFOQueue()
        squeue._ca = self._ca.copy()
        return squeue

    def push(self, *ds: Any) -> None:
        """Push data on rear of the LIFOQueue & no return value."""
        for d in ds:
            if d != None:
                self._ca.pushR(d)

    def pop(self) -> Any:
        """Pop data off rear of the LIFOQueue."""
        return self._ca.popR()

    def peak(self) -> Any:
        """Return last element pushed to the LIFOQueue without consuming it"""
        if self._ca:
            return self._ca[-1]
        else:
            return None

class DoubleQueue(QueueBase):
    """Stateful double sided queue datastructure. Will resize itself as needed.
    None represents the absence of a value and ignored if pushed onto a DQueue.
    """
    def __str__(self):
        return ">< " + " | ".join(map(str, self)) + " ><"

    def copy(self) -> DoubleQueue:
        """Return shallow copy of the DQueue in O(n) time & space complexity."""
        dqueue = DoubleQueue()
        dqueue._ca = self._ca.copy()
        return dqueue

    def pushR(self, *ds: Any) -> None:
        """Push data left to right onto rear of the DQueue."""
        for d in ds:
            if d != None:
                self._ca.pushR(d)

    def pushL(self, *ds: Any) -> None:
        """Push data left to right onto front of DQueue."""
        for d in ds:
            if d != None:
                self._ca.pushL(d)

    def popR(self) -> Any:
        """Pop data off rear of the DQueue"""
        return self._ca.popR()

    def popL(self) -> Any:
        """Pop data off front of the DQueue"""
        return self._ca.popL()

    def peakR(self) -> Any:
        """Return right-most element of the DQueue if it exists."""
        if self._ca:
            return self._ca[-1]
        else:
            return None

    def peakL(self) -> Any:
        """Return left-most element of the DQueue if it exists."""
        if self._ca:
            return self._ca[0]
        else:
            return None

if __name__ == "__main__":
    pass
