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

"""Core functions used to implement the grscheller.datastructures package"""

from __future__ import annotations
from typing import Any, Callable, Iterator

__all__ = ['concatIters', 'mergeIters', 'mapIter']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

def concatIters(*iters: Iterator[Any]) -> Iterator[Any]:
    """Sequentually concatenate multiple iterators into one"""
    for iter in iters:
        while True:
            try:
                value = next(iter)
                yield value
            except StopIteration:
                break

def mergeIters(*iters: Iterator[Any]) -> Iterator[Any]:
    """Merge multiple iterator streams until one is exhausted"""
    iterList = list(iters)
    numIters = len(iterList)
    values = []
    while True:
        try:
            values = []
            for ii in range(numIters):
                values.append(next(iterList[ii]))
            for value in values:
                yield value
        except StopIteration:
            break

def mapIter(iterator: Iterator[Any], f: Callable[[Any], Any]) -> Iterator[Any]:
    """Lazily map a function over an iterator stream"""
    # return iter([f(x) for x in iterator])
    return (f(x) for x in iterator)
