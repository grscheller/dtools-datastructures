# Copyright 2023-2024 Geoffrey R. Scheller
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

from __future__ import annotations

from typing import Optional
from grscheller.datastructures.queues import DoubleQueue, FIFOQueue, LIFOQueue
from grscheller.datastructures.split_ends import SplitEnd
from grscheller.datastructures.tuples import FTuple

def addLt42(x: int, y: int) -> int|None:
    sum = x + y
    if sum < 42:
        return sum
    return None

class Test_str:
    def test_SplitEnd(self) -> None:
        s1: SplitEnd[Optional[object]] = SplitEnd()
        assert str(s1) == '><  ||'
        s2 = s1.cons(42)
        assert str(s1) == '><  ||'
        assert str(s2) == '>< 42 ||'
        del s1
        s1 = s2.cons(None)
        assert s1 == s2
        s1 = s2.cons(0)
        assert str(s1) == '>< 0 <- 42 ||'
        s3 = s1.cons('wins!').cons('Buggy the clown')
        assert str(s3) == ">< Buggy the clown <- wins! <- 0 <- 42 ||"

        foo = SplitEnd(1, 2)
        bar = foo.copy()
        assert bar.head() == 2
        foo = foo.cons(3).cons(4).cons(5)
        baz = bar.cons(3).cons(4).cons(5)
        assert str(foo) == '>< 5 <- 4 <- 3 <- 2 <- 1 ||'
        assert str(baz) == '>< 5 <- 4 <- 3 <- 2 <- 1 ||'
        assert foo == baz
        assert foo is not baz

    def test_FIFOQueue(self) -> None:
        q1: FIFOQueue[int] = FIFOQueue()
        assert str(q1) == '<<  <<'
        q1.push(1, 2, 3, 42)
        q1.pop()
        assert str(q1) == '<< 2 < 3 < 42 <<'

    def test_LIFOQueue(self) -> None:
        q1: LIFOQueue[int] = LIFOQueue()
        assert str(q1) == '||  ><'
        q1.push(1, 2, 3, 42)
        q1.pop()
        assert str(q1) == '|| 3 > 2 > 1 ><'

    def test_DQueue(self) -> None:
        dq1: DoubleQueue[int] = DoubleQueue()
        dq2: DoubleQueue[int] = DoubleQueue()
        assert str(dq1) == '><  ><'
        dq1.pushL(1, 2, 3, 4, 5, 6)
        dq2.pushR(1, 2, 3, 4, 5, 6)
        dq1.popL()
        dq1.popR()
        dq2.popL()
        dq2.popR()
        assert str(dq1) == '>< 5 | 4 | 3 | 2 ><'
        assert str(dq2) == '>< 2 | 3 | 4 | 5 ><'

    def test_ftuple(self) -> None:
        ft1 = FTuple(1,2,3,4,5)
        ft2: FTuple[int] = ft1.flatMap(lambda x: FTuple(*range(1, x)))
        assert str(ft1) == '((1, 2, 3, 4, 5))'
        assert str(ft2) == '((1, 1, 2, 1, 2, 3, 1, 2, 3, 4))'
