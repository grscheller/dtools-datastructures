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
# from grscheller.datastructures.core.carray import Carray
from grscheller.datastructures import FStack, PStack
# from grscheller.datastructures import Queue, Dqueue, FLarray


def addLt42(x: int, y: int) -> int|None:
    sum = x + y
    if sum < 42:
        return sum
    return None

class TestMaybe:
    def test_identity(self):
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

    def testEither(self):
        assert repr(Either(10)) == 'Left(10)'
        assert repr(Either(addLt42(10, -4))) == 'Left(6)'
        assert repr(Either(addLt42(10, 40))) == 'Right(None)'
        assert repr(Either(None, 'Foofoo rules')) == "Right('Foofoo rules')"
        assert repr(Left(42)) == 'Left(42)'
        assert repr(Right(13)) == 'Right(13)'

class TestPStack:
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

# class TestFStack:
#     s1 = FStack()
#     assert repr(s1) == '|  ><'
#     s2 = s1.push(42)
#     assert repr(s1) == '| 42 ><'
#     assert repr(s2) == '| 42 ><'
#     del s1
#     assert repr(s2.push()) == '| 42 ><'
#     s2.push('Buggy the clown').push('wins!')
#     assert repr(s2) == "| 42 <- 'Buggy the clown' <- 'wins!' ><"
# 
#     foo = FStack(1, 2)
#     bar = foo.copy()
#     assert bar.pop() == 2
#     foo.push(3, 4, 5)
#     baz = bar.push(2).push(3).push(4).push(5)
#     assert repr(foo) == '| 1 <- 2 <- 3 <- 4 <- 5 ><'
#     assert repr(baz) == '| 1 <- 2 <- 3 <- 4 <- 5 ><'
#     assert repr(bar) == '| 1 <- 2 <- 3 <- 4 <- 5 ><'
#     assert foo == bar ==baz
#     assert foo is not bar
#     assert baz is bar
# 
