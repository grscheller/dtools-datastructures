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

from grscheller.datastructures.flarray import FLarray

class TestFPArray:
    def test_set_then_get(self):
        fl = FLarray(size=5, default=0)
        got = fl[1]
        assert got == 0
        fl[3] = set = 42
        got = fl[3]
        assert set == got

    def test_equality(self):
        fl1 = FLarray(1, 2, 'Forty-Two', (7, 11, 'foobar'))
        fl2 = FLarray(1, 3, 'Forty-Two', [1, 2, 3])
        assert fl1 != fl2
        fl2[1] = 2
        assert fl1 != fl2
        fl1[3] = fl2[3]
        assert fl1 == fl2

    def test_len_getting_indexing_padding_slicing(self):
        fl = FLarray(*range(2000))
        assert len(fl) == 2000

        fl = FLarray(*range(542), size=42)
        assert len(fl) == 42
        assert fl[0] == 0
        assert fl[41] == fl[-1] == 41
        assert fl[2] == fl[-40]

        fl = FLarray(*range(1042), size=-42)
        assert len(fl) == 42
        assert fl[0] == 1000
        assert fl[41] == 1041
        assert fl[-1] == 1041
        assert fl[41] == fl[-1] == 1041
        assert fl[1] == fl[-41] == 1001
        assert fl[0] == fl[-42]

        fl = FLarray(*[1, 'a', (1, 2)], size=5, default=42)
        assert fl[0] == 1
        assert fl[1] == 'a'
        assert fl[2] == (1, 2)
        assert fl[3] == 42
        assert fl[4] == 42
        assert fl[-1] == 42
        assert fl[-2] == 42
        assert fl[-3] == (1, 2)
        assert fl[-4] == 'a'
        assert fl[-5] == 1
        try:
            foo = fl[5] 
            print(f'should never print: {foo}')
        except IndexError:
            assert True
        except Exception as error:
            print(error)
            assert False
        else:
            assert False
        try:
            bar = fl[-6] 
            print(f'should never print: {bar}')
        except IndexError:
            assert True
        except Exception as error:
            print(error)
            assert False
        else:
            assert False

        fl = FLarray(*[1, 'a', (1, 2)], size=-6, default=42)
        assert fl[0] == 42
        assert fl[1] == 42
        assert fl[2] == 42
        assert fl[3] == 1
        assert fl[4] == 'a'
        assert fl[5] == (1, 2)
        assert fl[-1] == (1, 2)
        assert fl[-2] == 'a'
        assert fl[-3] == 1
        assert fl[-4] == 42
        assert fl[-5] == 42
        assert fl[-6] == 42
        try:
            foo = fl[6] 
            print(f'should never print: {foo}')
        except IndexError:
            assert True
        except Exception as error:
            print(error)
            assert False
        else:
            assert False
        try:
            bar = fl[-7] 
            print(f'should never print: {bar}')
        except IndexError:
            assert True
        except Exception as error:
            print(error)
            assert False
        else:
            assert False

    def test_mapFlatMap(self):
        fl1 = FLarray(1,2,3,10)
        fl2 = fl1.copy()
        fl3 = fl1.copy()

        fl4 = fl1.map(lambda x: x*x-1)
        fl4_answers = FLarray(0, 3, 8, 99)
        assert fl1 != fl4_answers
        assert fl4 == fl4_answers
        assert fl1 is not fl4
        
        fl5 = fl2.flatMap(lambda x: FLarray(1, x, x*x+1))
        fl5_answers = FLarray(1, 1, 2, 1, 2, 5, 1, 3, 10, 1, 10, 101)
        assert fl2 != fl5_answers
        assert fl5 == fl5_answers
        assert fl5 is not fl2
        
        fl6 = fl3.mergeMap(lambda x: FLarray(1, x, x*x+1))
        fl6_answers = FLarray(1, 1, 1, 1, 1, 2, 3, 10, 2, 5, 10, 101)
        assert fl3 != fl6_answers
        assert fl6 == fl6_answers
        assert fl6 is not fl3

    def test_mapFlatMap_update(self):
        fl1 = FLarray(1,2,3,10)
        fl2 = fl1.copy()
        fl3 = fl1.copy()

        fl1.map_update(lambda x: x*x-1)
        fl1_answers = FLarray(0, 3, 8, 99)
        assert fl1 == fl1_answers
        
    def test_bool(self):
        fl_allTrue = FLarray(True, True, True)
        fl_allFalse = FLarray(False, False, False)
        fl_firstTrue = FLarray(True, False, False)
        fl_lastTrue = FLarray(False, False, False, True)
        fl_someTrue = FLarray(False, True, False, True, False)
        fl_defaultTrue = FLarray(default = True)
        fl_defaultFalse = FLarray(default = False)
        assert fl_allTrue
        assert not fl_allFalse
        assert fl_firstTrue
        assert fl_lastTrue
        assert fl_someTrue
        assert fl_defaultTrue
        assert not fl_defaultFalse

        fl_None = FLarray(None)
        fl_0 = FLarray(0, 0, 0)
        fl_42 = FLarray(*([42]*42))
        fl_emptyStr = FLarray('')
        fl_hw = FLarray('hello world')
        assert not fl_None
        assert not fl_0
        assert fl_42
        assert not fl_emptyStr
        assert fl_hw

    def test_copy(self):
        fl4 = FLarray(*range(43), size = 5)
        fl42 = FLarray(*range(43), size = -5)
        fl4_copy = fl4.copy()
        fl42_copy = fl42.copy()
        assert fl4 == fl4_copy
        assert fl4 is not fl4_copy
        assert fl42 == fl42_copy
        assert fl42 is not fl42_copy
        assert fl4[0] == 0
        assert fl4[4] == fl4[-1] == 4
        assert fl42[0] == 38
        assert fl42[4] == fl42[-1] == 42

    def test_reversed_iter(self):
        """Tests that prior state of fl is used, not current one"""
        fl = FLarray(1,2,3,4,5)
        flrevIter = reversed(fl)
        aa = next(flrevIter)
        assert fl[4] == aa == 5
        fl[2] = 42
        aa = next(flrevIter)
        assert fl[3] == aa == 4
        aa = next(flrevIter)
        assert fl[2] != aa == 3
        aa = next(flrevIter)
        assert fl[1] == aa == 2
        aa = next(flrevIter)
        assert fl[0] == aa == 1

