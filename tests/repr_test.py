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

from grscheller.datastructures.functional import Maybe, Nothing, Some
from grscheller.datastructures.functional import Either, Left, Right
from grscheller.datastructures.core.carray import CArray
from grscheller.datastructures import FStack, PStack
from grscheller.datastructures import SQueue, DQueue, FLArray
from grscheller.datastructures import FLArray, FTuple


def addLt42(x: int, y: int) -> int|None:
    sum = x + y
    if sum < 42:
        return sum
    return None

class Test_repr:
    def test_Maybe(self):
        n1 = Maybe()
        o1 = Maybe(42)
        assert repr(n1) == 'Nothing'
        assert repr(o1) == 'Some(42)'
        mb1 = Maybe(addLt42(3, 7))
        mb2 = Maybe(addLt42(15, 30))
        assert repr(mb1) == 'Some(10)'
        assert repr(mb2) == 'Nothing'
        nt1 = Nothing
        nt2 = Some(None)
        nt3 = Some()
        s1 = Some(1)
        assert repr(nt1) == repr(nt2) == repr(nt3) == repr(mb2) =='Nothing'
        assert repr(s1) == 'Some(1)'

    def test_Either(self):
        assert repr(Either(10)) == 'Left(10)'
        assert repr(Either(addLt42(10, -4))) == 'Left(6)'
        assert repr(Either(addLt42(10, 40))) == 'Right(None)'
        assert repr(Either(None, 'Foofoo rules')) == "Right('Foofoo rules')"
        assert repr(Left(42)) == 'Left(42)'
        assert repr(Right(13)) == 'Right(13)'

    def test_PStack(self):
        s1 = PStack()
        assert repr(s1) == '||  ><'
        assert repr(s1.push(42)) == '|| 42 ><'
        assert repr(s1.push()) == '|| 42 ><'
        assert repr(s1.push('Buggy the clown')) == "|| 42 <- 'Buggy the clown' ><"
        assert repr(s1.pop()) == "'Buggy the clown'"
        foo = PStack(1)
        bar = foo.copy()
        bar.pop()
        foo.push(2,3,4)
        baz = bar.push(2).push(3).push(4)
        assert repr(foo) == '|| 1 <- 2 <- 3 <- 4 ><'
        assert repr(baz) == '|| 2 <- 3 <- 4 ><'
        assert repr(bar) == '|| 2 <- 3 <- 4 ><'
        assert bar == baz
        assert bar is baz

    def test_FStack(self):
        s1 = FStack()
        assert repr(s1) == '|  ><'
        s2 = s1.cons(42)
        assert repr(s1) == '|  ><'
        assert repr(s2) == '| 42 ><'
        del s1
        s1 = s2.cons(None)
        assert s1 == s2
        s1 = s2.cons(())
        assert repr(s1) == '| 42 <- () ><'
        s3 = s1.cons('Buggy the clown').cons('wins!')
        assert repr(s3) == "| 42 <- () <- 'Buggy the clown' <- 'wins!' ><"

        foo = FStack(1, 2)
        bar = foo.copy()
        assert bar.head() == 2
        foo = foo.cons(3).cons(4).cons(5)
        baz = bar.cons(3).cons(4).cons(5)
        assert repr(foo) == '| 1 <- 2 <- 3 <- 4 <- 5 ><'
        assert repr(baz) == '| 1 <- 2 <- 3 <- 4 <- 5 ><'
        assert foo ==baz
        assert foo is not baz

    def test_Queue(self):
        q1 = SQueue()
        assert repr(q1) == '<<  <<'
        q1.push(1, 2, 3, 42)
        q1.pop()
        assert repr(q1) == '<< 2 < 3 < 42 <<'

    def test_Dqueue(self):
        dq1 = DQueue()
        dq2 = DQueue()
        assert repr(dq1) == '><  ><'
        dq1.pushL(1, 2, 3, 4, 5, 6)
        dq2.pushR(1, 2, 3, 4, 5, 6)
        dq1.popL()
        dq1.popR()
        dq2.popL()
        dq2.popR()
        assert repr(dq1) == '>< 5 | 4 | 3 | 2 ><'
        assert repr(dq2) == '>< 2 | 3 | 4 | 5 ><'

    def test_flarray(self):
        fl = FLArray(1,2,3,4,5)
        fl[2] = 42
        assert repr(fl) == '[|1, 2, 42, 4, 5|]'

    def test_ftuple(self):
        ft1 = FTuple(1,2,3,4,5)
        ft2 = ft1.flatMap(lambda x: FTuple(*range(1, x)))
        assert repr(ft1) == '((1, 2, 3, 4, 5))'
        assert repr(ft2) == '((1, 1, 2, 1, 2, 3, 1, 2, 3, 4))'

    def testCArray(self):
        ca = CArray()
        assert repr(ca) == '(||)'
        ca.pushR(1)
        ca.pushL('foo')
        assert repr(ca) == "(|'foo', 1|)"
        assert ca.popL() == 'foo'
        ca.pushR(2)
        ca.pushR(3)
        ca.pushR(4)
        ca.pushR(5)
        assert ca.popL() == 1
        ca.pushL(42)
        ca.popR()
        assert repr(ca) == '(|42, 2, 3, 4|)'

