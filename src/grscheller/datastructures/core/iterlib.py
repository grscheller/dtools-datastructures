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

"""Module grscheller.datastructures.core.iterlib

Library of iterator related functions.
"""

from __future__ import annotations
from typing import Any, Callable, Iterator

__all__ = ['mapIter', 'concat', 'exhaust', 'merge']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

def mapIter(iterator: Iterator[Any], f: Callable[[Any], Any]) -> Iterator[Any]:
    """Lazily map a function over an iterator stream.

    See also the map Python builtin function.
    """
    return (f(x) for x in iterator)

def concat(*iterators: Iterator[Any]) -> Iterator[Any]:
    """Sequentually concatenate multiple iterators into one.

    See also the chain function from the itertools module.
    """
    for iterator in iterators:
        while True:
            try:
                value = next(iterator)
                yield value
            except StopIteration:
                break

def merge(*iterators: Iterator[Any], yieldPartial = False) -> Iterator[Any]:
    """Merge multiple iterator streams until one is exhausted."""
    iterList = list(iterators)
    if (numIters := len(iterList)) > 0:
        values = []
        # Break when first iterator is exhausted
        while True:
            try:
                for ii in range(numIters):
                    values.append(next(iterList[ii]))
                for value in values:
                    yield value
                values.clear()
            except StopIteration:
                break
        # Yield any remaining values
        if yieldPartial:
            for value in values:
                yield value

def exhaust(*iterators: Iterator[Any], yieldPartial = True) -> Iterator[Any]:
    """Merge multiple iterator streams until all are exhausted."""
    iterList = list(iterators)
    if (numIters := len(iterList)) > 0:
        ii = 0
        values = []
        # Break when last iterator is exhausted
        while True:
            try:
                while ii < numIters:
                    values.append(next(iterList[ii]))
                    ii += 1
                for value in values:
                    yield value
                ii = 0
                values.clear()
            except StopIteration:
                numIters -= 1
                if numIters < 1:
                    break
                del iterList[ii]
        # Yield any remaining values
        if yieldPartial:
            for value in values:
                yield value
