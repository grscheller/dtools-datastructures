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

"""grscheller.datastructures package

   Data structures supporting a functional sytle of programming yet still try
   to be Pythonic
"""
#
# Semantic Versioning:
#  - first digit signifies an event or epoch
#  - second digit means breaking API changes (between PyPI releases)
#  - third digit either means
#    - API breaking changes (between GitHub commits)
#    - API additions (between PyPI releases)
#  - fourth digit either means
#    - bugfixes or minor changes (between PyPI releases)
#    - GitHub only thrashing and experimentation
#
__version__ = "0.7.2.1"
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

from .functional.maybe import *
from .functional.either import *
from .functional.util import *
from .iterlib import *
from .circle import *
from .dqueue import *
from .flArray import *
from .stack import *
from .queue import *
