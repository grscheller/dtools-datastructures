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

__version__ = "0.10.13.2"
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

from .core.fp import Maybe, Some, Nothing
from .core.fp import Either, Left, Right
from .core.fp import maybeToEither, eitherToMaybe
from .core.iterlib import merge, exhaust
from .clarray import CLArray
from .dqueue import DQueue
from .squeue import SQueue
from .stack import Stack
from .fclarray import FCLArray
from .fstack import FStack
from .ftuple import FTuple
