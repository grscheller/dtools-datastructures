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

"""Package grscheller.datastructures

   Data structures supporting a functional style of programming, yet still
   endeavor to be Pythonic.
"""

# Semantic Versioning for PyPI releases:
#  - first digit signifies a major event, epoch, or paradigm shift
#  - second digit means
#    - breaking API changes
#    - major changes
#  - third digit means
#    - API additions
#    - bugfixes or minor changes
#    - documentation updates
#  - forth digit (development only)
#    - commit count
#
__version__ = "0.9.1"
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

from .functional.maybe import *
from .functional.either import *
from .functional.util import *
from .core.iterlib import *
from .core.carray import *
from .flarray import *
from .ftuple import *
from .stack import *
from .queue import *
