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

from grscheller.datastructures.stack import PStack, FStack
from grscheller.datastructures.core.iterlib import concat
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

class TestPStack:
    def test_pushThenPop(self):
        s1 = PStack()
        pushed = 42; s1.push(pushed)
        popped = s1.pop()
        assert pushed == popped == 42

    def test_popFromEmptyStack(self):
        s1 = PStack()
        popped = s1.pop()
        assert popped is None

        s2 = PStack(1, 2, 3, 42)
        while s2:
            assert s2.peak() is not None
            s2.pop()
        assert not s2
        assert s2.peak() is None
        s2.push(42)
        assert s2.peak() == 40+2
        assert s2.pop() == 42
        assert s2.peak() is None

    def test_StackLen(self):
        s0 = PStack()
        s1 = PStack(*range(0,2000))

        assert len(s0) == 0
        assert len(s1) == 2000
        s0.push(42)
        s1.pop()
        s1.pop()
        assert len(s0) == 1
        assert len(s1) == 1998

    def test_nolongerTailCons(self):
        s1 = PStack()
        s1.push("fum")
        s1.push("fo")
        s1.push("fi")
        s1.push("fe")
        s2 = s1.copy()
        assert s2.pop() == "fe"
        if s2 is None:
            assert False
        s3 = s2.copy()
        s3.push("fe")
        assert s3 == s1
        while s1:
            s1.pop()
        assert s1.pop() == None

    def test_stack_iter(self):
        giantStack = PStack(*[" Fum", " Fo", " Fi", "Fe"])
        giantTalk = giantStack.pop()
        assert giantTalk == "Fe"
        for giantWord in giantStack:
            giantTalk += giantWord
        assert len(giantStack) == 3
        assert giantTalk == "Fe Fi Fo Fum"

        es = PStack()
        for _ in es:
            assert False

    def test_equality(self):
        s1 = PStack(*range(3))
        s2 = s1.copy().push(42)
        assert s1 is not s2
        assert s1 != s2

        assert s2.peak() == 42
        assert s2.pop() == 42

        s3 = PStack(range(10000))
        s4 = s3.copy()
        assert s3 is not s4
        assert s3 == s4
        s3.push(s4.pop())
        assert s3 is not s4
        assert s3 != s4
        s3.pop()
        s3.pop()
        assert s3 == s4

        s5 = PStack(*[1,2,3,4])
        s6 = PStack(*[1,2,3,42])
        assert s5 != s6
        for aa in range(10):
            s5.push(aa)
            s6.push(aa)
        assert s5 != s6

        ducks = ['huey', 'dewey']
        s7 = PStack(ducks)
        s8 = PStack(ducks)
        s9 = PStack(['huey', 'dewey', 'louie'])
        assert s7 == s8
        assert s7 != s9
        assert s7.peak() == s8.peak()
        assert s7.peak() is s8.peak()
        assert s7.peak() != s9.peak()
        assert s7.peak() is not s9.peak()
        ducks.append('louie')
        assert s7 == s8
        assert s9 == s8
        s7.push(['moe', 'larry', 'curlie'])
        s8.push(['moe', 'larry'])
        assert s7 != s8
        s8.peak([]).append("curlie")
        assert s7 == s8

    def test_doNotStoreNones(self):
        s1 = PStack()
        s1.push(None)
        s1.push(None)
        s1.push(None)
        s1.push(42)
        s1.push(None)
        assert len(s1) == 1
        s1.pop()
        assert not s1

    def test_reversing(self):
        s1 = PStack('a', 'b', 'c', 'd')
        s2 = PStack('d', 'c', 'b', 'a')
        assert s1 != s2
        assert s2 == PStack(*iter(s1))
        s0 = PStack()
        assert s0 == PStack(*iter(s0))
        s2 = PStack(concat(iter(range(1, 100)), iter(range(98, 0, -1))))
        s3 = PStack(*iter(s2))
        assert s3 == s2

    def test_reversed(self):
        lf = [1.0, 2.0, 3.0, 4.0]
        lr = [4.0, 3.0, 2.0, 1.0]
        s1 = PStack(4.0, 3.0, 2.0, 1.0)
        l_s1 = list(s1)
        l_r_s1 = list(reversed(s1))
        assert lf == l_s1
        assert lr == l_r_s1
        s2 = PStack(*lf)
        while s2:
            assert s2.pop() == lf.pop()

    def test_map(self):
        s1 = PStack(1,2,3,4,5)
        s1.map(lambda x: 2*x+1)
        assert s1.peak() == 11
        s1.map(lambda y: (y-1)//2)
        assert s1.peak() == 5
        assert len(s1) == 5

    def test_flatMap(self):
        c0 = PStack()
        c1 = PStack(2, 1, 3)
        c2 = PStack(2, 1, 3)
     #  c2 = c1.copy()
        c1.flatMap(lambda x: PStack(*range(x, 3*x)))
        assert c1 == PStack(2, 3, 4, 5, 1, 2, 3, 4, 5, 6, 7, 8)
        c2.flatMap(lambda x: PStack(x, x+1))
        assert c2 == PStack(2, 3, 1, 2, 3, 4)
        c0.flatMap(lambda x: PStack(x, x+1))
        assert c0 == PStack()

    def test_mergeMap(self):
        c0 = PStack()
        c1 = PStack(2, 1, 3)
        c2 = PStack(2, 1, 3)
     #  c2 = c1.copy()
        c1.mergeMap(lambda x: PStack(*range(x, 2*x+1)))
        assert c1 == PStack(2, 1, 3, 3, 2, 4)
        c2.mergeMap(lambda x: PStack(x, x+1))
        assert c2 == PStack(2, 1, 3, 3, 2, 4)
        c0.mergeMap(lambda x: PStack(x, x+1))
        assert c0 == PStack()

    def test_exhaustMap(self):
        c0 = PStack()
        c1 = PStack(2, 1, 3)
        c2 = PStack(2, 1, 3)
     #  c2 = c1.copy()
        c0.exhaustMap(lambda x: PStack(x, x+1))
        assert c0 == PStack()
        c1.exhaustMap(lambda x: PStack(x, x+1))
        assert c1 == PStack(2, 1, 3, 3, 2, 4)
        c2.exhaustMap(lambda x: PStack(*range(x, 2*x+1)))
        assert c2 == PStack(2, 1, 3, 3, 2, 4, 4, 5, 6)
        c2.exhaustMap(lambda _: PStack())
        assert c2 == PStack()

class Test_FStack:
    def test_consTail(self):
        s1 = FStack()
        s2 = s1.cons(42)
        head = s2.head(())
        assert head == 42

    def test_headOfEmptyStack(self):
        s1 = FStack()
        assert s1.head() is None

        s2 = FStack(1, 2, 3, 42)
        while s2:
            assert s2.head() is not None
            s2 = s2.tail()
            if not s2:
                break
        assert not s2
        assert len(s2) == 0
        assert s2.head() is None
        s2 = s2.cons(42)
        assert s2.head() == 40+2

    def test_Stacklen(self):
        s0 = FStack()
        s1 = FStack(*range(0,2000))

        assert len(s0) == 0
        assert len(s1) == 2000
        s0 = s0.cons(42)
        s1 = s1.tail().tail()
        assert len(s0) == 1
        assert len(s1) == 1998

    def test_tailcons(self):
        s1 = FStack()
        s1 = s1.cons("fum").cons("fo").cons("fi").cons("fe")
        assert type(s1) == FStack
        s2 = s1.tail()
        if s2 is None:
            assert False
        s3 = s2.cons("fe")
        assert s3 == s1
        while s1:
            s1 = s1.tail()
        assert s1.head() == None
        assert s1.tail() == FStack()

    def test_stackIter(self):
        giantStack = FStack(*[" Fum", " Fo", " Fi", "Fe"])
        giantTalk = giantStack.head()
        giantStack = giantStack.tail()
        assert giantTalk == "Fe"
        for giantWord in giantStack:
            giantTalk += giantWord
        assert len(giantStack) == 3
        assert giantTalk == "Fe Fi Fo Fum"

        es = FStack()
        for _ in es:
            assert False

    def test_equality(self):
        s1 = FStack(*range(3))
        s2 = s1.cons(42)
        assert s2 is not None  # How do I let the typechecker
                               # know this can't be None?
        assert s1 is not s2
        assert s1 is not s2.tail()
        assert s1 != s2
        assert s1 == s2.tail()

        assert s2.head() == 42

        s3 = FStack(range(10000))
        s4 = s3.copy()
        assert s3 is not s4
        assert s3 == s4
        
        s3 = s3.cons(s4.head())
        s4 = s4.tail()
        assert s3 is not s4
        assert s3 != s4
        assert s3 is not None  # Not part of the tests,
                               # code idiot checking.
        s3 = s3.tail().tail()
        assert s3 == s4
        assert s3 is not None
        assert s4 != None

        s5 = FStack(*[1,2,3,4])
        s6 = FStack(*[1,2,3,42])
        assert s5 != s6
        for aa in range(10):
            s5 = s5.cons(aa)
            s6 = s6.cons(aa)
        assert s5 != s6

        ducks = ["huey", "dewey"]
        s7 = FStack(ducks)
        s8 = FStack(ducks)
        s9 = FStack(["huey", "dewey", "louie"])
        assert s7 == s8
        assert s7 != s9
        assert s7.head() == s8.head()
        assert s7.head() is s8.head()
        assert s7.head() != s9.head()
        assert s7.head() is not s9.head()
        ducks.append("louie")
        assert s7 == s8
        assert s7 == s9
        s7 = s7.cons(['moe', 'larry', 'curlie'])
        s8 = s8.cons(['moe', 'larry'])
        assert s7 != s8
        assert s8 is not None
        s8.head(default = []).append("curlie")
        assert s7 == s8

    def test_doNotStoreNones(self):
        s1 = FStack()
        assert s1.cons(None) == s1
        s2 = s1.cons(42)
        assert len(s2) == 1
        assert s2
        s2 = s2.tail()
        assert not s1
        assert not s2
        assert len(s2) == 0

    def test_reversing(self):
        s1 = FStack('a', 'b', 'c', 'd')
        s2 = FStack('d', 'c', 'b', 'a')
        assert s1 != s2
        assert s2 == FStack(*iter(s1))
        s0 = FStack()
        assert s0 == FStack(*iter(s0))
        s2 = FStack(concat(iter(range(1, 100)), iter(range(98, 0, -1))))
        s3 = FStack(*iter(s2))
        assert s3 == s2

    def test_reversed(self):
        lf = [1.0, 2.0, 3.0, 4.0]
        lr = [4.0, 3.0, 2.0, 1.0]
        s1 = FStack(*lr)
        l_s1 = list(s1)
        l_r_s1 = list(reversed(s1))
        assert lf == l_s1
        assert lr == l_r_s1
        s2 = FStack(*lf)
        while s2:
            assert s2.head() == lf.pop()
            s2 = s2.tail()
        assert len(s2) == 0

    def test_map(self):
        s1 = FStack(1,2,3,4,5)
        s2 = s1.map(lambda x: 2*x+1)
        assert s1.head() == 5
        assert s2.head() == 11
        s3 = s2.map(lambda y: (y-1)//2)
        assert s1 == s3
        assert s1 is not s3

    def test_flatMap(self):
        c1 = FStack(2, 1, 3)
        c2 = c1.flatMap(lambda x: FStack(*range(x, 3*x)))
        assert c2 == FStack(2, 3, 4, 5, 1, 2, 3, 4, 5, 6, 7, 8)
        c3 = FStack()
        c4 = c3.flatMap(lambda x: FStack(x, x+1))
        assert c3 == c4 == FStack()
        assert c3 is not c4

    def test_mergeMap(self):
        c1 = FStack(2, 1, 3)
        c2 = c1.mergeMap(lambda x: FStack(*range(x, 3*x)))
        assert c2 == FStack(2, 1, 3, 3, 2, 4)
        c3 = FStack()
        c4 = c3.mergeMap(lambda x: FStack(x, x+1))
        assert c3 == c4 == FStack()
        assert c3 is not c4

    def test_exhaustMap(self):
        c1 = FStack(2, 1, 3)
        c2 = c1.exhaustMap(lambda x: FStack(*range(x, 3*x)))
        assert c2 == FStack(2, 1, 3, 3, 2, 4, 4, 5, 5, 6, 7, 8)
        c3 = FStack()
        c4 = c3.exhaustMap(lambda x: FStack(x, x+1))
        assert c3 == c4 == FStack()
        assert c3 is not c4
