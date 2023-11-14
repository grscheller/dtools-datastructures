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

"""Module grscheller.datastructure.core.fp - functional tuples

Module implementing Functioal Programming (FP) behaviors.
"""

from __future__ import annotations

__all__ = ['FP', 'FP_rev']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

from typing import Any, Callable
from itertools import chain
from .iterlib import exhaust, merge

class FP():
    def __init__(self):
        pass

    def __iter__(self):
        raise NotImplementedError

    def reverse(self):
        raise NotImplementedError

    # For FIFO type data structures.
    def map(self, f: Callable[[Any], Any]) -> FP:
        return type(self)(*map(f, self))

    def flatMap(self, f: Callable[[Any], FP]) -> FP:
        return type(self)(*chain(*map(iter, map(f, self))))

    def mergeMap(self, f: Callable[[Any], FP]) -> FP:
        return type(self)(*merge(*map(iter, map(f, self))))

    def exhaustMap(self, f: Callable[[Any], FP]) -> FP:
        return type(self)(*exhaust(*map(iter, map(f, self))))


class FP_rev(FP):
    # FP modified for FILO type data structures.
    # Note: Can't just replace iter in the above with reversed which works with
    #       more concrete implemetations. Type checker (Pyright) barfs, maybe
    #       has something to do with iter() being a builtin function and
    #       reversed() being a built-in class. This is forcing me to define
    #       a reverse() method for my functional FILO classes.

    def map(self, f: Callable[[Any], Any]) -> FP:
        # return type(self)(*map(f, iter(self.reverse())))
        return type(self)(*map(f, iter(self.reverse())))

    def flatMap(self, f: Callable[[Any], FP]) -> FP:
        return type(self)(*chain(*map(iter, map(f, self.reverse())))).reverse()

    def mergeMap(self, f: Callable[[Any], FP]) -> FP:
        return type(self)(*merge(*map(iter, map(f, self.reverse())))).reverse()

    def exhaustMap(self, f: Callable[[Any], FP]) -> FP:
        return type(self)(*exhaust(*map(iter, map(f, self.reverse())))).reverse()

if __name__ == "__main__":
    pass
