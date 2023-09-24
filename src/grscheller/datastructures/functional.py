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

from __future__ import annotations

"""Functional Programming Library

Datastructures supporting a functional style of programming in Python.
"""
__all__ = ['Maybe', 'Nothing', 'Some']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

from typing import Callable

class Maybe():
    """
    Class representing a potentially missing value.

    - Some(value) constructed by Maybe(value)
    - Nothing constructed either by Maybe() or Maybe(None)
    - immutable semantics - map & flatMap return modified copies
    - None is always treated as a non-existance value, can not stored
    """
    def __init__(self, value=None):
        self._value = value

    def __bool__(self) -> bool:
        return self._value != None

    def __iter__(self):
        if self:
            yield self._value

    def __repr__(self) -> str:
        if self:
            return 'Some(' + repr(self._value) + ')'
        else:
            return 'Nothing'

    def __eq__(self, other: Maybe) -> bool:
        return self._value == other._value

    def map(self, f) -> Maybe:
        if self:
            return Maybe(f(self._value))
        else:
            return Maybe()

    def flatMap(self, f: Callable[..., Maybe]) -> Maybe:
        if self:
            return f(self._value)
        else:
            return Maybe()

    def getOrElse(self, default=()):
        if self:
            return self._value
        else:
            return default

# Convenience features at like "unit" and "Nil" or "()" in FP-languages.

def Some(value=None):
    """Convenience function for creating a Maybe containing a value (unit)"""
    return Maybe(value)

"""Maybe with no value. Not a singleton. Test via equality, not identity."""
Nothing = Some()

if __name__ == "__main__":
    pass
