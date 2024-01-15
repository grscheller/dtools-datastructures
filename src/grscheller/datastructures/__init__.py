# Copyright 2023-2024 Geoffrey R. Scheller
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

   Data structures geared to different algorithmic use cases. Supportive
   of both functional and imperative programming styles while endeavoring
   to remain Pythonic.

   The data structures in this package:

   - Allow developers to focus on the algorithms the data structures were
     designed to support.
   - Take care of all the "bit fiddling" needed to implement data structure
     behaviors, perform memory management, and deal with edge cases.
   - Mutate data structure instances safely by manipulating encapsulated
     data in protected inner scopes.
   - Iterate over inaccessible copies of internal state allowing the data
     structures to safely mutate while iterators leisurely iterate. 
   - Safely share data between multiple data structure instances by making
     shared data immutable and inaccessible to client code.
   - Don't force functional programming paradigms on client code, but
     provide functional tools to opt into.
   - Don't force exception driven code paths upon client code. Except for
     Python iterators and syntax errors, exceptions are for "exceptional"
     events.
"""
__version__ = "0.12.1"
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023-2024 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

from .arrays import PArray
from .queues import CircularArray, FIFOQueue, LIFOQueue, DoubleQueue
from .stacks import Stack, FStack
from .tuples import FTuple
from .core.fp import Maybe, Some, Nothing, Either, Left, Right
from .core.fp import maybeToEither, eitherToMaybe
from .core.iterlib import merge, exhaust
