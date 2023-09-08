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

"""_None sentinel class

   Module implementing a private sentinel value representing the absence
   of a value. Also, the parrent class of sentinel values for nonexisting
   datastructures, such as the tail of an empty List.

   This allows endusers to freely populate datastructures with Python None
   values and LSP servers not to complain about methods called on potential
   None values.
"""
__all__ = ['_None', '_none']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

class _None:
    def __init__(self, myType):
        self._type = myType

    def __repr__(self):
        return "NONE"

    def __eq__(self, other):
        return self._type is other._type

"""Sentinel value representing a missing user value"""
_none = _None(None)
