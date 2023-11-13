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

"""Module grscheller.datastructure.core.fp - functional tuples

Module implementing Functioal Programming (FP) behaviors.
"""

from __future__ import annotations

__all__ = ['FPrev']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

from typing import Any, Callable
from .fp import FP

class FPrev(FP):

    def map(self, f: Callable[[Any], Any]) -> FP:
        """Apply function over contents and use to create new instance."""
        return self._map(f)

    def flatMap(self, f: Callable[[Any], FP]) -> FP:
        """Apply function and flatten result by concatenating the results."""
        return self._flatMap(f)

    def mergeMap(self, f: Callable[[Any], FP]) -> FP:
        """Apply function and flatten result by round robin
        merging the results until first FTuple is exhauted.
        """
        return self._mergeMap(f)

    def exhaustMap(self, f: Callable[[Any], FP]) -> FP:
        """Apply function and flatten result by round robin
        merging the results until all FTuples are exhauted.
        """
        return self._exhaustMap(f)


if __name__ == "__main__":
    pass
