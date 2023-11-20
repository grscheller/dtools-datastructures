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

from grscheller.datastructures.fclarray import FCLArray

class TestFCLArray:
    def test_mapSelf(self):
        cl1 = FCLArray(0, 1, 2, 3, 4)
        cl1[2] = cl1[4]
        assert cl1[0] == 0
        assert cl1[1] == 1
        assert cl1[2] == 4
        assert cl1[3] == 3
        assert cl1[4] == 4
        ret = cl1.mapSelf(lambda x: x*x)
        assert ret == None
        ret = cl1.reverse()
        assert ret == None
        assert cl1[0] == 16
        assert cl1[1] == 9
        assert cl1[2] == 16
        assert cl1[3] == 1
        assert cl1[4] == 0

    def test_map1(self):
        cl1 = FCLArray(0, 1, 2, 3, size=-6, default=-1)
        cl2 = cl1.map(lambda x: x+1, size=7, default=42)
        assert cl1[0] + 1 == cl2[0] == 0
        assert cl1[1] + 1 == cl2[1] == 0
        assert cl1[2] + 1 == cl2[2] == 1
        assert cl1[3] + 1 == cl2[3] == 2
        assert cl1[4] + 1 == cl2[4] == 3
        assert cl1[5] + 1 == cl2[5] == 4
        assert cl2[6] == 42

    def test_map2(self):
        cl1 = FCLArray(0, 1, 2, 3, size=6, default=-1)
        cl2 = cl1.map(lambda x: x+1)
        assert cl1[0] + 1 == cl2[0] == 1
        assert cl1[1] + 1 == cl2[1] == 2
        assert cl1[2] + 1 == cl2[2] == 3
        assert cl1[3] + 1 == cl2[3] == 4
        assert cl1[4] + 1 == cl2[4] == 0
        assert cl1[5] + 1 == cl2[5] == 0

    def test_map3(self):
        cl1 = FCLArray(1, 2, 3, 10)

        cl2 = cl1.map(lambda x: x*x-1)
        assert cl2 is not None
        assert cl1 is not cl2
        assert cl1 == FCLArray(1, 2, 3, 10)
        assert cl2 == FCLArray(0, 3, 8, 99)
        
        ret = cl1.mapSelf(lambda x: x*x-1)
        assert ret is None
        assert cl1 == FCLArray(0, 3, 8, 99)
        
    def test_default(self):
        cl1 = FCLArray(size=1, default=1)
        cl2 = FCLArray(size=1, default=2)
        assert cl1 != cl2
        assert cl1[0] == 1
        assert cl2[0] == 2
        assert not cl1
        assert not cl2
        assert len(cl1) == 1
        assert len(cl2) == 1
        cl3 = cl1 + cl2
        assert cl3[0] == 1
        assert cl3[1] == 2
        assert len(cl3) == 2
        assert cl3
        assert type(cl3) == FCLArray
        cl4 = cl3.copy()
        assert cl4 == cl3
        assert cl4 is not cl3
        cl3_copy = cl3.copy()
        cl3.reverse()
        assert cl3 != cl3_copy
        assert cl3[0] == 2
        assert cl3[1] == 1

        foo = 42
        baz = 'hello world'

        try:
            foo = cl1[0]
        except IndexError as err:
            print(err)
            assert False
        else:
            assert True
        finally:
            assert True
            assert foo == 1

        try:
            baz = cl2[42]
        except IndexError as err:
            print(err)
            assert True
        else:
            assert False
        finally:
            assert True
            assert baz == 'hello world'

        cl1 = FCLArray(size=1, default=12)
        cl2 = FCLArray(size=1, default=30)
        assert cl1 != cl2
        assert not cl1
        assert not cl2
        assert len(cl1) == 1
        assert len(cl2) == 1
        cl3 = cl1 + cl2
        assert cl3[0] == 12
        assert cl3[1] == 30

        cl1 = FCLArray()
        cl2 = FCLArray(None, None, None, size=2)
        assert cl1 != cl2
        assert cl1 is not cl2
        assert not cl1
        assert not cl2
        assert len(cl1) == 0
        assert len(cl2) == 2
        assert cl2[0] == cl2[1] == ()

        cl1 = FCLArray(1, 2, size=3, default=42)
        cl2 = FCLArray(1, 2, None, default=42)
        assert cl1 == cl2
        assert cl1 is not cl2
        assert cl1
        assert cl2
        assert len(cl1) == 3
        assert len(cl2) == 3
        assert cl1[2] == cl2[2] == cl1[-1] == cl2[-1] == 42

        cl1 = FCLArray(1, 2, size=-3)
        cl2 = FCLArray((), 1, 2)
        assert cl1 == cl2
        assert cl1 is not cl2
        assert cl1
        assert cl2
        assert len(cl1) == 3
        assert len(cl2) == 3

        cl5 = FCLArray(*range(1,4), size=-5, default=42)
        assert cl5 == FCLArray(42, 42, 1, 2, 3)

    def test_set_then_get(self):
        cl = FCLArray(size=5, default=0)
        assert cl[1] == 0
        cl[3] = set = 42
        got = cl[3]
        assert set == got

    def test_equality(self):
        cl1 = FCLArray(1, 2, 'Forty-Two', (7, 11, 'foobar'))
        cl2 = FCLArray(1, 3, 'Forty-Two', [1, 2, 3])
        assert cl1 != cl2
        cl2[1] = 2
        assert cl1 != cl2
        cl1[3] = cl2[3]
        assert cl1 == cl2

    def test_len_getting_indexing_padding_slicing(self):
        cl = FCLArray(*range(2000))
        assert len(cl) == 2000

        cl = FCLArray(*range(542), size=42)
        assert len(cl) == 42
        assert cl[0] == 0
        assert cl[41] == cl[-1] == 41
        assert cl[2] == cl[-40]

        cl = FCLArray(*range(1042), size=-42)
        assert len(cl) == 42
        assert cl[0] == 1000
        assert cl[41] == 1041
        assert cl[-1] == 1041
        assert cl[41] == cl[-1] == 1041
        assert cl[1] == cl[-41] == 1001
        assert cl[0] == cl[-42]

        cl = FCLArray(*[1, 'a', (1, 2)], size=5, default=42)
        assert cl[0] == 1
        assert cl[1] == 'a'
        assert cl[2] == (1, 2)
        assert cl[3] == 42
        assert cl[4] == 42
        assert cl[-1] == 42
        assert cl[-2] == 42
        assert cl[-3] == (1, 2)
        assert cl[-4] == 'a'
        assert cl[-5] == 1
        try:
            foo = cl[5] 
            print(f'should never print: {foo}')
        except IndexError:
            assert True
        except Exception as error:
            print(error)
            assert False
        else:
            assert False
        try:
            bar = cl[-6] 
        except IndexError:
            assert True
        except Exception as error:
            print(error)
            assert False
        else:
            assert False

        cl = FCLArray(*[1, 'a', (1, 2)], size=-6, default=42)
        assert cl[0] == 42
        assert cl[1] == 42
        assert cl[2] == 42
        assert cl[3] == 1
        assert cl[4] == 'a'
        assert cl[5] == (1, 2)
        assert cl[-1] == (1, 2)
        assert cl[-2] == 'a'
        assert cl[-3] == 1
        assert cl[-4] == 42
        assert cl[-5] == 42
        assert cl[-6] == 42
        try:
            foo = cl[6] 
            print(f'should never print: {foo}')
        except IndexError:
            assert True
        except Exception as error:
            print(error)
            assert False
        else:
            assert False
        try:
            bar = cl[-7] 
            print(f'should never print: {bar}')
        except IndexError:
            assert True
        except Exception as error:
            print(error)
            assert False
        else:
            assert False

    def test_bool(self):
        cl_allNotNone = FCLArray(True, 0, '')
        cl_allNone = FCLArray(None, None, None, default=42)
        cl_firstNone = FCLArray(None, False, [])
        cl_lastNone = FCLArray(0.0, True, False, None)
        cl_someNone = FCLArray(0, None, 42, None, False)
        cl_defaultNone = FCLArray(default = None)
        cl_defaultNotNone = FCLArray(default = False)
        assert cl_allNotNone
        assert not cl_allNone
        assert cl_firstNone
        assert cl_lastNone
        assert cl_someNone
        assert not cl_defaultNone
        assert not cl_defaultNotNone

        cl_Nones = FCLArray(None, size=4321)
        cl_0 = FCLArray(0, 0, 0)
        cl_42s = FCLArray(*([42]*42))
        cl_emptyStr = FCLArray('')
        cl_hw = FCLArray('hello', 'world')
        assert not cl_Nones
        assert cl_0
        assert cl_42s
        assert cl_emptyStr
        assert cl_hw

    def test_copy(self):
        cl4 = FCLArray(*range(43), size = 5)
        cl42 = FCLArray(*range(43), size = -5)
        cl4_copy = cl4.copy()
        cl42_copy = cl42.copy()
        assert cl4 == cl4_copy
        assert cl4 is not cl4_copy
        assert cl42 == cl42_copy
        assert cl42 is not cl42_copy
        assert cl4[0] == 0
        assert cl4[4] == cl4[-1] == 4
        assert cl42[0] == 38
        assert cl42[4] == cl42[-1] == 42

    def test_reversed_iter(self):
        """Tests that prior state of cl is used, not current one"""
        cl = FCLArray(1,2,3,4,5)
        clrevIter = reversed(cl)
        aa = next(clrevIter)
        assert cl[4] == aa == 5
        cl[2] = 42
        aa = next(clrevIter)
        assert cl[3] == aa == 4
        aa = next(clrevIter)
        assert cl[2] != aa == 3
        aa = next(clrevIter)
        assert cl[1] == aa == 2
        aa = next(clrevIter)
        assert cl[0] == aa == 1

    def test_add(self):
        cl1 = FCLArray(1,2,3)
        cl2 = FCLArray(4,5,6)
        assert cl1 + cl2 == FCLArray(1,2,3,4,5,6)
        assert cl2 + cl1 == FCLArray(4,5,6,1,2,3)

        cl1 = FCLArray(1,2,3)
        cl2 = FCLArray(4,5,6,7,8,9)
        cl12 = cl1 + cl2
        cl21 = cl2 + cl1
        assert cl12 == FCLArray(1,2,3,4,5,6,7,8,9)
        assert cl21 == FCLArray(4,5,6,7,8,9,1,2,3)

    def test_reverse(self):
        cl1 = FCLArray(1, 2, 3, 'foo', 'bar')
        cl2 = FCLArray('bar', 'foo', 3, 2, 1)
        assert cl1 != cl2
        cl2.reverse()
        assert cl1 == cl2
        cl1.reverse()
        assert cl1 != cl2
        assert cl1[1] == cl2[-2]

        cl4 = cl2.copy()
        cl5 = cl2.copy()
        assert cl4 == cl5
        cl4.reverse()
        cl5.reverse()
        assert cl4 != cl2
        assert cl5 != cl2
        cl2.reverse()
        assert cl4 == cl2
