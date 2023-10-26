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

from grscheller.datastructures.carray import CArray

class TestCarray:
    def test_push_then_pop(self):
        c = CArray()
        pushed = 42; c.pushL(pushed)
        popped = c.popL()
        assert pushed == popped
        assert len(c) == 0
        assert c.popL() == None
        pushed = 0; c.pushL(pushed)
        popped = c.popR()
        assert pushed == popped == 0
        assert not c
        pushed = 0; c.pushR(pushed)
        popped = c.popL()
        assert popped is not None
        assert pushed == popped
        assert len(c) == 0
        pushed = ''; c.pushR(pushed)
        popped = c.popR()
        assert pushed == popped
        assert len(c) == 0
        c.pushR('first')
        c.pushR('second')
        c.pushR('last')
        assert c.popL() == 'first'
        assert c.popR() == 'last'
        assert c
        c.popL()
        assert len(c) == 0

    def test_iterators(self):
        data = [*range(100)]
        c = CArray(*data)
        ii = 0
        for item in c:
            assert data[ii] == item
            ii += 1
        assert ii == 100

        data.append(100)
        c = CArray(*data)
        data.reverse()
        ii = 0
        for item in reversed(c):
            assert data[ii] == item
            ii += 1
        assert ii == 101

        c0 = CArray()
        for _ in c0:
            assert False
        for _ in reversed(c0):
            assert False

        data = ()
        c0 = CArray(*data)
        for _ in c0:
            assert False
        for _ in reversed(c0):
            assert False

    def test_capacity(self):
        c = CArray()
        assert c.capacity() == 2
        c = CArray(1, 2)
        assert c.fractionFilled() == 2/4
        c.pushL(0)
        assert c.fractionFilled() == 3/4
        c.pushR(3)
        assert c.fractionFilled() == 4/4
        c.pushR(4)
        c.pushL(5)
        assert c.fractionFilled() == 6/8
        assert len(c) == 6
        assert c.capacity() == 8
        c.resize()
        assert c.fractionFilled() == 6/6
        c.resize(30)
        assert c.fractionFilled() == 6/36

    def test_equality(self):
        c1 = CArray(1, 2, 3, 'Forty-Two', (7, 11, 'foobar'))
        c2 = CArray(2, 3, 'Forty-Two')
        c2.pushL(1)
        c2.pushR((7, 11, 'foobar'))
        assert c1 == c2

        tup2 = c2.popR()
        assert c1 != c2

        c2.pushR((42, 'foofoo'))
        assert c1 != c2

        c1.popR()
        c1.pushR((42, 'foofoo'))
        c1.pushR(tup2)
        c2.pushR(tup2)
        assert c1 == c2

        holdA = c1.popL()
        c1.resize(42)
        holdB = c1.popL()
        holdC = c1.popR()
        c1.pushL(holdB)
        c1.pushR(holdC)
        c1.pushL(holdA)
        c1.pushL(200)
        c2.pushL(200)
        assert c1 == c2

    def test_map(self):
        c1 = CArray(1,2,3,10)
        c2 = c1.map(lambda x: x*x-1)
        c2_answers = CArray(0,3,8,99)
        assert c2 == c2_answers
        assert c1 != c2
        assert c1 is not c2
        assert len(c1) == len(c2) == 4

    def test_mapSelf(self):
        c1 = CArray(1,2,3,10)
        c1.map_update(lambda x: x*x-1)
        c1_answers = CArray(0,3,8,99)
        assert c1 == c1_answers
        assert len(c1) == 4

    def test_flatMap(self):
        c1 = CArray(1,2,3,10)
        c2 = c1.flatMap(lambda x: CArray(1, x, x*x+1))
        c2_answers = CArray(1, 1, 2, 1, 2, 5, 1, 3, 10, 1, 10, 101)
        assert c2 == c2_answers
        assert len(c2) == 3*len(c1) == 12
        c3 = CArray()
        c4 = c3.flatMap(lambda x: CArray(1, x, x*x+1))
        assert c3 == c4 == CArray()
        assert c3 is not c4

    def test_flatMapSelf(self):
        c1 = CArray(1,2,3,5,10)
        c1.flatMap_update(lambda x: CArray(1, x, x*x+1))
        c1_answers = CArray(1, 1, 2, 1, 2, 5, 1, 3, 10, 1, 5, 26, 1, 10, 101)
        assert c1 == c1_answers
        assert len(c1) == 5*3

    def test_mergeMap(self):
        c1 = CArray(5, 4, 7)
        min1 = min(iter(c1))
        len1 = len(c1)
        c2 = c1.mergeMap(lambda x: CArray(*([chr(0o100+x)*x]*x)))
        assert c2[0] == c2[3] == c2[6] == c2[9] == 'EEEEE'
        assert c2[1] == c2[4] == c2[7] == c2[10] == 'DDDD'
        assert c2[2] == c2[5] == c2[8] == c2[11] == 'GGGGGGG'
        assert c2[-1] == 'GGGGGGG'
        assert len(c2) == len1*min1 == 3*4
        assert len(c1) == len1 == 3

        c1 = CArray(3)
        min1 = min(iter(c1))
        len1 = len(c1)
        c2 = c1.mergeMap(lambda x: CArray(*([chr(0o100+x)*x]*x)))
        assert c2[0] == c2[1] == c2[2] == 'CCC'
        assert c2[-1] == 'CCC'
        assert len(c2) == len1*min1 == 1*3
        assert len(c1) == len1

        c1 = CArray()
        len1 = len(c1)
        c2 = c1.mergeMap(lambda x: CArray(*([chr(0o100+x)*x]*x)))
        assert len(c2) == len1 == 0
        assert len(c1) == len1 == 0

    def test_mergeMapSelf(self):
        c1 = CArray(5, 4, 7)
        min1 = min(iter(c1))
        len1 = len(c1)
        c1.mergeMap_update(lambda x: CArray(*([chr(0o100+x)*x]*x)))
        assert c1[0] == c1[3] == c1[6] == c1[9] == 'EEEEE'
        assert c1[1] == c1[4] == c1[7] == c1[10] == 'DDDD'
        assert c1[2] == c1[5] == c1[8] == c1[11] == 'GGGGGGG'
        assert c1[-1] == 'GGGGGGG'
        assert len(c1) == len1*min1 == 3*4

        c1 = CArray(2)
        min1 = min(iter(c1))
        len1 = len(c1)
        c1.mergeMap_update(lambda x: CArray(*([chr(0o100+x)*x]*x)))
        assert c1[0] == c1[1] == 'BB'
        assert c1[-1] == 'BB'
        assert len(c1) == len1*min1 == 1*2

        c1 = CArray()
        len1 = len(c1)
        c1.mergeMap_update(lambda x: CArray(*([chr(0o100+x)*x]*x)))
        assert len(c1) == len1 == 0

    def test_get_set_items(self):
        c1 = CArray('a', 'b', 'c', 'd')
        c2 = c1.copy()
        assert c1 == c2
        c1[2] = 'cat'
        c1[-1] = 'dog'
        assert c2.popR() == 'd'
        assert c2.popR() == 'c'
        c2.pushR('cat')
        try:
            c2[3] = 'dog'       # no such index
        except IndexError:
            assert True
        except:
            assert False
        else:
            assert False
        assert c1 != c2
        c2.pushR('dog')
        assert c1 == c2
        c2[1] = 'bob'
        assert c1 != c2
        assert c1.popL() == 'a'
        c1[0] = c2[1]
        assert c1 != c2
        assert c2.popL() == 'a'
        assert c1 == c2
