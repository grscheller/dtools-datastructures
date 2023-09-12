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

Module containing support classes, functions and objects used by various
datastructure implementations.
"""
__all__ = ['_NONE', 'NONE']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

class _NONE:
    """
    Class representing the absence of a value.

    - Creates surrogates for Python None.

    - A datastructure derived from _NONE represents "non-existant" values for
      a similar datastructure not derived from _NONE. Such a "NONE" type can be
      given methods that make sense in the context of a missing value for the
      similar datastrucure. Both the _NONE type and similar type should be
      derived from a common base class.

    - Should only be used to create singletons.

    - Allows the user to safely store Python None values in any of the package's
      datastructures.
    """
    def __bool__(self):
        return False

    def __eq__(self, other):
        if other is self:
            return True
        return False

    def __repr__(self):
        return 'NONE'

    def __iter__(self):
        pass

NONE = _NONE()

if __name__ == "__main__":
    pass




























