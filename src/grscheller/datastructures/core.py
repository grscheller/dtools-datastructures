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

"""Core infrastructure used by grscheller.datastructures package
"""
__all__ = ['Maybe', 'MaybeMutable']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

class _Maybe:
    """
    Base class for classes representing a potentially missing value.

    = instances represent either
      - Some(value) - internally a one-tuple
      - Nothing     - internally the empty tuple () singleton
    """
    def __init__(self, value):
        if value is None:
            self._valueT = ()
        else:
            self._valueT = value,

    def __bool__(self):
        return self._valueT != ()

    def __eq__(self, other):
        return self._valueT == other._valueT

    def __repr__(self):
        if self._valueT != ():
            return 'Some(' + repr(self._valueT) + ')'
        else:
            return 'Nothing'

    def __iter__(self):
        if self:
            yield self._valueT[0]

    def get(self):
        if self:
            return self._valueT[0]
        else:
            return None

class Maybe(_Maybe):
    """
    Class representing a potentially missing value.

    - Some(value) constructed via Maybe(value)
    - Nothing constructed via Maybe(None)
    - uses immutable semantics
    """
    def __init__(self, value=None):
        super().__init__(value)

    def map(self, f):
        if self:
            return Maybe(f(self._valueT[0]))
        else:
            return Maybe()

    def flatMap(self, f):
        if self:
            return f(self._valueT[0])
        else:
            return Maybe()

class MaybeMutable(_Maybe):
    """
    Class representing a potentially missing value.

    - Some(value) constructed via Maybe(value)
    - Nothing constructed via Maybe(None)
    - uses mutable semantics
    """
    def __init__(self, value=None):
        super().__init__(value)

    def map(self, f):
        if self:
            self._valueT = f(self._valueT[0]),
        return self

    def flatMap(self, f):
        if self:
            return f(self._valueT[0])
        else:
            return self

if __name__ == "__main__":
    pass
