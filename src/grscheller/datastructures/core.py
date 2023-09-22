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

"""Core infrastructure used by grscheller.datastructures package
"""
__all__ = ['Option']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

class Option:
    """
    Class representing a potentially missing value.
    """
    # TODO: Implement class, below are holdovers from NONE implementation
    def __bool__(self):
        return False

    def __eq__(self, other):
        if other is self:
            return True
        return False

    def __repr__(self):
        return 'Option'

    def __iter__(self):
        pass

if __name__ == "__main__":
    pass
