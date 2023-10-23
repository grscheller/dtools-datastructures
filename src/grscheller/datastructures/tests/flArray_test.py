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

from grscheller.datastructures.flArray import FLArray

class TestFPArray:
    def test_set_then_get(self):
        fl = FLArray(size=5, default=0)
        got = fl[1]
        assert got == 0
        fl[3] = set = 42
        got = fl[3]
        assert set == got

    def test_equality(self):
        fl1 = FLArray(1, 2, 'Forty-Two', (7, 11, 'foobar'))
        fl2 = FLArray(1, 3, 'Forty-Two', [1, 2, 3])
        assert fl1 != fl2
        fl2[1] = 2
        assert fl1 != fl2
        fl1[3] = fl2[3]
        assert fl1 == fl2

    def test_len_getting_indexing_padding_slicing(self):
        fl = FLArray(*range(2000))
        assert len(fl) == 2000

        fl = FLArray(*range(542), size=42)
        assert len(fl) == 42
        assert fl[0] == 0
        assert fl[41] == fl[-1] == 41
        assert fl[2] == fl[-40]

        fl = FLArray(*range(1042), size=-42)
        assert len(fl) == 42
        assert fl[0] == 1000
        assert fl[41] == 1041
        assert fl[-1] == 1041
        assert fl[41] == fl[-1] == 1041
        assert fl[1] == fl[-41] == 1001
        assert fl[0] == fl[-42]

        fl = FLArray(*[1, 'a', (1, 2)], size=5, default=42)
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

        fl = FLArray(*[1, 'a', (1, 2)], size=-6, default=42)
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
        fl1 = FLArray(1,2,3,10)
        fl2 = fl1.copy()
        fl3 = fl1.copy()

        fl4 = fl1.map(lambda x: x*x-1)
        fl4_answers = FLArray(0, 3, 8, 99)
        assert fl1 != fl4_answers
        assert fl4 == fl4_answers
        assert fl1 is not fl4
        
        fl5 = fl2.flatMap(lambda x: FLArray(1, x, x*x+1))
        fl5_answers = FLArray(1, 1, 2, 1, 2, 5, 1, 3, 10, 1, 10, 101)
        assert fl2 != fl5_answers
        assert fl5 == fl5_answers
        assert fl5 is not fl2
        
        fl6 = fl3.mergeMap(lambda x: FLArray(1, x, x*x+1))
        fl6_answers = FLArray(1, 1, 1, 1, 1, 2, 3, 10, 2, 5, 10, 101)
        assert fl3 != fl6_answers
        assert fl6 == fl6_answers
        assert fl6 is not fl3

    def test_mapFlatMap_update(self):
        fl1 = FLArray(1,2,3,10)
        fl2 = fl1.copy()
        fl3 = fl1.copy()

        fl1.map_update(lambda x: x*x-1)
        fl1_answers = FLArray(0, 3, 8, 99)
        assert fl1 == fl1_answers
        
        fl2.flatMap_update(lambda x: FLArray(1, x, x*x+1))
        fl2_answers = FLArray(1, 1, 2, 1, 2, 5, 1, 3, 10, 1, 10, 101)
        assert fl2 == fl2_answers
        
        fl3.mergeMap_update(lambda x: FLArray(1, x, x*x+1))
        fl3_answers = FLArray(1, 1, 1, 1, 1, 2, 3, 10, 2, 5, 10, 101)
        assert fl3 == fl3_answers

    def test_bool(self):
        flA_allTrue = FLArray(True, True, True)
        flA_allFalse = FLArray(False, False, False)
        flA_firstTrue = FLArray(True, False, False)
        flA_lastTrue = FLArray(False, False, False, True)
        flA_someTrue = FLArray(False, True, False, True, False)
        flA_defaultTrue = FLArray(default = True)
        flA_defaultFalse = FLArray(default = False)
        assert flA_allTrue
        assert not flA_allFalse
        assert flA_firstTrue
        assert flA_lastTrue
        assert flA_someTrue
        assert flA_defaultTrue
        assert not flA_defaultFalse

        flA_None = FLArray(None)
        flA_0 = FLArray(0, 0, 0)
        flA_42 = FLArray(*([42]*42))
        flA_emptyStr = FLArray('')
        flA_hw = FLArray('hello world')
        assert not flA_None
        assert not flA_0
        assert flA_42
        assert not flA_emptyStr
        assert flA_hw

    def test_copy(self):
        flA4 = FLArray(*range(43), size = 5)
        flA42 = FLArray(*range(43), size = -5)
        flA4_copy = flA4.copy()
        flA42_copy = flA42.copy()
        assert flA4 == flA4_copy
        assert flA4 is not flA4_copy
        assert flA42 == flA42_copy
        assert flA42 is not flA42_copy
        assert flA4[0] == 0
        assert flA4[4] == flA4[-1] == 4
        assert flA42[0] == 38
        assert flA42[4] == flA42[-1] == 42

    def test_reversed_iter(self):
        """Tests that prior state of flA is used, not current one"""
        flA = FLArray(1,2,3,4,5)
        flArevIter = reversed(flA)
        aa = next(flArevIter)
        assert flA[4] == aa == 5
        flA[2] = 42
        aa = next(flArevIter)
        assert flA[3] == aa == 4
        aa = next(flArevIter)
        assert flA[2] != aa == 3
        aa = next(flArevIter)
        assert flA[1] == aa == 2
        aa = next(flArevIter)
        assert flA[0] == aa == 1

