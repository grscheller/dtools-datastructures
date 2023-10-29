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

"""Package grscheller.datastructures.core

Subpackage of grscheller.datastructures.

Data modules supporting core infrastructure of grscheller.datastructures.


- grscheller.datastructures.core.iterlib iterator module
  - functions similar to itertools and more-itertools
    - will use itertools over these since they are C language builtins
    - not using PyPI more-itertools to avoid external dependencies

- grscheller.datastructures.core.carray module implementing a circular array
  - used in the implementation of several other data structures
  - None freely stored in this data structure
  - decided to not make private because
    - could be of utility on its own
    - could be of use for users to create their own data structures
"""

__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

from .iterlib import *
from .carray import *
