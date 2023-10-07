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

from grscheller.datastructures.circle import Circle

class TestCircle:
    def test_push_then_pop(self):
        c = Circle()
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
        c.pushR('first').pushR('second').pushR('last')
        assert c.popL() == 'first'
        assert c.popR() == 'last'
        assert c
        c.popL()
        assert len(c) == 0

    def test_iterators(self):
        data = [1, 2, 3, 4]
        c = Circle(*data)
        data.reverse()
        ii = 0
        for item in reversed(c):
            assert data[ii] == item
            ii += 1
        assert ii == 4

        data.reverse()
        data.append(42)
        c.pushR(42)
        ii=0
        for item in c:
            assert data[ii] == item
            ii += 1
        assert ii == 5

    def test_capacity(self):
        c = Circle()
        assert c.capacity() == 2
        c = Circle(1, 2)
        assert c.fractionFilled() == 2/4
        c.pushL(0)
        assert c.fractionFilled() == 3/4
        c.pushR(3)
        assert c.fractionFilled() == 4/4
        c.pushR(4).pushL(5)
        assert c.fractionFilled() == 6/8
        assert len(c) == 6
        assert c.capacity() == 8
        c.resize()
        assert c.fractionFilled() == 6/6
        c.resize(30)
        assert c.fractionFilled() == 6/36

    def test_equality(self):
        c1 = Circle(1, 2, 3, 'Forty-Two', (7, 11, 'foobar'))
        c2 = Circle(2, 3, 'Forty-Two').pushL(1).pushR((7, 11, 'foobar'))
        assert c1 == c2

        tup2 = c2.popR()
        assert c1 != c2

        c2.pushR((42, 'foofoo'))
        assert c1 != c2

        c1.popR()
        c1.pushR((42, 'foofoo')).pushR(tup2)
        c2.pushR(tup2)
        assert c1 == c2

        holdA = c1.popL()
        c1.resize(42)
        holdB = c1.popL()
        holdC = c1.popR()
        c1.pushL(holdB).pushR(holdC).pushL(holdA).pushL(200)
        c2.pushL(200)
        assert c1 == c2

    def test_mapAndFlatMap(self):
        c1 = Circle(1,2,3,10)
        c1_answers = Circle(0,3,8,99)
        assert c1.map(lambda x: x*x-1) == c1_answers
        c2 = c1.flatMap(lambda x: Circle(1, x, x*x+1))
        c2_answers = Circle(1, 1, 2, 1, 2, 5, 1, 3, 10, 1, 10, 101)
        assert c2 == c2_answers

    def test_mergeMap(self):
        c1 = Circle(5, 4, 7)
        assert len(c1) == 3
        c2 = c1.mergeMap(lambda x: Circle(*([chr(0o100+x)*x]*x)))
        assert len(c2) == 3*4
        assert c2[0] == c2[3] == c2[6] == c2[9] == 'EEEEE'
        assert c2[1] == c2[4] == c2[7] == c2[10] == 'DDDD'
        assert c2[2] == c2[5] == c2[8] == c2[11] == 'GGGGGGG'
        c2 = c1.flatMap(lambda x: Circle(*([chr(0o100+x)*x]*x)))
        assert len(c2) == 5 + 4 + 7
        assert c2[0] == 'EEEEE'
        assert c2[-1] == 'GGGGGGG'

    def test_get_set_items(self):
        c1 = Circle('a', 'b', 'c', 'd')
        c2 = c1.copy()
        assert c1 == c2
        c1[2] = 'cat'
        c1[-1] = 'dog'
        assert c2.popR() == 'd'
        assert c2.popR() == 'c'
        c2.pushR('cat')
        c2[3] = 'dog'       # no such index
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
