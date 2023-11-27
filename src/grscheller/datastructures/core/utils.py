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

"""Module grscheller.datastructure.core.utils

Utility functions for grscheller.datastructure package.
"""

from __future__ import annotations

__all__ = ['infiniteEmptyTPs']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

from typing import Any, Generator

def infiniteEmptyTPs() -> Generator[tuple[()], Any, Any]:
    while True:
        yield ()

def infiniteZeros() -> Generator[int, Any, Any]:
    while True:
        yield 0

if __name__ == "__main__":
    pass
