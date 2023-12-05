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

from typing import Any
from .core.queue_base import QueueBase

class SQueue(QueueBase):
    """Single sided queue datastructure. Will resize itself as needed.
    None represents the absence of a value and ignored if pushed onto an SQueue.
    """
    def __str__(self):
        return "<< " + " < ".join(map(str, self)) + " <<"

    def copy(self) -> SQueue:
        """Return shallow copy of the SQueue in O(n) time & space complexity."""
        squeue = SQueue()
        squeue._ca = self._ca.copy()
        return squeue

    def push(self, *ds: Any) -> None:
        """Push data on rear of the SQueue & no return value."""
        for d in ds:
            if d != None:
                self._ca.pushR(d)

    def pop(self) -> Any:
        """Pop data off front of the SQueue."""
        if len(self._ca) > 0:
            return self._ca.popL()
        else:
            return None

    def peakLastIn(self) -> Any:
        """Return last element pushed to the SQueue without consuming it"""
        if len(self._ca) > 0:
            return self._ca[-1]
        else:
            return None

    def peakNextOut(self) -> Any:
        """Return next element ready to pop from the SQueue."""
        if len(self._ca) > 0:
            return self._ca[0]
        else:
            return None

if __name__ == "__main__":
    pass
