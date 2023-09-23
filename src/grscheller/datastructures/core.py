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
__all__ = ['Maybe']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

class Maybe():
    """
    Class representing a potentially missing value.

    - Some(value) constructed via Maybe(value)
    - Nothing constructed via Maybe() or Maybe(None)
    - uses immutable semantics
    """
    def __init__(self, value=None):
        self._value = value

    def __bool__(self):
        return self._value != None

    def __eq__(self, other):
        return self._value == other._value

    def __repr__(self):
        if self:
            return 'Some(' + repr(self._value) + ')'
        else:
            return 'Nothing'

    def __iter__(self):
        if self:
            yield self._value

    def map(self, f):
        if self:
            return Maybe(f(self._value))
        else:
            return Maybe()

    def flatMap(self, f):
        if self:
            return f(self._value)
        else:
            return Maybe()

    def get(self):
        return self._value

    def getOrElse(self, default):
        if self:
            return self._value
        else:
            return default

if __name__ == "__main__":
    pass
