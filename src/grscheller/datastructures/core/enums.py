# Copyright 2024 Geoffrey R. Scheller
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

"""Immutable Tuple-like data structure with a functional interfaces."""

from __future__ import annotations
from enum import auto, Enum

__all__ = ['FM', 'CONCAT', 'MERGE', 'EXHAUST']

class FM(Enum):
    CONCAT = auto()
    MERGE = auto()
    EXHAUST = auto()

CONCAT = FM.CONCAT
MERGE = FM.MERGE
EXHAUST = FM.EXHAUST
