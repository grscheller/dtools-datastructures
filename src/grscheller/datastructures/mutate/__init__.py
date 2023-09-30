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

"""grscheller.datastructures.mutable subpackage

   Mutable version of Data structures supporting a functional sytle of programming which
   
   1. don't throw exceptions - when used syntactically properly,
   2. mutable takes on grscheller.datastructures data structures
   3. employ annotations, see PEP-649,
       - needs annotations module from __future__ package
       - useful for LSP and other external tooling
   4. return None for "non-existent" values, does not return error monads

"""
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

from .dqueue_mut import *
