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

from grscheller.datastructures.core.fp import Maybe, Nothing, Some
from grscheller.datastructures.core.fp import Either, Left, Right
from grscheller.datastructures.core.fp import maybe_to_either, either_to_maybe

def add2(x: int) -> int:
    return x + 2

class TestMaybe:
    def test_identity(self) -> None:
        n1: Maybe[int] = Maybe()
        n2: Maybe[int] = Maybe()
        o1 = Maybe(42)
        o2 = Maybe(40)
        assert o1 is o1
        assert o1 is not o2
        o3 = o2.map(add2)
        assert o3 is not o2
        assert o1 is not o3
        assert n1 is n1
        assert n1 is not n2
        assert o1 is not n1
        assert n2 is not o2

    def test_equality(self) -> None:
        n1: Maybe[int] = Maybe()
        n2: Maybe[int] = Maybe()
        o1 = Maybe(42)
        o2 = Maybe(40)
        assert o1 == o1
        assert o1 != o2
        o3 = o2.map(add2)
        assert o3 != o2
        assert o1 == o3
        assert n1 == n1
        assert n1 == n2
        assert o1 != n1
        assert n2 != o2

    def test_iterate(self) -> None:
        o1 = Maybe(38)
        o2 = o1.map(add2).map(add2)
        n1: Maybe[int] = Maybe()
        l1 = []
        l2 = []
        for v in n1:
            l1.append(v)
        for v in o2:
            l2.append(v)
        assert len(l1) == 0
        assert len(l2) == 1
        assert l2[0] == 42

    def test_get(self) -> None:
        o1 = Maybe(1)
        n1: Maybe[int] = Maybe()
        assert o1.get(42) == 1
        assert n1.get(42) == 42
        assert o1.get() == 1
        assert n1.get() is None
        assert n1.get(13) == (10 + 3)
        assert n1.get(10//7) == 10//7

    def test_some(self) -> None:
        o1 = Some(42)
        n1: Maybe[int] = Some(None)
        n2: Maybe[int] = Some()
        assert n1 == n2
        o2 = o1.map(lambda x: x // 2) 
        assert o2 == Some(21)
        o3 = o1.map(lambda _: None) 
        assert o3 == Some() == Nothing()

    def test_nothing(self) -> None:
        o1 = Maybe(42)
        n1: Maybe[int] = Maybe()
        n2 = n1
        assert o1 != Nothing()
        assert n1 == Nothing()
        assert n1 is n1
        assert n1 is n2

class TestEither:
    def test_identity(self) -> None:
        e1: Either[int, str] = Left(42)
        e2: Either[int, str] = Either(42, 'The secret is unknown')
        e3: Either[int, str] = Right('not 42')
        e4: Either[int, str] = Right('not 42')
        e5: Either[int, str] = Right('also not 42')
        e6 = e3
        assert e1 is e1
        assert e1 is not e2
        assert e1 is not e3
        assert e1 is not e4
        assert e1 is not e5
        assert e1 is not e6
        assert e2 is e2
        assert e2 is not e3
        assert e2 is not e4
        assert e2 is not e5
        assert e2 is not e6
        assert e3 is e3
        assert e3 is not e4
        assert e3 is not e5
        assert e3 is e6
        assert e4 is e4
        assert e4 is not e5
        assert e4 is not e6
        assert e5 is e5
        assert e5 is not e6
        assert e6 is e6

    def test_equality(self) -> None:
        e1: Either[int, str] = Left(42)
        e2: Either[int, str] = Left(42)
        e3: Either[int, str] = Right('not 42')
        e4: Either[int, str] = Right('not 42')
        e5: Either[int, str] = Right('also not 42')
        e7 = e3
        assert e1 == e1
        assert e1 == e2
        assert e1 != e3
        assert e1 != e4
        assert e1 != e5
        assert e1 != e7
        assert e2 == e2
        assert e2 != e3
        assert e2 != e4
        assert e2 != e5
        assert e2 != e7
        assert e3 == e3
        assert e3 == e4
        assert e3 != e5
        assert e3 == e7
        assert e4 == e4
        assert e4 != e5
        assert e4 == e7
        assert e5 == e5
        assert e5 != e7
        assert e7 == e7

    def test_either_right(self) -> None:
        def noMoreThan5(x: int) -> int|None:
            if x <= 5:
                return x
            else:
                return None

        s1 = Left(3, right = 'foofoo rules')
        s2 = s1.map(noMoreThan5, 'more than 5')
        s3 = Left(42, right = 'foofoo rules')
        s4 = s3.map(noMoreThan5, 'more than 5')
        assert s1 == Left(3)
        assert s2 == Left(3)
        assert s4 == Right('more than 5')
        assert s1.getRight() == None
        assert s2.getRight() == None
        assert s3.getRight() == None
        assert s4.getRight() == 'more than 5'
        assert s1.get(0) == 3
        assert s3.get(0) == 42
        assert s4.get(0) == 0
        assert s4.getRight() == 'more than 5'

    def test_either_flatMaps(self) -> None:
        def lessThan2(x: int) -> Either[int, str]:
            if x < 2:
                return Either(x, 'fail!')
            else:
                return Either(None, '>=2')

        def lessThan5(x: int) -> Either[int, str]:
            if x < 5:
                return Left(x)
            else:
                return Right('>=5')

        left1 = Left(1)
        left4 = Left(4)
        left7 = Left(7)
        right: Either[int, str] = Right('Nobody home')

        nobody = right.flatMap(lessThan2)
        assert nobody == Right('Nobody home')

        lt2 = left1.flatMap(lessThan2)
        lt5 = left1.flatMap(lessThan5)
        assert lt2 == Left(1)
        assert lt5 == Left(1)

        lt2 = left4.flatMap(lessThan2)
        lt5 = left4.flatMap(lessThan5)
        assert lt2 == Right('>=2')
        assert lt5 == Left(4)

        lt2 = left7.flatMap(lessThan2)
        lt5 = left7.flatMap(lessThan5)
        assert lt2 == Right('>=2')
        assert lt5 == Right('>=5')

        nobody = right.flatMap(lessThan5, right=', STILL NOBODY HOME')
        assert nobody == Right('Nobody home, STILL NOBODY HOME')

        lt2 = left1.flatMap(lessThan2, right='greater than or equal 2')
        lt5 = left1.flatMap(lessThan5, right='greater than or equal 5')
        assert lt2 == Left(1)
        assert lt5 == Left(1)

        lt2 = left4.flatMap(lessThan2)
        lt5 = left4.flatMap(lessThan5, right=', greater than or equal 5')
        assert lt2 == Right('>=2')
        assert lt5 == Left(4)

        lt2 = left7.flatMap(lessThan2, g=lambda x, r: r, right='greater than or equal 2')
        lt5 = left7.flatMap(lessThan5, right=', greater than or equal 5')
        assert lt2 == Right('greater than or equal 2')
        assert lt5 == Right('>=5, greater than or equal 5')

    def test_Maybe_Either(self) -> None:
        mb42 = Some(42)
        mbNot: Maybe[int] = Nothing()

        left42 = maybe_to_either(mb42, 'fail!')
        right = maybe_to_either(mbNot, 'Nobody home')
        assert left42 == Left(42)
        assert right == Right('Nobody home')

        ph42 = either_to_maybe(left42)
        phNot = either_to_maybe(right)
        assert mb42 == ph42
        assert mbNot == phNot
