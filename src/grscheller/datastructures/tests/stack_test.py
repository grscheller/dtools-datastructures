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

from grscheller.datastructures.stack import Stack
from grscheller.datastructures.iterlib import concatIters
import grscheller.datastructures.stack as stack

class Test_Node:
    def test_bool(self):
        n1 = stack._Node(1, None)
        n2 = stack._Node(2, n1)
        assert n1
        assert n2

    def test_linking(self):
        n1 = stack._Node(1, None)
        n2 = stack._Node(2, n1)
        n3 = stack._Node(3, n2)
        assert n3._data == 3
        assert n3._next is not None
        assert n3._next._next is not None
        assert n2._next is not None
        assert n2._data == n3._next._data == 2
        assert n1._data == n2._next._data == n3._next._next._data == 1
        assert n3._next != None
        assert n3._next._next != None
        assert n3._next._next._next == None
        assert n3._next._next == n2._next

class TestStack:
    def test_push_then_pop(self):
        s1 = Stack()
        pushed = 42; s1.push(pushed)
        popped = s1.pop()
        assert pushed == popped == 42

    def test_pop_from_empty_stack(self):
        s1 = Stack()
        popped = s1.pop()
        assert popped is None

        s2 = Stack(1, 2, 3, 42)
        while s2:
            assert s2.peak() is not None
            s2.pop()
        assert not s2
        assert s2.peak() is None
        s2.push(42)
        assert s2.peak() == 40+2
        assert s2.pop() == 42
        assert s2.peak() is None

    def test_stack_len(self):
        s0 = Stack()
        s1 = Stack(*range(0,2000))

        assert len(s0) == 0
        assert len(s1) == 2000
        s0.push(42)
        s1.pop()
        s1.pop()
        assert len(s0) == 1
        assert len(s1) == 1998

    def test_tail_cons(self):
        s1 = Stack()
        s1.push("fum")
        s1.push("fo")
        s1.push("fi")
        s1.push("fe")
        s2 = s1.tail()
        if s2 is None:
            assert False
        s3 = s2.cons("fe")
        assert s3 == s1
        while s1:
            s1.pop()
        assert s1.pop() == None
        assert s1.tail() == None

    def test_stack_iter(self):
        giantStack = Stack(*[" Fum", " Fo", " Fi", "Fe"])
        giantTalk = giantStack.pop()
        assert giantTalk == "Fe"
        for giantWord in giantStack:
            giantTalk += giantWord
        assert len(giantStack) == 3
        assert giantTalk == "Fe Fi Fo Fum"

        es = Stack()
        for _ in es:
            assert False

    def test_equality(self):
        s1 = Stack(*range(3))
        s2 = s1.cons(42)
        assert s1 is not s2
        assert s1 is not s2.tailOrElse()
        assert s1 != s2
        assert s1 == s2.tail()

        assert s2.peak() == 42
        assert s2.pop() == 42

        s3 = Stack(range(10000))
        s4 = s3.copy()
        assert s3 is not s4
        assert s3 == s4
        
        s3.push(s4.pop())
        assert s3 is not s4
        assert s3 != s4
        s3.pop()
        s3.pop()
        assert s3 == s4

        s5 = Stack(*[1,2,3,4])
        s6 = Stack(*[1,2,3,42])
        assert s5 != s6
        for aa in range(10):
            s5.push(aa)
            s6.push(aa)
        assert s5 != s6

        ducks = ["huey", "dewey"]
        s7 = Stack(ducks)
        s8 = Stack(ducks)
        s9 = Stack(["huey", "dewey", "louie"])
        assert s7 == s8
        assert s7 != s9
        assert s7.peak() == s8.peak()
        assert s7.peak() is s8.peak()
        assert s7.peak() != s9.peak()
        assert s7.peak() is not s9.peak()
        ducks.append("louie")
        assert s7 == s8
        assert s7 == s9
        s7.push(['moe', 'larry', 'curlie'])
        s8.push(['moe', 'larry'])
        assert s7 != s8
        s8.peakOrElse([]).append("curlie")
        assert s7 == s8

    def test_doNotStoreNones(self):
        s1 = Stack()
        s1.push(None)
        s1.push(None)
        s1.push(None)
        s1.push(42)
        s1.push(None)
        assert len(s1) == 1
        s1.pop()
        assert not s1

    def test_reversing(self):
        s1 = Stack('a', 'b', 'c', 'd')
        s2 = Stack('d', 'c', 'b', 'a')
        assert s1 != s2
        assert s2 == Stack(*iter(s1))
        s0 = Stack()
        assert s0 == Stack(*iter(s0))
        s2 = Stack(concatIters(iter(range(1, 100)), iter(range(98, 0, -1))))
        s3 = Stack(*iter(s2))
        assert s3 == s2

    def test_reversed(self):
        lf = [1.0, 2.0, 3.0, 4.0]
        lr = [4.0, 3.0, 2.0, 1.0]
        s1 = Stack(4.0, 3.0, 2.0, 1.0)
        l_s1 = list(s1)
        l_r_s1 = list(reversed(s1))
        assert lf == l_s1
        assert lr == l_r_s1
        s2 = Stack(*lf)
        while s2:
            assert s2.pop() == lf.pop()

    def test_map(self):
        s1 = Stack(1,2,3,4,5)
        s2 = s1.map(lambda x: 2*x+1)
        assert s1.peak() == 5
        assert s2.peak() == 11
        s3 = s2.map(lambda y: (y-1)//2)
        assert s1 == s3
        assert s1 is not s3

    def test_flatMap(self):
        c1 = Stack(1, 20, 300)
        c2 = c1.flatMap(lambda x: Stack(x, x+1))
        c2_answers = Stack(1, 2, 20, 21, 300, 301)
        assert c2 == c2_answers
        assert len(c2) == 2*len(c1) == 6
        c3 = Stack()
        c4 = c3.flatMap(lambda x: Stack(x, x+1))
        assert c3 == c4 == Stack()
        assert c3 is not c4

    def test_mergeMap(self):
        c1 = Stack(1, 20, 300)
        c2 = c1.mergeMap(lambda x: Stack(x, x+1))
        c2_answers = Stack(1, 20, 300, 2, 21, 301)
        assert c2 == c2_answers
        assert len(c2) == 2*len(c1) == 6
        c3 = Stack()
        c4 = c3.flatMap(lambda x: Stack(x, x+1))
        assert c3 == c4 == Stack()
        assert c3 is not c4
