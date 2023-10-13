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

    def test_mapAndFlatMap(self):
        fl1 = FLArray(1,2,3,10)
        fl1_answers = FLArray(0, 3, 8, 99)
        assert fl1.map(lambda x: x*x-1) == fl1_answers
        fl2 = fl1.flatMap(lambda x: FLArray(1, x, x*x+1))
        fl2_answers = FLArray(1, 1, 2, 1, 2, 5, 1, 3, 10, 1, 10, 101)
        assert fl2 == fl2_answers
        fl3 = fl1.mergeMap(lambda x: FLArray(1, x, x*x+1))
        fl3_answers = FLArray(1, 1, 1, 1, 1, 2, 3, 10, 2, 5, 10, 101)
        assert fl3 == fl3_answers
