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

from grscheller.datastructures.flarray import FLArray

class TestFLArray:
    def test_default(self):
        fl1 = FLArray(default=0)
        fl2 = FLArray(default=0)
        assert fl1 == fl2
        assert fl1 is not fl2
        assert fl1
        assert fl2
        assert len(fl1) == 1
        assert len(fl2) == 1
        fl3 = fl1 + fl2
        assert fl3 == fl2 == fl3
        assert fl3 is not fl1
        assert fl3 is not fl2
        assert fl3
        assert len(fl3) == 1
        assert type(fl3) == FLArray
        fl4 = fl3.copy()
        assert fl4 == fl3
        assert fl4 is not fl3
        fl1_copy = fl1.copy()
        fl1.reverse()
        assert fl1 == fl1_copy   # only one element

        foo = 42
        baz = 'hello world'

        try:
            foo = fl1[0]
        except IndexError as err:
            print(err)
            assert False
        else:
            assert True
        finally:
            assert True
            assert foo == 0

        try:
            baz = fl2[42]
        except IndexError as err:
            print(err)
            assert True
        else:
            assert False
        finally:
            assert True
            assert baz == 'hello world'

        fl1 = FLArray(default=12)
        fl2 = FLArray(default=30)
        assert fl1 != fl2
        assert fl1
        assert fl2
        assert len(fl1) == 1
        assert len(fl2) == 1
        fl3 = fl1 + fl2
        assert fl3[0] == 42

        fl1 = FLArray()
        fl2 = FLArray(None, None, None)
        assert fl1 != fl2
        assert fl1 is not fl2
        assert not fl1
        assert not fl2
        assert len(fl1) == 1
        assert len(fl2) == 3

        fl1 = FLArray(1, 2, size=3)
        fl2 = FLArray(1, 2, None)
        assert fl1 == fl2
        assert fl1 is not fl2
        assert fl1
        assert fl2
        assert len(fl1) == 3
        assert len(fl2) == 3

        fl1 = FLArray(1, 2, size=-3)
        fl2 = FLArray(None, 1, 2)
        assert fl1 == fl2
        assert fl1 is not fl2
        assert fl1
        assert fl2
        assert len(fl1) == 3
        assert len(fl2) == 3

        fl5 = FLArray(*range(1,4), size=-5, default=42)
        assert fl5 == FLArray(42, 42, 1, 2, 3)

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

        fl4 = fl1.map(lambda x: x*x-1, mut=False)
        assert fl1 == FLArray(1,2,3,10)
        assert fl4 == FLArray(0, 3, 8, 99)
        assert fl1 is not fl4
        
        fl5 = fl2.flatMap(lambda x: FLArray(1, x, x*x+1))
        assert fl2 == FLArray(1,2,3,10)
        assert fl5 == FLArray(1, 1, 2, 1, 2, 5, 1, 3, 10, 1, 10, 101)
        assert fl5 is not fl2
        
        fl6 = fl3.mergeMap(lambda x: FLArray(1, x, x*x+1))
        assert fl3 == FLArray(1,2,3,10)
        assert fl6 == FLArray(1, 1, 1, 1, 1, 2, 3, 10, 2, 5, 10, 101)
        assert fl6 is not fl3

    def test_mapFlatMap_mutate(self):
        fl1 = FLArray(1,2,3,10)
        fl1.map(lambda x: x*x-1, mut=True)
        assert fl1 == FLArray(0, 3, 8, 99)
        
    def test_bool(self):
        fl_allNotNone = FLArray(True, 0, '')
        fl_allNone = FLArray(None, None, None)
        fl_firstNone = FLArray(None, False, [])
        fl_lastNone = FLArray(0.0, True, False, None)
        fl_someNone = FLArray(0, None, 42, None, False)
        fl_defaultNone = FLArray(default = None)
        fl_defaultNotNone = FLArray(default = False)
        assert fl_allNotNone
        assert not fl_allNone
        assert fl_firstNone
        assert fl_lastNone
        assert fl_someNone
        assert not fl_defaultNone
        assert fl_defaultNotNone

        fl_Nones = FLArray(None, size=4321)
        fl_0 = FLArray(0, 0, 0)
        fl_42s = FLArray(*([42]*42))
        fl_emptyStr = FLArray('')
        fl_hw = FLArray('hello', 'world')
        assert not fl_Nones
        assert fl_0
        assert fl_42s
        assert fl_emptyStr
        assert fl_hw

    def test_copy(self):
        fl4 = FLArray(*range(43), size = 5)
        fl42 = FLArray(*range(43), size = -5)
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
        fl = FLArray(1,2,3,4,5)
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

    def test_add(self):
        fl1 = FLArray(1,2,3)
        fl2 = FLArray(4,5,6)
        assert fl1 + fl2 == FLArray(5,7,9)
        assert fl2 + fl1 == FLArray(5,7,9)

        try:
            fl1 = FLArray(1,2,3)
            fl2 = FLArray(4,5,6,7,8,9)
            fl12 = fl1 + fl2
            fl21 = fl2 + fl1
            assert fl12 == fl21 == FLArray(5,7,9)
        except ValueError:
            assert True
        else:
            assert False

    def test_reverse(self):
        fl1 = FLArray(1, 2, 3, 'foo', 'bar')
        fl2 = FLArray('bar', 'foo', 3, 2, 1)
        assert fl1 != fl2
        fl2.reverse()
        assert fl1 == fl2
        fl1.reverse()
        assert fl1 != fl2
        assert fl1[1] == fl2[-2]

        fl4 = fl2.copy()
        fl5 = fl2.copy()
        assert fl4 == fl5
        fl4.reverse()
        fl5.reverse()
        assert fl4 != fl2
        assert fl5 != fl2
        fl2.reverse()
        assert fl4 == fl2
